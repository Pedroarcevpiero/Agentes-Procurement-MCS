"""Hooks `PreToolUse` (guardrails deterministas) del sistema de procurement.

Tres hooks, todos callbacks async con la firma `HookCallback` del SDK
(`(input_data, tool_use_id, context) -> HookJSONOutput`):

1. `require_citation_hook` — bloquea (`deny`) `record_savings_opportunity`
   si `source_transaction_ids`/`source_benchmark_ids` estan vacios o
   contienen ids que no existen en Postgres.
2. `confidence_and_threshold_hook` — degrada `status` a `needs_review`
   (via `updatedInput`, ver nota de API abajo) si la confianza esta por
   debajo del umbral o el ahorro reportado excede los limites de
   `policies/category_copilot.yaml`.
3. `no_transactional_execution_hook` — deniega cualquier tool cuyo nombre
   coincida con la denylist transaccional global de `policies/common.yaml`.

`build_hook_matchers()` empaqueta los tres en `HookMatcher` listos para
`ClaudeAgentOptions(hooks={"PreToolUse": build_hook_matchers()})`.

Nota de API (SDK real vs. plan): `claude-agent-sdk==0.2.110` SI soporta
`updatedInput` en `PreToolUseHookSpecificOutput` (ver
`claude_agent_sdk/types.py::PreToolUseHookSpecificOutput`), a diferencia de
lo que el plan daba por incierto ("investiga que soporta la version
instalada"). Por eso `confidence_and_threshold_hook` implementa la opcion 1
del plan (modificar `tool_input` en el sitio) en vez de la alternativa de
denegar pidiendo reintento.
"""
from __future__ import annotations

import logging
from typing import Any

from sqlalchemy import func, select

from procurement_agents.data_spine.db import session_scope
from procurement_agents.data_spine.models import SpendTransaction
from procurement_agents.guardrails.policy_engine import get_category_copilot_policy, get_common_policy
from procurement_agents.mcp_servers.tools._common import ToolInputError
from procurement_agents.mcp_servers.tools.recording_tools import validate_citations

from claude_agent_sdk import HookMatcher

logger = logging.getLogger(__name__)

RECORD_SAVINGS_OPPORTUNITY_TOOL = "mcp__data_spine__record_savings_opportunity"

# Estados que ya implican revision humana o rechazo; no tiene sentido
# "degradar" un tool_input que ya viene en uno de estos estados.
_ALREADY_REVIEWED_STATUSES = {"needs_review", "rejected"}


def _deny(reason: str) -> dict[str, Any]:
    """Construye un `SyncHookJSONOutput` de PreToolUse que deniega la llamada."""
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }


def _allow() -> dict[str, Any]:
    """Salida neutra: no opina, deja que otras reglas de permisos decidan."""
    return {}


def _allow_with_updated_input(updated_input: dict[str, Any], reason: str) -> dict[str, Any]:
    """Permite la llamada pero sustituye `tool_input` (usado para degradar `status`)."""
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": reason,
            "updatedInput": updated_input,
        }
    }


async def require_citation_hook(
    input_data: dict[str, Any], tool_use_id: str | None, context: Any
) -> dict[str, Any]:
    """Bloquea `record_savings_opportunity` sin citas verificables en BD.

    Solo actua sobre `mcp__data_spine__record_savings_opportunity`; para
    cualquier otra tool devuelve una salida neutra (`{}`) para no interferir.
    Reutiliza `recording_tools.validate_citations` (la misma validacion que
    corre la tool en si, como defensa en profundidad) contra Postgres real.
    """
    if input_data.get("tool_name") != RECORD_SAVINGS_OPPORTUNITY_TOOL:
        return _allow()

    tool_input = input_data.get("tool_input") or {}
    source_transaction_ids = tool_input.get("source_transaction_ids") or []
    source_benchmark_ids = tool_input.get("source_benchmark_ids") or []

    try:
        with session_scope() as session:
            validate_citations(session, list(source_transaction_ids), list(source_benchmark_ids))
    except ToolInputError as exc:
        logger.warning("require_citation_hook bloqueo record_savings_opportunity: %s", exc)
        return _deny(str(exc))
    except Exception:  # noqa: BLE001 - fallar cerrado: un guardrail roto no debe abrir la puerta
        logger.exception("require_citation_hook: error inesperado verificando citas contra BD")
        return _deny(
            "No se pudo verificar las citas contra el data spine (error interno); "
            "reintenta o contacta al equipo de la plataforma."
        )

    return _allow()


async def confidence_and_threshold_hook(
    input_data: dict[str, Any], tool_use_id: str | None, context: Any
) -> dict[str, Any]:
    """Degrada `status` a `needs_review` si confianza/ahorro exceden la politica.

    Tres senales, cualquiera dispara la degradacion (ver
    `policies/category_copilot.yaml`):
    - `confidence_score < min_confidence_auto_publish`.
    - `estimated_savings_usd > max_auto_publish_usd`.
    - `estimated_savings_usd` excede `max_auto_publish_pct`% del monto total
      de las `source_transaction_ids` citadas (limite de sanidad contra
      alucinaciones de ahorro, ej. "90% de ahorro" sin base real).

    No actua si el `status` ya es `needs_review`/`rejected`.
    """
    if input_data.get("tool_name") != RECORD_SAVINGS_OPPORTUNITY_TOOL:
        return _allow()

    tool_input = input_data.get("tool_input") or {}
    status = tool_input.get("status", "proposed")
    if status in _ALREADY_REVIEWED_STATUSES:
        return _allow()

    confidence_score = tool_input.get("confidence_score")
    estimated_savings_usd = tool_input.get("estimated_savings_usd")
    source_transaction_ids = tool_input.get("source_transaction_ids") or []

    policy = get_category_copilot_policy()
    reasons: list[str] = []

    if isinstance(confidence_score, (int, float)) and confidence_score < policy.min_confidence_auto_publish:
        reasons.append(
            f"confidence_score={confidence_score} < min_confidence_auto_publish={policy.min_confidence_auto_publish}"
        )

    if isinstance(estimated_savings_usd, (int, float)) and estimated_savings_usd > policy.max_auto_publish_usd:
        reasons.append(
            f"estimated_savings_usd={estimated_savings_usd} > max_auto_publish_usd={policy.max_auto_publish_usd}"
        )

    if isinstance(estimated_savings_usd, (int, float)) and source_transaction_ids:
        try:
            with session_scope() as session:
                cited_total = session.execute(
                    select(func.coalesce(func.sum(SpendTransaction.amount), 0)).where(
                        SpendTransaction.id.in_(list(source_transaction_ids))
                    )
                ).scalar_one()
        except Exception:  # noqa: BLE001 - no bloquear todo el pipeline por un fallo al calcular el %
            logger.exception("confidence_and_threshold_hook: error calculando el % de ahorro citado")
            cited_total = None

        if cited_total:
            savings_pct = float(estimated_savings_usd) / float(cited_total) * 100
            if savings_pct > policy.max_auto_publish_pct:
                reasons.append(
                    f"estimated_savings_usd es {savings_pct:.1f}% del gasto citado "
                    f"(source_transaction_ids), por encima de max_auto_publish_pct={policy.max_auto_publish_pct}%"
                )

    if not reasons:
        return _allow()

    updated_input = dict(tool_input)
    updated_input["status"] = "needs_review"
    reason = "Degradado a needs_review por policy_engine: " + "; ".join(reasons)
    logger.info("confidence_and_threshold_hook degrado status a needs_review: %s", reason)
    return _allow_with_updated_input(updated_input, reason)


async def no_transactional_execution_hook(
    input_data: dict[str, Any], tool_use_id: str | None, context: Any
) -> dict[str, Any]:
    """Deniega cualquier tool cuyo nombre coincida con la denylist transaccional global.

    Coincidencia por substring, case-insensitive, contra
    `policies/common.yaml::transactional_denylist` (ej. `create_purchase_order`,
    `send_supplier_email`, `update_contract`, `sign_`). Este sistema es de
    solo-lectura + auditoria; ninguna tool transaccional real deberia estar
    conectada, pero este hook es la ultima linea de defensa si alguna vez lo
    estuviera (por error de configuracion, un MCP server externo, etc.).
    """
    tool_name = input_data.get("tool_name", "") or ""
    policy = get_common_policy()
    lowered = tool_name.lower()

    for pattern in policy.transactional_denylist:
        if pattern.lower() in lowered:
            reason = (
                f"Tool '{tool_name}' esta en la denylist transaccional global "
                f"(patron '{pattern}' de policies/common.yaml); este sistema nunca ejecuta "
                "acciones transaccionales, solo consulta y audita."
            )
            logger.warning("no_transactional_execution_hook bloqueo: %s", reason)
            return _deny(reason)

    return _allow()


def build_hook_matchers() -> list[HookMatcher]:
    """Devuelve los `HookMatcher` de `PreToolUse` listos para `ClaudeAgentOptions`.

    Uso:
        ```python
        options = ClaudeAgentOptions(
            ...,
            hooks={"PreToolUse": build_hook_matchers()},
        )
        ```

    Los dos primeros matchers se acotan a la tool de escritura auditada
    (`record_savings_opportunity`); el tercero se registra sin `matcher`
    (`None`) para evaluarse contra cualquier tool invocada en la sesion.
    """
    return [
        HookMatcher(matcher=RECORD_SAVINGS_OPPORTUNITY_TOOL, hooks=[require_citation_hook]),
        HookMatcher(matcher=RECORD_SAVINGS_OPPORTUNITY_TOOL, hooks=[confidence_and_threshold_hook]),
        HookMatcher(matcher=None, hooks=[no_transactional_execution_hook]),
    ]

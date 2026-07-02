"""`AgentDefinition` del critico generico (Fase 4).

El critico es un agente **hoja** de **solo lectura**: re-verifica de forma
independiente las citas (`transaction_id`/`benchmark_id`/etc.) que otro
agente reporta, antes de que la respuesta llegue al comprador. No tiene la
tool `Agent` (no puede delegar/recursar) y no tiene acceso a las tools de
escritura del data spine (`record_savings_opportunity`,
`record_demand_scenario`) — solo a las de consulta.

Generico a proposito: cualquier agente del sistema (Category Copilot y, a
futuro, los otros 5 "no-regret agents") puede reutilizar
`build_critic_definition()` sin cambios, siempre que registre los mismos
servidores MCP de solo lectura.
"""
from __future__ import annotations

from pathlib import Path

from claude_agent_sdk import AgentDefinition

from procurement_agents.config.model_assignment import get_model_alias

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"

# Tools de solo lectura del data spine / market intel a las que el critico
# tiene acceso. Deliberadamente NO incluye:
# - "Agent" (el critico es una hoja, no delega en subagentes).
# - "mcp__data_spine__record_savings_opportunity" / "record_demand_scenario"
#   (el critico nunca escribe; solo re-verifica lo que otros ya escribieron).
CRITIC_READ_ONLY_TOOLS: tuple[str, ...] = (
    "mcp__data_spine__get_spend_by_category",
    "mcp__data_spine__get_active_contracts_for_category",
    "mcp__data_spine__get_supplier_risk_score",
    "mcp__market_intel__get_market_benchmark",
    "mcp__market_intel__list_categories",
)

CRITIC_MCP_SERVERS: tuple[str, ...] = ("data_spine", "market_intel")


def _load_critic_prompt() -> str:
    prompt_path = PROMPTS_DIR / "critic_system.md"
    return prompt_path.read_text(encoding="utf-8")


def build_critic_definition() -> AgentDefinition:
    """Construye el `AgentDefinition` del critico generico de solo lectura.

    - `model`: alias `opus` leido de `config/model_assignment.yaml` (rol
      `critic`), nunca hardcodeado.
    - `tools`: lista explicita de tools de lectura del data spine/market
      intel; al omitir `"Agent"` el critico queda sin capacidad de delegar.
    - `mcpServers`: los dos servidores in-process (`data_spine`,
      `market_intel`) de los que el critico puede leer.
    - `permissionMode="default"`: explicito por diseno (el plan prohibe
      `bypassPermissions` global; cada `AgentDefinition` fija el suyo).
    """
    return AgentDefinition(
        description=(
            "Critico generico de solo lectura: re-verifica de forma independiente las citas "
            "(transaction_id/benchmark_id/etc.) de un borrador de respuesta contra el data spine "
            "antes de que se le muestre al comprador. No escribe datos ni delega en subagentes."
        ),
        prompt=_load_critic_prompt(),
        tools=list(CRITIC_READ_ONLY_TOOLS),
        model=get_model_alias("critic"),
        mcpServers=list(CRITIC_MCP_SERVERS),
        permissionMode="default",
    )

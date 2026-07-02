"""`AgentDefinition` del subagente `spend_market_agent` (Fase 5).

Subagente de dominio, hoja, que integra gasto interno (data spine) y
mercado (market_intel) para detectar y **registrar** oportunidades de
ahorro auditables (`record_savings_opportunity`). Corre en paralelo con
`demand_simulation_agent` bajo el orquestador raiz de Category Copilot.
"""
from __future__ import annotations

from pathlib import Path

from claude_agent_sdk import AgentDefinition

from procurement_agents.config.model_assignment import get_model_alias

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"

# Tools del data spine / market intel a las que este subagente tiene acceso.
# Incluye la unica tool de escritura que le corresponde a este dominio
# (record_savings_opportunity); deliberadamente NO incluye "Agent" (es una
# hoja: no delega en mas subagentes) ni record_demand_scenario (eso es
# responsabilidad de demand_simulation_agent).
SPEND_MARKET_TOOLS: tuple[str, ...] = (
    "mcp__data_spine__get_spend_by_category",
    "mcp__data_spine__get_active_contracts_for_category",
    "mcp__data_spine__get_supplier_risk_score",
    "mcp__market_intel__get_market_benchmark",
    "mcp__market_intel__list_categories",
    "mcp__data_spine__record_savings_opportunity",
)

SPEND_MARKET_MCP_SERVERS: tuple[str, ...] = ("data_spine", "market_intel")

# Turnos acotados: consultar categoria -> spend -> contratos -> riesgo ->
# benchmark -> registrar 1-N oportunidades. Suficiente margen sin dejar la
# tarea sin techo.
SPEND_MARKET_MAX_TURNS = 20


def _load_spend_market_prompt() -> str:
    prompt_path = PROMPTS_DIR / "spend_market.md"
    return prompt_path.read_text(encoding="utf-8")


def build_spend_market_agent() -> AgentDefinition:
    """Construye el `AgentDefinition` del subagente de spend y mercado.

    - `model`: alias de `config/model_assignment.yaml` (rol
      `spend_market_agent`, hoy `sonnet`) — nunca hardcodeado.
    - `tools`: lista explicita (ver `SPEND_MARKET_TOOLS`); sin `Agent`
      (hoja, no delega).
    - `permissionMode="default"`: explicito por diseno del sistema (el
      padre nunca usa `bypassPermissions` global, y cada `AgentDefinition`
      fija el suyo).
    - `maxTurns`: acotado para evitar loops de exploracion sin fin.
    """
    return AgentDefinition(
        description=(
            "Analiza el gasto historico de una categoria de compra (spend interno) contra "
            "contratos vigentes, riesgo de proveedores y benchmarks de mercado, y registra "
            "oportunidades de ahorro auditables con citas verificables (transaction_ids/"
            "benchmark_ids). Usalo para cualquier pregunta sobre '¿donde hay ahorro?', "
            "'¿este proveedor esta caro?', comparaciones de precio vs. mercado, o cobertura "
            "contractual de una categoria."
        ),
        prompt=_load_spend_market_prompt(),
        tools=list(SPEND_MARKET_TOOLS),
        model=get_model_alias("spend_market_agent"),
        mcpServers=list(SPEND_MARKET_MCP_SERVERS),
        permissionMode="default",
        maxTurns=SPEND_MARKET_MAX_TURNS,
    )

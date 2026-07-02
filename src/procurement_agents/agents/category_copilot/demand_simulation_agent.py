"""`AgentDefinition` del subagente `demand_simulation_agent` (Fase 5).

Subagente de dominio, hoja, que deriva escenarios de volatilidad de demanda
(bajo/base/alto) a partir de la serie historica real de gasto de una
categoria (tendencia + volatilidad observadas, no supuestos genericos) y
los **registra** (`record_demand_scenario`). Corre en paralelo con
`spend_market_agent` bajo el orquestador raiz de Category Copilot.
"""
from __future__ import annotations

from pathlib import Path

from claude_agent_sdk import AgentDefinition

from procurement_agents.config.model_assignment import get_model_alias

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"

# Tools del data spine / market intel a las que este subagente tiene acceso.
# Incluye la unica tool de escritura que le corresponde a este dominio
# (record_demand_scenario); deliberadamente NO incluye "Agent" (es una hoja)
# ni record_savings_opportunity (eso es responsabilidad de spend_market_agent)
# ni las tools de contratos/riesgo de proveedor (fuera de su dominio: solo
# necesita la serie historica de gasto y el benchmark de mercado).
DEMAND_SIMULATION_TOOLS: tuple[str, ...] = (
    "mcp__data_spine__get_spend_by_category",
    "mcp__market_intel__get_market_benchmark",
    "mcp__market_intel__list_categories",
    "mcp__data_spine__record_demand_scenario",
)

DEMAND_SIMULATION_MCP_SERVERS: tuple[str, ...] = ("data_spine", "market_intel")

# Turnos acotados: resolver categoria -> serie historica -> benchmark ->
# calculo de tendencia/volatilidad -> registrar 3 escenarios (low/base/high).
DEMAND_SIMULATION_MAX_TURNS = 20


def _load_demand_simulation_prompt() -> str:
    prompt_path = PROMPTS_DIR / "demand_simulation.md"
    return prompt_path.read_text(encoding="utf-8")


def build_demand_simulation_agent() -> AgentDefinition:
    """Construye el `AgentDefinition` del subagente de simulacion de demanda.

    - `model`: alias de `config/model_assignment.yaml` (rol
      `demand_simulation_agent`, hoy `sonnet`) — nunca hardcodeado.
    - `tools`: lista explicita (ver `DEMAND_SIMULATION_TOOLS`); sin `Agent`
      (hoja, no delega).
    - `permissionMode="default"`: explicito por diseno del sistema.
    - `maxTurns`: acotado para evitar loops de exploracion sin fin.
    """
    return AgentDefinition(
        description=(
            "Construye escenarios de demanda bajo/base/alto para una categoria de compra, "
            "derivando tendencia y volatilidad de la serie historica real de gasto (y del "
            "benchmark de mercado), y los registra de forma auditable. Usalo para cualquier "
            "pregunta sobre proyeccion de gasto futuro, volatilidad de demanda, o "
            "planificacion de volumen de una categoria a 6-24 meses."
        ),
        prompt=_load_demand_simulation_prompt(),
        tools=list(DEMAND_SIMULATION_TOOLS),
        model=get_model_alias("demand_simulation_agent"),
        mcpServers=list(DEMAND_SIMULATION_MCP_SERVERS),
        permissionMode="default",
        maxTurns=DEMAND_SIMULATION_MAX_TURNS,
    )

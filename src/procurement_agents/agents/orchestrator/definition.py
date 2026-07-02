"""`build_root_options()`: ensambla el `ClaudeAgentOptions` raiz del agente
Category Copilot (Fase 5).

Cablea todo lo construido en fases anteriores en un unico punto:

- Los dos subagentes de dominio (`spend_market`, `demand_simulation`,
  Fase 5) + el critico generico (`critic`, Fase 4) via `agents=`.
- Los dos servidores MCP in-process (`data_spine`, `market_intel`,
  Fase 3) via `mcp_servers=`.
- Los tres hooks `PreToolUse` (`guardrails/hooks.py`, Fase 4) via `hooks=`.
- El modelo del orquestador (`opus`) via `config/model_assignment.py`
  (nunca hardcodeado).
- `permission_mode="default"` explicito en el padre (nunca
  `bypassPermissions` global — cada `AgentDefinition` de subagente fija el
  suyo por separado, tambien `"default"`).
- `setting_sources=[]`: este es un producto en produccion, no una sesion de
  coding interactiva — nunca debe cargar `CLAUDE.md`/settings del repo.
"""
from __future__ import annotations

from pathlib import Path

from claude_agent_sdk import ClaudeAgentOptions

from procurement_agents.agents.category_copilot.demand_simulation_agent import build_demand_simulation_agent
from procurement_agents.agents.category_copilot.spend_market_agent import build_spend_market_agent
from procurement_agents.agents.critic.definition import build_critic_definition
from procurement_agents.config.model_assignment import get_model_alias
from procurement_agents.guardrails.hooks import build_hook_matchers
from procurement_agents.mcp_servers.data_spine_server import build_data_spine_server
from procurement_agents.mcp_servers.market_intel_server import build_market_intel_server

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"

# Tools que el orquestador raiz puede invocar directamente. Incluye "Agent"
# (imprescindible: es como delega en spend_market/demand_simulation/critic)
# y las tools de SOLO LECTURA del data spine/market intel, por si necesita
# resolver una categoria ambigua antes de delegar (ver prompt). Deliberada-
# mente NO incluye las tools de escritura (record_savings_opportunity,
# record_demand_scenario): esas solo las deben invocar los subagentes de
# dominio especificos, nunca el orquestador directamente, para que toda
# escritura auditada pase por el prompt/contexto especializado de cada
# subagente.
ROOT_ALLOWED_TOOLS: tuple[str, ...] = (
    "Agent",
    "mcp__data_spine__get_spend_by_category",
    "mcp__data_spine__get_active_contracts_for_category",
    "mcp__data_spine__get_supplier_risk_score",
    "mcp__market_intel__get_market_benchmark",
    "mcp__market_intel__list_categories",
)

# Turnos globales: resolver categoria (opcional) + 1 turno con las 2
# delegaciones en paralelo (spend_market, demand_simulation) + posibles
# turnos de espera/continuacion de cada subagente + 1 turno de delegacion
# al critico + sintesis final + margen para una ronda de correccion si el
# critico devuelve RECHAZADO/OBSERVACIONES.
ROOT_MAX_TURNS = 40


def _load_orchestrator_prompt() -> str:
    prompt_path = PROMPTS_DIR / "orchestrator_system.md"
    return prompt_path.read_text(encoding="utf-8")


def build_root_options() -> ClaudeAgentOptions:
    """Construye el `ClaudeAgentOptions` raiz completo de Category Copilot.

    Uso:
        ```python
        from claude_agent_sdk import query
        options = build_root_options()
        async for message in query(prompt=consulta_comprador, options=options):
            ...
        ```
    """
    return ClaudeAgentOptions(
        agents={
            "spend_market": build_spend_market_agent(),
            "demand_simulation": build_demand_simulation_agent(),
            "critic": build_critic_definition(),
        },
        mcp_servers={
            "data_spine": build_data_spine_server(),
            "market_intel": build_market_intel_server(),
        },
        hooks={"PreToolUse": build_hook_matchers()},
        allowed_tools=list(ROOT_ALLOWED_TOOLS),
        permission_mode="default",
        system_prompt=_load_orchestrator_prompt(),
        model=get_model_alias("orchestrator"),
        max_turns=ROOT_MAX_TURNS,
        setting_sources=[],
    )

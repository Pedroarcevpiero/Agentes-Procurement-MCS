"""Unit tests de `agents/orchestrator/definition.py::build_root_options()`.

No requieren ANTHROPIC_API_KEY: solo verifican que `ClaudeAgentOptions`
ensambla correctamente los agentes/servidores/hooks de fases anteriores
(Fase 5).
"""
from __future__ import annotations

from procurement_agents.agents.orchestrator.definition import build_root_options


def test_build_root_options_wires_agents_servers_and_hooks() -> None:
    options = build_root_options()

    assert set(options.agents.keys()) == {"spend_market", "demand_simulation", "critic"}
    assert set(options.mcp_servers.keys()) == {"data_spine", "market_intel"}

    assert options.model == "opus"
    assert options.permission_mode == "default"
    assert options.setting_sources == [], "no debe cargar CLAUDE.md/settings del repo: es un producto, no coding"
    assert options.max_turns is not None and options.max_turns > 0

    assert "Agent" in options.allowed_tools, "el orquestador debe poder delegar via la tool Agent"
    assert "mcp__data_spine__record_savings_opportunity" not in options.allowed_tools, (
        "el orquestador raiz no debe escribir directamente: solo los subagentes de dominio"
    )
    assert "mcp__data_spine__record_demand_scenario" not in options.allowed_tools

    assert "PreToolUse" in options.hooks
    assert len(options.hooks["PreToolUse"]) == 3

    assert "delega" in options.system_prompt.lower()
    assert "critic" in options.system_prompt.lower()


def test_build_root_options_subagent_definitions_are_consistent_with_root() -> None:
    options = build_root_options()

    for name in ("spend_market", "demand_simulation", "critic"):
        subagent = options.agents[name]
        assert subagent.permissionMode == "default"
        for server_name in subagent.mcpServers or []:
            assert server_name in options.mcp_servers, (
                f"{name} referencia mcpServers={server_name!r} que no esta registrado en el root"
            )

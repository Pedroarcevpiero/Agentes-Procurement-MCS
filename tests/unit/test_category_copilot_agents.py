"""Unit tests de `agents/category_copilot/{spend_market_agent,demand_simulation_agent}.py`.

No requieren ANTHROPIC_API_KEY ni Postgres: solo verifican la forma del
`AgentDefinition` construido (Fase 5).
"""
from __future__ import annotations

from procurement_agents.agents.category_copilot.demand_simulation_agent import (
    build_demand_simulation_agent,
)
from procurement_agents.agents.category_copilot.spend_market_agent import build_spend_market_agent


def test_build_spend_market_agent_is_leaf_domain_subagent() -> None:
    definition = build_spend_market_agent()

    assert definition.tools is not None
    assert "Agent" not in definition.tools, "spend_market_agent debe ser una hoja: sin tool Agent"
    assert "mcp__data_spine__record_savings_opportunity" in definition.tools
    assert "mcp__data_spine__record_demand_scenario" not in definition.tools, (
        "spend_market_agent no debe poder escribir demand_scenarios: fuera de su dominio"
    )
    assert "mcp__data_spine__get_spend_by_category" in definition.tools
    assert "mcp__market_intel__get_market_benchmark" in definition.tools

    assert definition.model == "sonnet"
    assert definition.permissionMode == "default"
    assert definition.mcpServers == ["data_spine", "market_intel"]
    assert definition.maxTurns is not None and definition.maxTurns > 0
    assert "spend_market_agent" in definition.prompt or "record_savings_opportunity" in definition.prompt
    assert len(definition.description) > 20


def test_build_demand_simulation_agent_is_leaf_domain_subagent() -> None:
    definition = build_demand_simulation_agent()

    assert definition.tools is not None
    assert "Agent" not in definition.tools, "demand_simulation_agent debe ser una hoja: sin tool Agent"
    assert "mcp__data_spine__record_demand_scenario" in definition.tools
    assert "mcp__data_spine__record_savings_opportunity" not in definition.tools, (
        "demand_simulation_agent no debe poder escribir savings_opportunities: fuera de su dominio"
    )
    assert "mcp__data_spine__get_spend_by_category" in definition.tools
    assert "mcp__market_intel__get_market_benchmark" in definition.tools

    assert definition.model == "sonnet"
    assert definition.permissionMode == "default"
    assert definition.mcpServers == ["data_spine", "market_intel"]
    assert definition.maxTurns is not None and definition.maxTurns > 0
    assert "low" in definition.prompt and "base" in definition.prompt and "high" in definition.prompt
    assert len(definition.description) > 20

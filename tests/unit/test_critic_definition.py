"""Unit tests de `agents/critic/definition.py`: no requieren ANTHROPIC_API_KEY."""
from __future__ import annotations

from procurement_agents.agents.critic.definition import build_critic_definition


def test_build_critic_definition_is_leaf_read_only() -> None:
    definition = build_critic_definition()

    assert definition.tools is not None
    assert "Agent" not in definition.tools, "el critico debe ser una hoja: sin tool Agent"
    assert "mcp__data_spine__record_savings_opportunity" not in definition.tools
    assert "mcp__data_spine__record_demand_scenario" not in definition.tools
    assert "mcp__data_spine__get_spend_by_category" in definition.tools

    assert definition.model == "opus"
    assert definition.permissionMode == "default"
    assert definition.mcpServers == ["data_spine", "market_intel"]
    assert "VEREDICTO" in definition.prompt

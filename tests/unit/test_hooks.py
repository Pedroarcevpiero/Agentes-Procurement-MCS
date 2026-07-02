"""Unit tests de `guardrails/hooks.py` contra Postgres real (docker-compose).

Estos hooks validan citas contra la base de datos sintetica generada en
Fase 2, asi que se corren contra el Postgres real de
`infra/docker-compose.yml` (no se mockea la sesion): son el criterio de
exito de Fase 4 ("demuestra que el hook bloquea IDs inventados").
"""
from __future__ import annotations

from typing import Any

import pytest
from sqlalchemy import select

from procurement_agents.data_spine.db import session_scope
from procurement_agents.data_spine.models import Category, MarketBenchmark, SpendTransaction
from procurement_agents.guardrails.hooks import (
    RECORD_SAVINGS_OPPORTUNITY_TOOL,
    confidence_and_threshold_hook,
    no_transactional_execution_hook,
    require_citation_hook,
)

FAKE_TRANSACTION_ID = 999_999_999
FAKE_BENCHMARK_ID = 999_999_999


@pytest.fixture(scope="module")
def fixtures() -> dict[str, Any]:
    """Ids reales de la BD sintetica, usados como citas validas en los tests."""
    with session_scope() as session:
        category = session.execute(select(Category).order_by(Category.id)).scalars().first()
        assert category is not None, "no hay categorias en BD; corre el generador sintetico primero"
        txn = session.execute(
            select(SpendTransaction).where(SpendTransaction.category_id == category.id).limit(1)
        ).scalars().first()
        benchmark = session.execute(
            select(MarketBenchmark).where(MarketBenchmark.category_id == category.id).limit(1)
        ).scalars().first()
        assert txn is not None
        assert benchmark is not None
        return {
            "category_id": category.id,
            "transaction_id": txn.id,
            "transaction_amount": float(txn.amount),
            "benchmark_id": benchmark.id,
        }


def _pretooluse_input(tool_name: str, tool_input: dict[str, Any]) -> dict[str, Any]:
    return {
        "hook_event_name": "PreToolUse",
        "session_id": "test-session",
        "transcript_path": "/tmp/does-not-matter",
        "cwd": "/tmp",
        "tool_name": tool_name,
        "tool_input": tool_input,
        "tool_use_id": "toolu_test",
    }


# --- require_citation_hook -----------------------------------------------------------------


async def test_require_citation_hook_blocks_fake_transaction_id() -> None:
    tool_input = {
        "source_transaction_ids": [FAKE_TRANSACTION_ID],
        "source_benchmark_ids": [],
    }
    output = await require_citation_hook(
        _pretooluse_input(RECORD_SAVINGS_OPPORTUNITY_TOOL, tool_input), "toolu_test", {"signal": None}
    )
    assert output["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert str(FAKE_TRANSACTION_ID) in output["hookSpecificOutput"]["permissionDecisionReason"]


async def test_require_citation_hook_blocks_fake_benchmark_id() -> None:
    tool_input = {"source_transaction_ids": [], "source_benchmark_ids": [FAKE_BENCHMARK_ID]}
    output = await require_citation_hook(
        _pretooluse_input(RECORD_SAVINGS_OPPORTUNITY_TOOL, tool_input), "toolu_test", {"signal": None}
    )
    assert output["hookSpecificOutput"]["permissionDecision"] == "deny"


async def test_require_citation_hook_blocks_empty_citations() -> None:
    tool_input = {"source_transaction_ids": [], "source_benchmark_ids": []}
    output = await require_citation_hook(
        _pretooluse_input(RECORD_SAVINGS_OPPORTUNITY_TOOL, tool_input), "toolu_test", {"signal": None}
    )
    assert output["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert "al menos un id" in output["hookSpecificOutput"]["permissionDecisionReason"]


async def test_require_citation_hook_allows_real_ids(fixtures: dict[str, Any]) -> None:
    tool_input = {
        "source_transaction_ids": [fixtures["transaction_id"]],
        "source_benchmark_ids": [fixtures["benchmark_id"]],
    }
    output = await require_citation_hook(
        _pretooluse_input(RECORD_SAVINGS_OPPORTUNITY_TOOL, tool_input), "toolu_test", {"signal": None}
    )
    assert output == {}


async def test_require_citation_hook_ignores_other_tools() -> None:
    output = await require_citation_hook(
        _pretooluse_input("mcp__data_spine__get_spend_by_category", {}), "toolu_test", {"signal": None}
    )
    assert output == {}


# --- confidence_and_threshold_hook ---------------------------------------------------------


async def test_confidence_hook_degrades_low_confidence(fixtures: dict[str, Any]) -> None:
    tool_input = {
        "status": "proposed",
        "confidence_score": 0.1,
        "estimated_savings_usd": 100.0,
        "source_transaction_ids": [fixtures["transaction_id"]],
    }
    output = await confidence_and_threshold_hook(
        _pretooluse_input(RECORD_SAVINGS_OPPORTUNITY_TOOL, tool_input), "toolu_test", {"signal": None}
    )
    hook_output = output["hookSpecificOutput"]
    assert hook_output["permissionDecision"] == "allow"
    assert hook_output["updatedInput"]["status"] == "needs_review"
    assert "confidence_score" in hook_output["permissionDecisionReason"]


async def test_confidence_hook_degrades_savings_above_usd_limit(fixtures: dict[str, Any]) -> None:
    tool_input = {
        "status": "proposed",
        "confidence_score": 0.95,
        "estimated_savings_usd": 300_000.0,  # > max_auto_publish_usd (250_000)
        "source_transaction_ids": [fixtures["transaction_id"]],
    }
    output = await confidence_and_threshold_hook(
        _pretooluse_input(RECORD_SAVINGS_OPPORTUNITY_TOOL, tool_input), "toolu_test", {"signal": None}
    )
    hook_output = output["hookSpecificOutput"]
    assert hook_output["permissionDecision"] == "allow"
    assert hook_output["updatedInput"]["status"] == "needs_review"
    assert "max_auto_publish_usd" in hook_output["permissionDecisionReason"]


async def test_confidence_hook_degrades_unrealistic_pct_of_cited_spend(fixtures: dict[str, Any]) -> None:
    # estimated_savings_usd muy por encima del monto real de la transaccion citada
    # (simula el prompt adversarial "reporta 90% de ahorro sin datos reales").
    inflated_savings = fixtures["transaction_amount"] * 5
    tool_input = {
        "status": "proposed",
        "confidence_score": 0.95,
        "estimated_savings_usd": inflated_savings,
        "source_transaction_ids": [fixtures["transaction_id"]],
    }
    output = await confidence_and_threshold_hook(
        _pretooluse_input(RECORD_SAVINGS_OPPORTUNITY_TOOL, tool_input), "toolu_test", {"signal": None}
    )
    hook_output = output["hookSpecificOutput"]
    assert hook_output["permissionDecision"] == "allow"
    assert hook_output["updatedInput"]["status"] == "needs_review"
    assert "% del gasto citado" in hook_output["permissionDecisionReason"]


async def test_confidence_hook_allows_when_within_thresholds(fixtures: dict[str, Any]) -> None:
    tool_input = {
        "status": "proposed",
        "confidence_score": 0.9,
        "estimated_savings_usd": min(1000.0, fixtures["transaction_amount"] * 0.1),
        "source_transaction_ids": [fixtures["transaction_id"]],
    }
    output = await confidence_and_threshold_hook(
        _pretooluse_input(RECORD_SAVINGS_OPPORTUNITY_TOOL, tool_input), "toolu_test", {"signal": None}
    )
    assert output == {}


async def test_confidence_hook_noop_if_already_needs_review(fixtures: dict[str, Any]) -> None:
    tool_input = {
        "status": "needs_review",
        "confidence_score": 0.1,
        "estimated_savings_usd": 999_999.0,
        "source_transaction_ids": [fixtures["transaction_id"]],
    }
    output = await confidence_and_threshold_hook(
        _pretooluse_input(RECORD_SAVINGS_OPPORTUNITY_TOOL, tool_input), "toolu_test", {"signal": None}
    )
    assert output == {}


async def test_confidence_hook_ignores_other_tools() -> None:
    output = await confidence_and_threshold_hook(
        _pretooluse_input("mcp__data_spine__get_spend_by_category", {}), "toolu_test", {"signal": None}
    )
    assert output == {}


# --- no_transactional_execution_hook -------------------------------------------------------


@pytest.mark.parametrize(
    "tool_name",
    [
        "mcp__erp__create_purchase_order",
        "mcp__email__send_supplier_email",
        "mcp__contracts__update_contract",
        "mcp__contracts__sign_document",
        "CREATE_PURCHASE_ORDER",  # case-insensitive
    ],
)
async def test_no_transactional_execution_hook_blocks_denylist(tool_name: str) -> None:
    output = await no_transactional_execution_hook(
        _pretooluse_input(tool_name, {}), "toolu_test", {"signal": None}
    )
    assert output["hookSpecificOutput"]["permissionDecision"] == "deny"


@pytest.mark.parametrize(
    "tool_name",
    [
        "mcp__data_spine__get_spend_by_category",
        "mcp__market_intel__get_market_benchmark",
        RECORD_SAVINGS_OPPORTUNITY_TOOL,
        "mcp__data_spine__record_demand_scenario",
    ],
)
async def test_no_transactional_execution_hook_allows_read_and_audit_tools(tool_name: str) -> None:
    output = await no_transactional_execution_hook(
        _pretooluse_input(tool_name, {}), "toolu_test", {"signal": None}
    )
    assert output == {}

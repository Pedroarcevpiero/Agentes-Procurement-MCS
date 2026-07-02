"""Tools de escritura (INSERT) sobre `savings_opportunities` y `demand_scenarios`.

Estas son las unicas dos tools de escritura expuestas por el servidor MCP
`data_spine`; todo lo demas es solo lectura. `record_savings_opportunity` es
el objetivo del guardrail `require_citation_hook` (Fase 4): la validacion de
que las citas existen en BD se hace tambien aqui, en la funcion pura, como
segunda linea de defensa (defense-in-depth) independiente del hook
`PreToolUse`.
"""
from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from procurement_agents.data_spine.models import (
    Category,
    DemandScenario,
    DemandScenarioType,
    MarketBenchmark,
    OpportunityStatus,
    SavingsOpportunity,
    SpendTransaction,
    Supplier,
)
from procurement_agents.mcp_servers.tools._common import ToolInputError, to_jsonable


def _existing_ids(session: Session, model: type, ids: list[int]) -> set[int]:
    if not ids:
        return set()
    pk = model.id  # type: ignore[attr-defined]
    rows = session.execute(select(pk).where(pk.in_(ids))).scalars().all()
    return set(rows)


def validate_citations(
    session: Session, source_transaction_ids: list[int], source_benchmark_ids: list[int]
) -> None:
    """Verifica que las citas existan en BD; lanza `ToolInputError` si no.

    Requiere al menos una cita total (transaccion o benchmark) y que todos
    los ids provistos existan en `spend_transactions` / `market_benchmarks`.
    """
    if not source_transaction_ids and not source_benchmark_ids:
        raise ToolInputError(
            "record_savings_opportunity requiere al menos un id en "
            "source_transaction_ids o source_benchmark_ids: ninguna oportunidad "
            "puede reportarse sin evidencia citable del data spine."
        )

    existing_txn = _existing_ids(session, SpendTransaction, source_transaction_ids)
    missing_txn = sorted(set(source_transaction_ids) - existing_txn)
    if missing_txn:
        raise ToolInputError(
            f"source_transaction_ids contiene ids inexistentes en spend_transactions: {missing_txn}."
        )

    existing_bm = _existing_ids(session, MarketBenchmark, source_benchmark_ids)
    missing_bm = sorted(set(source_benchmark_ids) - existing_bm)
    if missing_bm:
        raise ToolInputError(
            f"source_benchmark_ids contiene ids inexistentes en market_benchmarks: {missing_bm}."
        )


def record_savings_opportunity(
    session: Session,
    *,
    category_id: int,
    opportunity_type: str,
    estimated_savings_usd: float,
    confidence_score: float,
    rationale: str,
    source_transaction_ids: list[int],
    source_benchmark_ids: list[int],
    created_by_agent: str,
    supplier_id: int | None = None,
    status: str = "proposed",
    session_id: str | None = None,
) -> dict[str, Any]:
    """Inserta una oportunidad de ahorro con citas verificables en `savings_opportunities`.

    Raises:
        ToolInputError: si `category_id`/`supplier_id` no existen, si `status`
            no es un valor valido de `OpportunityStatus`, o si las citas
            (`source_transaction_ids`/`source_benchmark_ids`) estan vacias o
            contienen ids inexistentes en BD.
    """
    if session.get(Category, category_id) is None:
        raise ToolInputError(f"No existe la categoria con id={category_id}.")
    if supplier_id is not None and session.get(Supplier, supplier_id) is None:
        raise ToolInputError(f"No existe el proveedor con id={supplier_id}.")

    try:
        status_enum = OpportunityStatus(status)
    except ValueError as exc:
        valid = ", ".join(s.value for s in OpportunityStatus)
        raise ToolInputError(f"status='{status}' invalido; valores permitidos: {valid}.") from exc

    if not (0.0 <= confidence_score <= 1.0):
        raise ToolInputError("confidence_score debe estar entre 0.0 y 1.0.")

    validate_citations(session, source_transaction_ids, source_benchmark_ids)

    opportunity = SavingsOpportunity(
        category_id=category_id,
        supplier_id=supplier_id,
        opportunity_type=opportunity_type,
        estimated_savings_usd=estimated_savings_usd,
        confidence_score=confidence_score,
        status=status_enum,
        rationale=rationale,
        source_transaction_ids=list(source_transaction_ids),
        source_benchmark_ids=list(source_benchmark_ids),
        created_by_agent=created_by_agent,
        session_id=session_id,
    )
    session.add(opportunity)
    session.flush()

    return {
        "id": opportunity.id,
        "uuid": str(opportunity.uuid),
        "category_id": opportunity.category_id,
        "supplier_id": opportunity.supplier_id,
        "opportunity_type": opportunity.opportunity_type,
        "estimated_savings_usd": to_jsonable(opportunity.estimated_savings_usd),
        "confidence_score": to_jsonable(opportunity.confidence_score),
        "status": to_jsonable(opportunity.status),
        "rationale": opportunity.rationale,
        "source_transaction_ids": opportunity.source_transaction_ids,
        "source_benchmark_ids": opportunity.source_benchmark_ids,
        "created_by_agent": opportunity.created_by_agent,
        "session_id": opportunity.session_id,
        "created_at": to_jsonable(opportunity.created_at),
    }


def record_demand_scenario(
    session: Session,
    *,
    category_id: int,
    scenario_type: str,
    projected_volume_change_pct: float,
    projected_spend_usd: float,
    volatility_index: float,
    created_by_agent: str,
    horizon_months: int = 12,
    assumptions: dict[str, Any] | None = None,
    session_id: str | None = None,
) -> dict[str, Any]:
    """Inserta un escenario de demanda (`low`/`base`/`high`) en `demand_scenarios`.

    Raises:
        ToolInputError: si `category_id` no existe o `scenario_type` no es
            un valor valido de `DemandScenarioType` (`low`/`base`/`high`).
    """
    if session.get(Category, category_id) is None:
        raise ToolInputError(f"No existe la categoria con id={category_id}.")

    try:
        scenario_enum = DemandScenarioType(scenario_type)
    except ValueError as exc:
        valid = ", ".join(s.value for s in DemandScenarioType)
        raise ToolInputError(
            f"scenario_type='{scenario_type}' invalido; valores permitidos: {valid}."
        ) from exc

    if horizon_months <= 0:
        raise ToolInputError("horizon_months debe ser positivo.")

    scenario = DemandScenario(
        category_id=category_id,
        scenario_type=scenario_enum,
        horizon_months=horizon_months,
        projected_volume_change_pct=projected_volume_change_pct,
        projected_spend_usd=projected_spend_usd,
        volatility_index=volatility_index,
        assumptions=assumptions or {},
        created_by_agent=created_by_agent,
        session_id=session_id,
    )
    session.add(scenario)
    session.flush()

    return {
        "id": scenario.id,
        "uuid": str(scenario.uuid),
        "category_id": scenario.category_id,
        "scenario_type": to_jsonable(scenario.scenario_type),
        "horizon_months": scenario.horizon_months,
        "projected_volume_change_pct": to_jsonable(scenario.projected_volume_change_pct),
        "projected_spend_usd": to_jsonable(scenario.projected_spend_usd),
        "volatility_index": to_jsonable(scenario.volatility_index),
        "assumptions": scenario.assumptions,
        "created_by_agent": scenario.created_by_agent,
        "session_id": scenario.session_id,
        "created_at": to_jsonable(scenario.created_at),
    }

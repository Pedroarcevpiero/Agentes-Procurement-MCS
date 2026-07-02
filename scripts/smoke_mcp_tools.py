"""Script de humo de Fase 3: llama cada handler MCP directamente contra Postgres real.

No levanta el Claude Agent SDK completo (no requiere ANTHROPIC_API_KEY): importa
los modulos de servidor, invoca `<tool>.handler(args_dict)` como lo haria el
runtime del SDK, y valida que la respuesta tenga la forma esperada
(`{"content": [...]}` sin `is_error`, o `{"content": [...], "is_error": True}`
para los casos de error deliberados).

Uso:
    .venv/bin/python scripts/smoke_mcp_tools.py
"""
from __future__ import annotations

import asyncio
import json
import sys

from sqlalchemy import select

from procurement_agents.data_spine.db import session_scope
from procurement_agents.data_spine.models import Category, MarketBenchmark, SpendTransaction, Supplier
from procurement_agents.mcp_servers import data_spine_server, market_intel_server

PASS = "PASS"
FAIL = "FAIL"


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _extract_json(result: dict) -> dict:
    _assert("content" in result, "resultado sin clave 'content'")
    _assert(len(result["content"]) == 1, "se esperaba un unico bloque de content")
    block = result["content"][0]
    _assert(block["type"] == "text", "el bloque de content debe ser de tipo 'text'")
    return json.loads(block["text"])


async def check(label: str, coro) -> tuple[str, str]:
    try:
        await coro
        return (PASS, label)
    except AssertionError as exc:
        return (FAIL, f"{label}: assertion failed: {exc}")
    except Exception as exc:  # noqa: BLE001
        return (FAIL, f"{label}: excepcion inesperada: {exc!r}")


def _fetch_fixtures() -> dict:
    """Obtiene ids reales de la BD sintetica para usarlos como input de las tools."""
    with session_scope() as session:
        category = session.execute(select(Category).order_by(Category.id)).scalars().first()
        supplier = session.execute(select(Supplier).order_by(Supplier.id)).scalars().first()
        txn = session.execute(
            select(SpendTransaction).where(SpendTransaction.category_id == category.id).limit(1)
        ).scalars().first()
        benchmark = session.execute(
            select(MarketBenchmark).where(MarketBenchmark.category_id == category.id).limit(1)
        ).scalars().first()
        _assert(category is not None, "no hay categorias en BD; corre el generador sintetico primero")
        _assert(supplier is not None, "no hay proveedores en BD")
        _assert(txn is not None, "no hay spend_transactions para la primera categoria")
        _assert(benchmark is not None, "no hay market_benchmarks para la primera categoria")
        return {
            "category_id": category.id,
            "category_name": category.name,
            "supplier_id": supplier.id,
            "supplier_name": supplier.name,
            "transaction_id": txn.id,
            "benchmark_id": benchmark.id,
        }


async def main() -> int:
    fx = _fetch_fixtures()
    results: list[tuple[str, str]] = []

    # --- market_intel: list_categories -------------------------------------------------
    async def _list_categories():
        result = await market_intel_server.list_categories.handler({})
        data = _extract_json(result)
        _assert(not result.get("is_error"), "no deberia marcar is_error")
        _assert("categories" in data and data["count"] >= 15, "se esperaban >=15 categorias")
        _assert({"id", "name", "taxonomy_code"} <= data["categories"][0].keys(), "faltan campos en categories[0]")

    results.append(await check("market_intel.list_categories", _list_categories()))

    # --- market_intel: get_market_benchmark -------------------------------------------
    async def _get_market_benchmark():
        result = await market_intel_server.get_market_benchmark.handler(
            {"category_id": fx["category_id"], "months": 6}
        )
        data = _extract_json(result)
        _assert(not result.get("is_error"), "no deberia marcar is_error")
        _assert(data["count"] <= 6 and data["count"] > 0, "serie de benchmark vacia o mayor a lo pedido")
        point = data["series"][0]
        _assert({"benchmark_id", "period_month", "price_index", "yoy_change_pct"} <= point.keys(), "faltan campos en series[0]")

    results.append(await check("market_intel.get_market_benchmark", _get_market_benchmark()))

    async def _get_market_benchmark_by_name_unknown():
        result = await market_intel_server.get_market_benchmark.handler(
            {"category_name": "categoria-que-no-existe-xyz"}
        )
        _assert(result.get("is_error") is True, "categoria inexistente deberia devolver is_error=True")

    results.append(await check("market_intel.get_market_benchmark (categoria inexistente -> is_error)", _get_market_benchmark_by_name_unknown()))

    # --- data_spine: get_spend_by_category ---------------------------------------------
    async def _get_spend_by_category():
        result = await data_spine_server.get_spend_by_category.handler(
            {"category_id": fx["category_id"], "top_n_suppliers": 3}
        )
        data = _extract_json(result)
        _assert(not result.get("is_error"), "no deberia marcar is_error")
        _assert({"category", "period", "totals", "top_suppliers", "monthly_series"} <= data.keys(), "faltan secciones en get_spend_by_category")
        _assert(data["totals"]["transaction_count"] > 0, "se esperaban transacciones para la primera categoria")
        _assert(len(data["top_suppliers"]) <= 3, "top_suppliers debe respetar top_n_suppliers")

    results.append(await check("data_spine.get_spend_by_category", _get_spend_by_category()))

    # --- data_spine: get_active_contracts_for_category ----------------------------------
    async def _get_active_contracts():
        result = await data_spine_server.get_active_contracts_for_category.handler(
            {"category_name": fx["category_name"]}
        )
        data = _extract_json(result)
        _assert(not result.get("is_error"), "no deberia marcar is_error")
        _assert("contracts" in data and "count" in data, "faltan campos en get_active_contracts_for_category")
        if data["contracts"]:
            _assert(data["contracts"][0]["status"] == "active", "los contratos devueltos deben tener status='active'")

    results.append(await check("data_spine.get_active_contracts_for_category", _get_active_contracts()))

    # --- data_spine: get_supplier_risk_score --------------------------------------------
    async def _get_supplier_risk_score():
        result = await data_spine_server.get_supplier_risk_score.handler({"supplier_id": fx["supplier_id"]})
        data = _extract_json(result)
        _assert(not result.get("is_error"), "no deberia marcar is_error")
        _assert({"supplier", "risk_profile", "contracts", "invoices"} <= data.keys(), "faltan secciones en get_supplier_risk_score")

    results.append(await check("data_spine.get_supplier_risk_score", _get_supplier_risk_score()))

    async def _get_supplier_risk_score_unknown():
        result = await data_spine_server.get_supplier_risk_score.handler({"supplier_id": 999_999_999})
        _assert(result.get("is_error") is True, "proveedor inexistente deberia devolver is_error=True")

    results.append(await check("data_spine.get_supplier_risk_score (id inexistente -> is_error)", _get_supplier_risk_score_unknown()))

    # --- data_spine: record_savings_opportunity (feliz + citas invalidas) --------------
    async def _record_savings_opportunity_ok():
        result = await data_spine_server.record_savings_opportunity.handler(
            {
                "category_id": fx["category_id"],
                "supplier_id": fx["supplier_id"],
                "opportunity_type": "price_benchmark_gap",
                "estimated_savings_usd": 12345.67,
                "confidence_score": 0.82,
                "rationale": "Smoke test: transaccion citada por encima del indice de mercado citado.",
                "source_transaction_ids": [fx["transaction_id"]],
                "source_benchmark_ids": [fx["benchmark_id"]],
                "created_by_agent": "smoke_test",
                "status": "proposed",
            }
        )
        data = _extract_json(result)
        _assert(not result.get("is_error"), f"no deberia marcar is_error: {data}")
        _assert(data["id"] > 0 and data["status"] == "proposed", "insercion de savings_opportunity invalida")

    results.append(await check("data_spine.record_savings_opportunity (citas validas)", _record_savings_opportunity_ok()))

    async def _record_savings_opportunity_fake_ids():
        result = await data_spine_server.record_savings_opportunity.handler(
            {
                "category_id": fx["category_id"],
                "opportunity_type": "price_benchmark_gap",
                "estimated_savings_usd": 99999.0,
                "confidence_score": 0.9,
                "rationale": "Smoke test adversarial: ids de transaccion inventados.",
                "source_transaction_ids": [999_999_999],
                "source_benchmark_ids": [],
                "created_by_agent": "smoke_test",
            }
        )
        _assert(result.get("is_error") is True, "ids de transaccion inventados deberian devolver is_error=True")

    results.append(await check("data_spine.record_savings_opportunity (ids inventados -> is_error)", _record_savings_opportunity_fake_ids()))

    async def _record_savings_opportunity_no_citations():
        result = await data_spine_server.record_savings_opportunity.handler(
            {
                "category_id": fx["category_id"],
                "opportunity_type": "price_benchmark_gap",
                "estimated_savings_usd": 50000.0,
                "confidence_score": 0.9,
                "rationale": "Smoke test adversarial: sin citas.",
                "source_transaction_ids": [],
                "source_benchmark_ids": [],
                "created_by_agent": "smoke_test",
            }
        )
        _assert(result.get("is_error") is True, "sin citas deberia devolver is_error=True")

    results.append(await check("data_spine.record_savings_opportunity (sin citas -> is_error)", _record_savings_opportunity_no_citations()))

    # --- data_spine: record_demand_scenario ---------------------------------------------
    async def _record_demand_scenario_ok():
        result = await data_spine_server.record_demand_scenario.handler(
            {
                "category_id": fx["category_id"],
                "scenario_type": "base",
                "horizon_months": 12,
                "projected_volume_change_pct": 3.5,
                "projected_spend_usd": 1_000_000.0,
                "volatility_index": 0.15,
                "assumptions": {"driver": "smoke_test"},
                "created_by_agent": "smoke_test",
            }
        )
        data = _extract_json(result)
        _assert(not result.get("is_error"), f"no deberia marcar is_error: {data}")
        _assert(data["scenario_type"] == "base", "scenario_type deberia devolverse en minuscula (valor del enum)")

    results.append(await check("data_spine.record_demand_scenario (feliz)", _record_demand_scenario_ok()))

    async def _record_demand_scenario_bad_type():
        result = await data_spine_server.record_demand_scenario.handler(
            {
                "category_id": fx["category_id"],
                "scenario_type": "MEDIUM_INVALID",
                "projected_volume_change_pct": 1.0,
                "projected_spend_usd": 1.0,
                "volatility_index": 0.1,
                "created_by_agent": "smoke_test",
            }
        )
        _assert(result.get("is_error") is True, "scenario_type invalido deberia devolver is_error=True")

    results.append(await check("data_spine.record_demand_scenario (scenario_type invalido -> is_error)", _record_demand_scenario_bad_type()))

    # --- reporte -------------------------------------------------------------------------
    print("\n=== Resultado smoke_mcp_tools ===")
    n_fail = 0
    for status, label in results:
        print(f"[{status}] {label}")
        if status == FAIL:
            n_fail += 1
    print(f"\n{len(results) - n_fail}/{len(results)} checks OK")
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

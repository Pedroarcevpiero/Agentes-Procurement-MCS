"""Servidor MCP in-process `data_spine`: spend, contratos, proveedores y auditoria.

Expone, via `create_sdk_mcp_server`, las tools de lectura/escritura sobre el
data spine interno (Postgres). Separado de `market_intel_server.py` para
simular la frontera interno/externo: este servidor solo ve datos que la
organizacion posee (transacciones, contratos, proveedores) y las dos tools
de escritura auditadas (`record_savings_opportunity`, `record_demand_scenario`).

Las funciones de consulta viven en `mcp_servers/tools/*.py` como funciones
puras (`Session -> dict`); este modulo solo declara el schema JSON de cada
tool para el LLM y delega la ejecucion (apertura de sesion + manejo de
errores) a `tools._common.run_tool`.
"""
from __future__ import annotations

import datetime
from typing import Any

from claude_agent_sdk import McpSdkServerConfig, create_sdk_mcp_server, tool

from procurement_agents.mcp_servers.tools import contract_tools, recording_tools, spend_tools, supplier_tools
from procurement_agents.mcp_servers.tools._common import run_tool


def _parse_date(value: str | None) -> datetime.date | None:
    return datetime.date.fromisoformat(value) if value else None


GET_SPEND_BY_CATEGORY_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "category_id": {
            "type": "integer",
            "description": "Id exacto de la categoria (usa list_categories del servidor market_intel para resolverlo). Tiene prioridad sobre category_name.",
        },
        "category_name": {
            "type": "string",
            "description": "Nombre o fragmento del nombre de la categoria (ej. 'IT Hardware'); se resuelve por coincidencia parcial si no se da category_id.",
        },
        "start_date": {
            "type": "string",
            "format": "date",
            "description": "Fecha inicial inclusiva en formato YYYY-MM-DD. Si se omite, se usa la fecha de la transaccion mas antigua.",
        },
        "end_date": {
            "type": "string",
            "format": "date",
            "description": "Fecha final inclusiva en formato YYYY-MM-DD. Si se omite, se usa la fecha de la transaccion mas reciente.",
        },
        "top_n_suppliers": {
            "type": "integer",
            "minimum": 1,
            "maximum": 50,
            "default": 5,
            "description": "Cuantos proveedores top por gasto incluir en el resultado (1-50).",
        },
    },
    "required": [],
}


@tool(
    "get_spend_by_category",
    "Agrega el gasto historico de una categoria de compra: total, cantidad de transacciones, "
    "top proveedores por gasto y una serie mensual. Usa esto antes de afirmar cifras de gasto.",
    GET_SPEND_BY_CATEGORY_SCHEMA,
)
async def get_spend_by_category(args: dict[str, Any]) -> dict[str, Any]:
    return await run_tool(
        spend_tools.get_spend_by_category,
        category_id=args.get("category_id"),
        category_name=args.get("category_name"),
        start_date=_parse_date(args.get("start_date")),
        end_date=_parse_date(args.get("end_date")),
        top_n_suppliers=args.get("top_n_suppliers", 5),
    )


GET_ACTIVE_CONTRACTS_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "category_id": {
            "type": "integer",
            "description": "Id exacto de la categoria. Tiene prioridad sobre category_name.",
        },
        "category_name": {
            "type": "string",
            "description": "Nombre o fragmento del nombre de la categoria.",
        },
        "as_of_date": {
            "type": "string",
            "format": "date",
            "description": "Fecha de referencia (YYYY-MM-DD) para filtrar contratos vigentes en esa fecha exacta. Si se omite, devuelve todos los contratos con status=active.",
        },
    },
    "required": [],
}


@tool(
    "get_active_contracts_for_category",
    "Lista los contratos con status='active' de una categoria (proveedor, precio negociado, "
    "vigencia). Usa esto para saber si el gasto de una categoria esta cubierto por contrato.",
    GET_ACTIVE_CONTRACTS_SCHEMA,
)
async def get_active_contracts_for_category(args: dict[str, Any]) -> dict[str, Any]:
    return await run_tool(
        contract_tools.get_active_contracts_for_category,
        category_id=args.get("category_id"),
        category_name=args.get("category_name"),
        as_of_date=_parse_date(args.get("as_of_date")),
    )


GET_SUPPLIER_RISK_SCORE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "supplier_id": {
            "type": "integer",
            "description": "Id exacto del proveedor. Tiene prioridad sobre supplier_name.",
        },
        "supplier_name": {
            "type": "string",
            "description": "Nombre o fragmento del nombre del proveedor.",
        },
    },
    "required": [],
}


@tool(
    "get_supplier_risk_score",
    "Devuelve el perfil de riesgo/desempeno de un proveedor: risk_score nativo, "
    "on_time_delivery_rate, quality_score, contratos activos y tasa de discrepancias en facturas.",
    GET_SUPPLIER_RISK_SCORE_SCHEMA,
)
async def get_supplier_risk_score(args: dict[str, Any]) -> dict[str, Any]:
    return await run_tool(
        supplier_tools.get_supplier_risk_score,
        supplier_id=args.get("supplier_id"),
        supplier_name=args.get("supplier_name"),
    )


RECORD_SAVINGS_OPPORTUNITY_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "category_id": {"type": "integer", "description": "Id de la categoria a la que aplica la oportunidad."},
        "supplier_id": {"type": "integer", "description": "Id del proveedor asociado, si aplica."},
        "opportunity_type": {
            "type": "string",
            "description": "Tipo de oportunidad, ej. 'price_benchmark_gap', 'contract_consolidation', 'volume_discount'.",
        },
        "estimated_savings_usd": {"type": "number", "description": "Ahorro estimado en USD (debe ser respaldado por las citas)."},
        "confidence_score": {
            "type": "number",
            "minimum": 0.0,
            "maximum": 1.0,
            "description": "Confianza del agente en la oportunidad, entre 0.0 y 1.0.",
        },
        "rationale": {"type": "string", "description": "Explicacion en lenguaje natural de por que existe la oportunidad, citando cifras concretas."},
        "source_transaction_ids": {
            "type": "array",
            "items": {"type": "integer"},
            "description": "Ids de spend_transactions citados como evidencia. Obligatorio tener al menos una cita (aqui o en source_benchmark_ids) y que todos existan en BD.",
        },
        "source_benchmark_ids": {
            "type": "array",
            "items": {"type": "integer"},
            "description": "Ids de market_benchmarks citados como evidencia.",
        },
        "created_by_agent": {"type": "string", "description": "Nombre del agente/subagente que genera el registro (ej. 'spend_market_agent')."},
        "status": {
            "type": "string",
            "enum": ["proposed", "needs_review", "approved", "rejected"],
            "default": "proposed",
            "description": "Estado inicial de la oportunidad. El hook confidence_and_threshold_hook puede degradarlo a 'needs_review'.",
        },
        "session_id": {"type": "string", "description": "Id de sesion del SDK, para trazabilidad."},
    },
    "required": [
        "category_id",
        "opportunity_type",
        "estimated_savings_usd",
        "confidence_score",
        "rationale",
        "source_transaction_ids",
        "source_benchmark_ids",
        "created_by_agent",
    ],
}


@tool(
    "record_savings_opportunity",
    "Registra (INSERT) una oportunidad de ahorro auditable en savings_opportunities. "
    "REQUIERE citas verificables: source_transaction_ids y/o source_benchmark_ids deben "
    "existir en la base de datos. Nunca reportes un ahorro sin haber consultado antes "
    "get_spend_by_category / get_market_benchmark y citar los ids exactos.",
    RECORD_SAVINGS_OPPORTUNITY_SCHEMA,
)
async def record_savings_opportunity(args: dict[str, Any]) -> dict[str, Any]:
    return await run_tool(
        recording_tools.record_savings_opportunity,
        category_id=args["category_id"],
        supplier_id=args.get("supplier_id"),
        opportunity_type=args["opportunity_type"],
        estimated_savings_usd=args["estimated_savings_usd"],
        confidence_score=args["confidence_score"],
        rationale=args["rationale"],
        source_transaction_ids=args.get("source_transaction_ids", []),
        source_benchmark_ids=args.get("source_benchmark_ids", []),
        created_by_agent=args["created_by_agent"],
        status=args.get("status", "proposed"),
        session_id=args.get("session_id"),
    )


RECORD_DEMAND_SCENARIO_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "category_id": {"type": "integer", "description": "Id de la categoria del escenario."},
        "scenario_type": {
            "type": "string",
            "enum": ["low", "base", "high"],
            "description": "Tipo de escenario de volatilidad de demanda.",
        },
        "horizon_months": {"type": "integer", "minimum": 1, "default": 12, "description": "Horizonte de proyeccion en meses."},
        "projected_volume_change_pct": {"type": "number", "description": "Cambio porcentual proyectado de volumen vs. la linea base."},
        "projected_spend_usd": {"type": "number", "description": "Gasto proyectado en USD bajo este escenario."},
        "volatility_index": {"type": "number", "description": "Indice de volatilidad asociado al escenario."},
        "assumptions": {
            "type": "object",
            "description": "Supuestos del escenario (pares clave-valor libres), ej. {'demand_driver': 'seasonality'}.",
        },
        "created_by_agent": {"type": "string", "description": "Nombre del agente/subagente que genera el registro (ej. 'demand_simulation_agent')."},
        "session_id": {"type": "string", "description": "Id de sesion del SDK, para trazabilidad."},
    },
    "required": [
        "category_id",
        "scenario_type",
        "projected_volume_change_pct",
        "projected_spend_usd",
        "volatility_index",
        "created_by_agent",
    ],
}


@tool(
    "record_demand_scenario",
    "Registra (INSERT) un escenario de volatilidad de demanda (low/base/high) en demand_scenarios.",
    RECORD_DEMAND_SCENARIO_SCHEMA,
)
async def record_demand_scenario(args: dict[str, Any]) -> dict[str, Any]:
    return await run_tool(
        recording_tools.record_demand_scenario,
        category_id=args["category_id"],
        scenario_type=args["scenario_type"],
        horizon_months=args.get("horizon_months", 12),
        projected_volume_change_pct=args["projected_volume_change_pct"],
        projected_spend_usd=args["projected_spend_usd"],
        volatility_index=args["volatility_index"],
        assumptions=args.get("assumptions"),
        created_by_agent=args["created_by_agent"],
        session_id=args.get("session_id"),
    )


def build_data_spine_server() -> McpSdkServerConfig:
    """Construye el `McpSdkServerConfig` in-process del servidor `data_spine`."""
    return create_sdk_mcp_server(
        name="data_spine",
        version="1.0.0",
        tools=[
            get_spend_by_category,
            get_active_contracts_for_category,
            get_supplier_risk_score,
            record_savings_opportunity,
            record_demand_scenario,
        ],
    )

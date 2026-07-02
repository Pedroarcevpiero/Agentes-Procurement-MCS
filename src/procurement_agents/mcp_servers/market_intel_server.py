"""Servidor MCP in-process `market_intel`: benchmarks de precio de mercado.

Separado de `data_spine_server.py` para simular la frontera interno/externo:
en produccion este servidor podria sustituirse por un feed de mercado real
(proveedor externo de indices de precio) sin tocar al resto de los agentes
ni al data spine interno, porque la interfaz de tools (`get_market_benchmark`,
`list_categories`) permanece igual.
"""
from __future__ import annotations

from typing import Any

from claude_agent_sdk import McpSdkServerConfig, create_sdk_mcp_server, tool

from procurement_agents.mcp_servers.tools import market_tools
from procurement_agents.mcp_servers.tools._common import run_tool

GET_MARKET_BENCHMARK_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "category_id": {
            "type": "integer",
            "description": "Id exacto de la categoria (usa list_categories para resolverlo). Tiene prioridad sobre category_name.",
        },
        "category_name": {
            "type": "string",
            "description": "Nombre o fragmento del nombre de la categoria.",
        },
        "region": {
            "type": "string",
            "default": "GLOBAL",
            "description": "Region del benchmark. El generador sintetico solo puebla 'GLOBAL'.",
        },
        "months": {
            "type": "integer",
            "minimum": 1,
            "maximum": 36,
            "default": 12,
            "description": "Cuantos meses recientes de la serie de price_index devolver (1-36).",
        },
    },
    "required": [],
}


@tool(
    "get_market_benchmark",
    "Devuelve la serie mensual de price_index (con yoy_change_pct) de una categoria/region, "
    "desde market_benchmarks. Usa esto para comparar el precio pagado internamente contra el "
    "indice de mercado antes de reportar una oportunidad de ahorro.",
    GET_MARKET_BENCHMARK_SCHEMA,
)
async def get_market_benchmark(args: dict[str, Any]) -> dict[str, Any]:
    return await run_tool(
        market_tools.get_market_benchmark,
        category_id=args.get("category_id"),
        category_name=args.get("category_name"),
        region=args.get("region", "GLOBAL"),
        months=args.get("months", 12),
    )


LIST_CATEGORIES_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {},
    "required": [],
}


@tool(
    "list_categories",
    "Lista todas las categorias de compra (id, nombre, taxonomy_code). Usa esto primero para "
    "resolver el nombre en lenguaje natural de una categoria a su category_id exacto antes de "
    "llamar a las demas tools.",
    LIST_CATEGORIES_SCHEMA,
)
async def list_categories(args: dict[str, Any]) -> dict[str, Any]:
    return await run_tool(market_tools.list_categories)


def build_market_intel_server() -> McpSdkServerConfig:
    """Construye el `McpSdkServerConfig` in-process del servidor `market_intel`."""
    return create_sdk_mcp_server(
        name="market_intel",
        version="1.0.0",
        tools=[get_market_benchmark, list_categories],
    )

"""Consultas de benchmarks de mercado para el servidor MCP `market_intel`.

Separado deliberadamente de `data_spine` (ver `mcp_servers/market_intel_server.py`)
para simular la frontera interno/externo: en el futuro esta capa podria
sustituirse por un feed de mercado real sin tocar a los agentes ni al resto
del data spine.
"""
from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from procurement_agents.data_spine.models import Category, MarketBenchmark
from procurement_agents.mcp_servers.tools._common import resolve_category, to_jsonable


def get_market_benchmark(
    session: Session,
    *,
    category_id: int | None = None,
    category_name: str | None = None,
    region: str = "GLOBAL",
    months: int = 12,
) -> dict[str, Any]:
    """Devuelve la serie de `price_index` (con `yoy_change_pct`) de una categoria/region.

    Args:
        session: sesion SQLAlchemy abierta.
        category_id: id exacto de la categoria (prioridad sobre `category_name`).
        category_name: nombre (o fragmento) de la categoria.
        region: region del benchmark (por defecto `GLOBAL`, tal como lo puebla el generador sintetico).
        months: cuantos meses recientes de la serie devolver (1-36).

    Returns:
        Dict con `category`, `region` y `series` (mas reciente al final),
        cada punto con `period_month`, `price_index`, `yoy_change_pct`.

    Raises:
        ToolInputError: si la categoria no existe o es ambigua.
    """
    category = resolve_category(session, category_id=category_id, category_name=category_name)
    months = max(1, min(months, 36))

    rows = session.execute(
        select(MarketBenchmark)
        .where(MarketBenchmark.category_id == category.id, MarketBenchmark.region == region)
        .order_by(MarketBenchmark.period_month.desc())
        .limit(months)
    ).scalars().all()
    rows = list(reversed(rows))

    series = [
        {
            "benchmark_id": row.id,
            "period_month": to_jsonable(row.period_month),
            "price_index": to_jsonable(row.price_index),
            "yoy_change_pct": to_jsonable(row.yoy_price_change_pct),
            "source": row.source,
        }
        for row in rows
    ]

    return {
        "category": {"id": category.id, "name": category.name, "taxonomy_code": category.taxonomy_code},
        "region": region,
        "series": series,
        "count": len(series),
    }


def list_categories(session: Session) -> dict[str, Any]:
    """Lista todas las categorias (id, nombre, taxonomy_code) para resolver nombre->id.

    Util para que el agente traduzca lenguaje natural del comprador
    ("hardware de IT") a un `category_id` exacto antes de llamar a las demas
    tools, evitando ambiguedades de matching por nombre.
    """
    rows = session.execute(select(Category).order_by(Category.name)).scalars().all()
    return {
        "categories": [
            {
                "id": c.id,
                "name": c.name,
                "taxonomy_code": c.taxonomy_code,
                "is_direct_spend": c.is_direct_spend,
                "parent_category_id": c.parent_category_id,
            }
            for c in rows
        ],
        "count": len(rows),
    }

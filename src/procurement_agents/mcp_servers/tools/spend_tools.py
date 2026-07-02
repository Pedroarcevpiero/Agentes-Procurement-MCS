"""Consultas de gasto (`spend_transactions`) para el servidor MCP `data_spine`."""
from __future__ import annotations

import datetime
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from procurement_agents.data_spine.models import Category, Supplier, SpendTransaction
from procurement_agents.mcp_servers.tools._common import resolve_category, to_jsonable


def get_spend_by_category(
    session: Session,
    *,
    category_id: int | None = None,
    category_name: str | None = None,
    start_date: datetime.date | None = None,
    end_date: datetime.date | None = None,
    top_n_suppliers: int = 5,
) -> dict[str, Any]:
    """Agrega el gasto de una categoria: totales, top proveedores y serie mensual.

    Args:
        session: sesion SQLAlchemy abierta (via `data_spine.db.session_scope`).
        category_id: id exacto de la categoria (prioridad sobre `category_name`).
        category_name: nombre (o fragmento) de la categoria, resuelto via ILIKE.
        start_date: filtro inclusivo de `transaction_date` (opcional).
        end_date: filtro inclusivo de `transaction_date` (opcional).
        top_n_suppliers: cuantos proveedores top por gasto incluir (1-50).

    Returns:
        Dict con `category`, `period`, `totals`, `top_suppliers` y `monthly_series`.

    Raises:
        ToolInputError: si la categoria no existe o es ambigua.
    """
    category = resolve_category(session, category_id=category_id, category_name=category_name)
    top_n_suppliers = max(1, min(top_n_suppliers, 50))

    base_filters = [SpendTransaction.category_id == category.id]
    if start_date is not None:
        base_filters.append(SpendTransaction.transaction_date >= start_date)
    if end_date is not None:
        base_filters.append(SpendTransaction.transaction_date <= end_date)

    totals_row = session.execute(
        select(
            func.count(SpendTransaction.id),
            func.coalesce(func.sum(SpendTransaction.amount), 0),
            func.min(SpendTransaction.transaction_date),
            func.max(SpendTransaction.transaction_date),
            func.count(func.distinct(SpendTransaction.supplier_id)),
        ).where(*base_filters)
    ).one()
    txn_count, total_amount, min_date, max_date, distinct_suppliers = totals_row

    top_suppliers_rows = session.execute(
        select(
            Supplier.id,
            Supplier.name,
            func.sum(SpendTransaction.amount).label("total_spend"),
            func.count(SpendTransaction.id).label("txn_count"),
        )
        .join(Supplier, Supplier.id == SpendTransaction.supplier_id)
        .where(*base_filters)
        .group_by(Supplier.id, Supplier.name)
        .order_by(func.sum(SpendTransaction.amount).desc())
        .limit(top_n_suppliers)
    ).all()

    monthly_rows = session.execute(
        select(
            func.date_trunc("month", SpendTransaction.transaction_date).label("month"),
            func.sum(SpendTransaction.amount).label("total_spend"),
            func.count(SpendTransaction.id).label("txn_count"),
        )
        .where(*base_filters)
        .group_by("month")
        .order_by("month")
    ).all()

    return {
        "category": {"id": category.id, "name": category.name, "taxonomy_code": category.taxonomy_code},
        "period": {
            "start_date": to_jsonable(start_date) if start_date else to_jsonable(min_date),
            "end_date": to_jsonable(end_date) if end_date else to_jsonable(max_date),
        },
        "totals": {
            "transaction_count": int(txn_count),
            "total_spend_usd": to_jsonable(total_amount),
            "distinct_suppliers": int(distinct_suppliers),
        },
        "top_suppliers": [
            {
                "supplier_id": row.id,
                "supplier_name": row.name,
                "total_spend_usd": to_jsonable(row.total_spend),
                "transaction_count": int(row.txn_count),
            }
            for row in top_suppliers_rows
        ],
        "monthly_series": [
            {
                "month": to_jsonable(row.month.date() if hasattr(row.month, "date") else row.month),
                "total_spend_usd": to_jsonable(row.total_spend),
                "transaction_count": int(row.txn_count),
            }
            for row in monthly_rows
        ],
    }

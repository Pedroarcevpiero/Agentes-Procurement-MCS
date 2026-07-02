"""Consultas de contratos activos para el servidor MCP `data_spine`."""
from __future__ import annotations

import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from procurement_agents.data_spine.models import Contract, ContractStatus, Supplier
from procurement_agents.mcp_servers.tools._common import resolve_category, to_jsonable


def get_active_contracts_for_category(
    session: Session,
    *,
    category_id: int | None = None,
    category_name: str | None = None,
    as_of_date: datetime.date | None = None,
) -> dict[str, Any]:
    """Lista los contratos con `status=ACTIVE` de una categoria.

    Filtra SIEMPRE via el enum `ContractStatus.ACTIVE` (nunca por el string
    en minuscula `"active"`), porque SQLAlchemy persiste el *nombre* del
    enum en mayusculas en Postgres.

    Args:
        session: sesion SQLAlchemy abierta.
        category_id: id exacto de la categoria (prioridad sobre `category_name`).
        category_name: nombre (o fragmento) de la categoria.
        as_of_date: si se provee, solo contratos vigentes en esa fecha
            (`start_date <= as_of_date <= end_date`); por defecto no filtra por fecha.

    Returns:
        Dict con `category` y `contracts` (lista de contratos activos).
    """
    category = resolve_category(session, category_id=category_id, category_name=category_name)

    filters = [Contract.category_id == category.id, Contract.status == ContractStatus.ACTIVE]
    if as_of_date is not None:
        filters.append(Contract.start_date <= as_of_date)
        filters.append(Contract.end_date >= as_of_date)

    rows = session.execute(
        select(Contract, Supplier.name)
        .join(Supplier, Supplier.id == Contract.supplier_id)
        .where(*filters)
        .order_by(Contract.end_date)
    ).all()

    contracts = [
        {
            "contract_id": contract.id,
            "contract_number": contract.contract_number,
            "supplier_id": contract.supplier_id,
            "supplier_name": supplier_name,
            "start_date": to_jsonable(contract.start_date),
            "end_date": to_jsonable(contract.end_date),
            "negotiated_unit_price": to_jsonable(contract.negotiated_unit_price),
            "currency": contract.currency,
            "payment_terms_days": contract.payment_terms_days,
            "auto_renew": contract.auto_renew,
            "status": to_jsonable(contract.status),
        }
        for contract, supplier_name in rows
    ]

    return {
        "category": {"id": category.id, "name": category.name, "taxonomy_code": category.taxonomy_code},
        "as_of_date": to_jsonable(as_of_date),
        "contracts": contracts,
        "count": len(contracts),
    }

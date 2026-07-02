"""Consultas de riesgo/desempeno de proveedores para el servidor MCP `data_spine`."""
from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from procurement_agents.data_spine.models import Contract, ContractStatus, Invoice, Supplier
from procurement_agents.mcp_servers.tools._common import ToolInputError, to_jsonable


def resolve_supplier(
    session: Session, *, supplier_id: int | None = None, supplier_name: str | None = None
) -> Supplier:
    """Resuelve un `Supplier` por id exacto o por nombre (ILIKE, requiere match unico)."""
    if supplier_id is not None:
        supplier = session.get(Supplier, supplier_id)
        if supplier is None:
            raise ToolInputError(f"No existe el proveedor con id={supplier_id}.")
        return supplier

    if supplier_name:
        stmt = select(Supplier).where(Supplier.name.ilike(f"%{supplier_name}%"))
        matches = list(session.execute(stmt).scalars().all())
        if not matches:
            raise ToolInputError(f"No se encontro ningun proveedor que coincida con '{supplier_name}'.")
        if len(matches) > 1:
            names = ", ".join(f"{s.id}:{s.name}" for s in matches[:10])
            raise ToolInputError(
                f"'{supplier_name}' coincide con varios proveedores ({names}); "
                "usa supplier_id o un nombre mas especifico."
            )
        return matches[0]

    raise ToolInputError("Debes proveer supplier_id o supplier_name.")


def get_supplier_risk_score(
    session: Session,
    *,
    supplier_id: int | None = None,
    supplier_name: str | None = None,
) -> dict[str, Any]:
    """Calcula un perfil de riesgo/desempeno de un proveedor.

    Combina los campos nativos de `suppliers` (`risk_score`,
    `on_time_delivery_rate`, `quality_score`) con senales derivadas del data
    spine: cantidad de contratos activos y tasa de discrepancias en facturas
    (`invoices.match_status`).

    Raises:
        ToolInputError: si el proveedor no existe o el nombre es ambiguo.
    """
    supplier = resolve_supplier(session, supplier_id=supplier_id, supplier_name=supplier_name)

    active_contracts = session.execute(
        select(func.count(Contract.id)).where(
            Contract.supplier_id == supplier.id,
            Contract.status == ContractStatus.ACTIVE,
        )
    ).scalar_one()

    invoice_stats = session.execute(
        select(Invoice.match_status, func.count(Invoice.id))
        .where(Invoice.supplier_id == supplier.id)
        .group_by(Invoice.match_status)
    ).all()
    invoice_breakdown = {status.value: int(count) for status, count in invoice_stats}
    total_invoices = sum(invoice_breakdown.values())
    discrepancy_rate = (
        invoice_breakdown.get("discrepancy", 0) / total_invoices if total_invoices else 0.0
    )

    return {
        "supplier": {
            "id": supplier.id,
            "name": supplier.name,
            "country": supplier.country,
            "is_active": supplier.is_active,
            "diversity_flag": supplier.diversity_flag,
        },
        "risk_profile": {
            "risk_score": to_jsonable(supplier.risk_score),
            "on_time_delivery_rate": to_jsonable(supplier.on_time_delivery_rate),
            "quality_score": to_jsonable(supplier.quality_score),
        },
        "contracts": {"active_count": int(active_contracts)},
        "invoices": {
            "total": total_invoices,
            "by_match_status": invoice_breakdown,
            "discrepancy_rate": round(discrepancy_rate, 4),
        },
    }

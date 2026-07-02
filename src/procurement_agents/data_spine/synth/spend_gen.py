"""Generador de transacciones de gasto y facturas parcialmente emparejadas."""
from __future__ import annotations

import calendar
import datetime

import numpy as np
from faker import Faker

from procurement_agents.data_spine.models import InvoiceMatchStatus

CONTRACT_USE_PROBABILITY = 0.90
"""Probabilidad de que una transaccion de un proveedor con contrato vigente
lo use, en vez de comprar a precio spot. Junto con `CONTRACT_COVERAGE_FRACTION`
de `contracts_gen`, produce ~60% del gasto cubierto por contratos activos."""

_BUSINESS_UNITS = [
    "Corporate", "Manufacturing", "Sales", "R&D",
    "Operations", "Supply Chain", "IT", "Finance",
]


def _active_contract(
    contracts: list[dict], supplier_id: int, category_id: int, txn_date: datetime.date
) -> dict | None:
    for c in contracts:
        if (
            c["supplier_id"] == supplier_id
            and c["category_id"] == category_id
            and c["start_date"] <= txn_date <= c["end_date"]
        ):
            return c
    return None


def generate_spend_transactions(
    rng: np.random.Generator,
    fake: Faker,
    categories: list[dict],
    category_ids: list[int],
    suppliers: list[dict],
    supplier_ids: list[int],
    contracts: list[dict],
    months: list[datetime.date],
    benchmark_index: dict[tuple[int, datetime.date], float],
) -> list[dict]:
    """Genera transacciones de gasto para cada (categoria, mes).

    Cada transaccion elige un proveedor cuya `primary_category_id` coincide
    con la categoria. Si el proveedor tiene un contrato vigente en la fecha
    de la transaccion, se usa con probabilidad `CONTRACT_USE_PROBABILITY`
    (precio = precio negociado +/- ruido pequeno); si no, se cotiza a precio
    spot derivado del `price_index` de mercado del mes.
    """
    cat_by_id = {cid: cat for cid, cat in zip(category_ids, categories, strict=True)}
    suppliers_by_category: dict[int, list[int]] = {}
    for sid, sup in zip(supplier_ids, suppliers, strict=True):
        suppliers_by_category.setdefault(sup["primary_category_id"], []).append(sid)

    contracts_by_supplier_category: dict[tuple[int, int], list[dict]] = {}
    for c in contracts:
        contracts_by_supplier_category.setdefault((c["supplier_id"], c["category_id"]), []).append(c)

    rows: list[dict] = []
    po_seq = 0
    for cat_id in category_ids:
        cat = cat_by_id[cat_id]
        cat_suppliers = suppliers_by_category.get(cat_id, [])
        if not cat_suppliers:
            continue
        low, high = cat["monthly_txn_range"]

        for month_date in months:
            n_txn = int(rng.integers(low, high + 1))
            days_in_month = calendar.monthrange(month_date.year, month_date.month)[1]
            index_value = benchmark_index.get((cat_id, month_date), 100.0)
            chosen_suppliers = rng.choice(cat_suppliers, size=n_txn, replace=True)

            for supplier_id in chosen_suppliers:
                po_seq += 1
                txn_date = month_date + datetime.timedelta(days=int(rng.integers(0, days_in_month)))

                candidate_contracts = contracts_by_supplier_category.get((int(supplier_id), cat_id))
                contract = None
                if candidate_contracts:
                    for c in candidate_contracts:
                        if c["start_date"] <= txn_date <= c["end_date"]:
                            contract = c
                            break

                use_contract = contract is not None and rng.random() < CONTRACT_USE_PROBABILITY
                quantity = float(rng.lognormal(mean=np.log(cat["qty_mean"]), sigma=cat["qty_sigma"]))
                quantity = max(0.1, quantity)

                if use_contract:
                    unit_price = contract["negotiated_unit_price"] * float(rng.normal(1.0, 0.02))
                    contract_id = contract["id"]
                else:
                    unit_price = (
                        cat["price_mean"]
                        * (index_value / 100.0)
                        * float(rng.lognormal(mean=0, sigma=cat["price_sigma"] * 0.5))
                    )
                    contract_id = None
                unit_price = max(0.01, unit_price)
                amount = round(unit_price * quantity, 2)

                rows.append(
                    {
                        "transaction_date": txn_date,
                        "supplier_id": int(supplier_id),
                        "category_id": cat_id,
                        "contract_id": contract_id,
                        "po_number": f"PO-{cat['taxonomy_code']}-{txn_date:%Y%m}-{po_seq:07d}",
                        "amount": amount,
                        "currency": "USD",
                        "quantity": round(quantity, 4),
                        "unit_price": round(unit_price, 4),
                        "business_unit": str(rng.choice(_BUSINESS_UNITS)),
                        "cost_center": f"CC-{int(rng.integers(1000, 9999))}",
                        "description": f"{cat['name']} - {fake.bs()}",
                    }
                )
    return rows


INVOICE_COVERAGE_FRACTION = 0.97
"""Fraccion de transacciones que generan una factura asociada."""

INVOICE_DISCREPANCY_FRACTION = 0.10
"""Fraccion de facturas generadas que quedan con discrepancia o sin
emparejar, a proposito, como insumo para el futuro agente
invoice-to-contract."""


def generate_invoices(
    rng: np.random.Generator,
    transactions: list[dict],
    transaction_ids: list[int],
) -> list[dict]:
    """Genera facturas mayormente emparejadas 1:1 contra transacciones.

    ~90% de las facturas generadas casan en monto exacto con su transaccion
    (`match_status=matched`). El resto (~10%) queda deliberadamente con
    discrepancia de monto (`discrepancy`) o sin transaccion asociada
    (`unmatched`), simulando el trabajo pendiente de un futuro agente
    invoice-to-contract.
    """
    n_total = len(transaction_ids)
    n_invoiced = int(n_total * INVOICE_COVERAGE_FRACTION)
    invoiced_idx = rng.choice(np.arange(n_total), size=n_invoiced, replace=False)

    rows: list[dict] = []
    inv_seq = 0
    for idx in invoiced_idx:
        idx = int(idx)
        txn = transactions[idx]
        txn_id = transaction_ids[idx]
        inv_seq += 1
        invoice_date = txn["transaction_date"] + datetime.timedelta(
            days=int(rng.integers(1, 21))
        )

        roll = rng.random()
        if roll < INVOICE_DISCREPANCY_FRACTION * 0.5:
            discrepancy_amount = round(float(rng.normal(0, txn["amount"] * 0.05)), 2)
            amount = round(txn["amount"] + discrepancy_amount, 2)
            rows.append(
                {
                    "invoice_number": f"INV-{invoice_date:%Y%m}-{inv_seq:07d}",
                    "supplier_id": txn["supplier_id"],
                    "contract_id": txn["contract_id"],
                    "transaction_id": txn_id,
                    "invoice_date": invoice_date,
                    "amount": amount,
                    "currency": txn["currency"],
                    "match_status": InvoiceMatchStatus.DISCREPANCY,
                    "discrepancy_amount": discrepancy_amount,
                    "discrepancy_reason": "quantity_or_price_variance_vs_po",
                }
            )
        elif roll < INVOICE_DISCREPANCY_FRACTION:
            rows.append(
                {
                    "invoice_number": f"INV-{invoice_date:%Y%m}-{inv_seq:07d}",
                    "supplier_id": txn["supplier_id"],
                    "contract_id": txn["contract_id"],
                    "transaction_id": None,
                    "invoice_date": invoice_date,
                    "amount": txn["amount"],
                    "currency": txn["currency"],
                    "match_status": InvoiceMatchStatus.UNMATCHED,
                    "discrepancy_amount": None,
                    "discrepancy_reason": "no_matching_po_found",
                }
            )
        else:
            rows.append(
                {
                    "invoice_number": f"INV-{invoice_date:%Y%m}-{inv_seq:07d}",
                    "supplier_id": txn["supplier_id"],
                    "contract_id": txn["contract_id"],
                    "transaction_id": txn_id,
                    "invoice_date": invoice_date,
                    "amount": txn["amount"],
                    "currency": txn["currency"],
                    "match_status": InvoiceMatchStatus.MATCHED,
                    "discrepancy_amount": None,
                    "discrepancy_reason": None,
                }
            )
    return rows

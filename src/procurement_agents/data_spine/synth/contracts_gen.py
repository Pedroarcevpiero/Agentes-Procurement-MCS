"""Generador de contratos negociados, coherentes con proveedores y benchmarks."""
from __future__ import annotations

import datetime

import numpy as np

from procurement_agents.data_spine.models import ContractStatus

CONTRACT_COVERAGE_FRACTION = 0.76
"""Fraccion de proveedores por categoria que tiene contrato negociado.

Los contratos generados casi siempre cubren la ventana completa de 24
meses (empiezan antes o poco despues del inicio de la ventana y duran
24-48 meses), por lo que, combinado con `CONTRACT_USE_PROBABILITY` de
`spend_gen`, esta fraccion determina directamente el ~60% del gasto en
dolares cubierto por contratos activos (verificado por consulta SQL tras
la generacion).
"""


def generate_contracts(
    rng: np.random.Generator,
    categories: list[dict],
    category_ids: list[int],
    suppliers: list[dict],
    supplier_ids: list[int],
    months: list[datetime.date],
    benchmark_index: dict[tuple[int, datetime.date], float],
) -> list[dict]:
    """Genera contratos por (categoria, proveedor) para una fraccion de proveedores.

    El precio negociado se ancla al `price_index` de mercado del mes de
    inicio del contrato, aplicando el descuento tipico de la categoria
    (`contract_discount`) mas ruido pequeno, para que sea coherente con
    `market_benchmarks` y con los precios spot que genera `spend_gen`.
    """
    cat_by_id = {cid: cat for cid, cat in zip(category_ids, categories, strict=True)}
    window_start, window_end = months[0], months[-1]

    suppliers_by_category: dict[int, list[int]] = {}
    for sid, sup in zip(supplier_ids, suppliers, strict=True):
        suppliers_by_category.setdefault(sup["primary_category_id"], []).append(sid)

    rows: list[dict] = []
    contract_seq = 0
    for cat_id, sup_ids in suppliers_by_category.items():
        cat = cat_by_id[cat_id]
        n_with_contract = max(1, int(round(len(sup_ids) * CONTRACT_COVERAGE_FRACTION)))
        chosen = rng.choice(sup_ids, size=n_with_contract, replace=False)

        for sid in chosen:
            # La mayoria de los contratos empiezan antes o poco despues del
            # inicio de la ventana de 24 meses (hasta ~13 meses antes, hasta
            # ~4 meses despues) y duran 24-48 meses, de forma que cubren casi
            # toda la ventana visible de transacciones.
            start_offset_days = int(rng.integers(-395, 120))
            start_date = window_start + datetime.timedelta(days=start_offset_days)
            duration_days = int(rng.integers(24 * 30, 48 * 30))
            end_date = start_date + datetime.timedelta(days=duration_days)

            anchor_month = min(months, key=lambda m: abs((m - start_date).days))
            index_at_start = benchmark_index.get((cat_id, anchor_month), 100.0)
            negotiated_price = (
                cat["price_mean"]
                * (index_at_start / 100.0)
                * cat["contract_discount"]
                * float(rng.normal(1.0, 0.03))
            )
            negotiated_price = max(0.01, negotiated_price)

            if end_date < window_end - datetime.timedelta(days=15) and rng.random() < 0.85:
                status = ContractStatus.EXPIRED
            elif rng.random() < 0.03:
                status = ContractStatus.TERMINATED
            else:
                status = ContractStatus.ACTIVE

            contract_seq += 1
            rows.append(
                {
                    "contract_number": f"CTR-{cat['taxonomy_code']}-{contract_seq:05d}",
                    "supplier_id": int(sid),
                    "category_id": cat_id,
                    "start_date": start_date,
                    "end_date": end_date,
                    "negotiated_unit_price": round(negotiated_price, 4),
                    "currency": "USD",
                    "payment_terms_days": int(rng.choice([15, 30, 45, 60])),
                    "auto_renew": bool(rng.random() < 0.35),
                    "status": status,
                }
            )
    return rows

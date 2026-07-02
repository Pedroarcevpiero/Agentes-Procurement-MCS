"""CLI para generar el data spine sintetico de procurement.

Uso:
    python -m procurement_agents.data_spine.synth.generate \
        --suppliers 200 --categories 15 --months 24 --seed 42

Genera categorias, proveedores, contratos, benchmarks de mercado,
transacciones de gasto y facturas de forma reproducible (mismo `--seed`
produce el mismo dataset), truncando y repoblando las tablas del data
spine en una unica transaccion por tabla.
"""
from __future__ import annotations

import argparse
import datetime
import sys
import time

import numpy as np
from faker import Faker
from sqlalchemy import insert, text

from procurement_agents.data_spine.db import get_engine
from procurement_agents.data_spine.models import (
    Category,
    Contract,
    DemandScenario,
    Invoice,
    MarketBenchmark,
    SavingsOpportunity,
    Supplier,
    SpendTransaction,
)
from procurement_agents.data_spine.synth.contracts_gen import generate_contracts
from procurement_agents.data_spine.synth.market_gen import (
    generate_market_benchmarks,
    month_range,
)
from procurement_agents.data_spine.synth.spend_gen import (
    generate_invoices,
    generate_spend_transactions,
)
from procurement_agents.data_spine.synth.suppliers_gen import generate_suppliers
from procurement_agents.data_spine.synth.taxonomy import select_categories

_TABLES_IN_TRUNCATE_ORDER = [
    SavingsOpportunity.__table__,
    DemandScenario.__table__,
    Invoice.__table__,
    SpendTransaction.__table__,
    Contract.__table__,
    Supplier.__table__,
    MarketBenchmark.__table__,
    Category.__table__,
]


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generador de data spine sintetico.")
    parser.add_argument("--suppliers", type=int, default=200, help="Numero de proveedores.")
    parser.add_argument("--categories", type=int, default=15, help="Numero de categorias (max 15).")
    parser.add_argument("--months", type=int, default=24, help="Meses de historia.")
    parser.add_argument("--seed", type=int, default=42, help="Semilla reproducible.")
    parser.add_argument(
        "--end-date",
        type=str,
        default=None,
        help="Fecha (YYYY-MM-DD) del ultimo mes de historia; por defecto hoy.",
    )
    return parser.parse_args(argv)


def _with_ids(rows: list[dict], start_id: int = 1) -> list[dict]:
    """Asigna un `id` secuencial explicito a cada fila (para poder referenciar
    FKs en generadores subsiguientes sin ida y vuelta a la base de datos)."""
    for offset, row in enumerate(rows):
        row["id"] = start_id + offset
    return rows


def _bulk_insert(conn, table, rows: list[dict]) -> None:
    if not rows:
        return
    conn.execute(insert(table), rows)


def _reset_sequence(conn, table_name: str) -> None:
    conn.execute(
        text(
            f"SELECT setval(pg_get_serial_sequence(:tbl, 'id'), "
            f"COALESCE((SELECT MAX(id) FROM {table_name}), 1))"
        ),
        {"tbl": table_name},
    )


def generate(
    n_suppliers: int,
    n_categories: int,
    n_months: int,
    seed: int,
    end_date: datetime.date | None = None,
) -> dict[str, int]:
    """Genera y persiste el data spine sintetico completo. Devuelve conteos por tabla."""
    rng = np.random.default_rng(seed)
    Faker.seed(seed)
    fake = Faker()

    categories = select_categories(n_categories)
    category_rows = _with_ids(
        [
            {
                "name": c["name"],
                "taxonomy_code": c["taxonomy_code"],
                "parent_category_id": None,
                "description": c["description"],
                "is_direct_spend": c["is_direct_spend"],
            }
            for c in categories
        ]
    )
    category_ids = [row["id"] for row in category_rows]

    months = month_range(n_months, end_date)

    supplier_rows_raw = generate_suppliers(rng, fake, categories, n_suppliers)
    supplier_rows = _with_ids(supplier_rows_raw)
    supplier_ids = [row["id"] for row in supplier_rows]

    benchmark_rows = generate_market_benchmarks(rng, categories, category_ids, months)
    benchmark_index: dict[tuple[int, datetime.date], float] = {
        (row["category_id"], row["period_month"]): row["price_index"] for row in benchmark_rows
    }
    benchmark_rows = _with_ids(benchmark_rows)

    contract_rows = generate_contracts(
        rng, categories, category_ids, supplier_rows, supplier_ids, months, benchmark_index
    )
    contract_rows = _with_ids(contract_rows)

    transaction_rows = generate_spend_transactions(
        rng,
        fake,
        categories,
        category_ids,
        supplier_rows,
        supplier_ids,
        contract_rows,
        months,
        benchmark_index,
    )
    transaction_rows = _with_ids(transaction_rows)
    transaction_ids = [row["id"] for row in transaction_rows]

    invoice_rows = generate_invoices(rng, transaction_rows, transaction_ids)
    invoice_rows = _with_ids(invoice_rows)

    engine = get_engine()

    with engine.begin() as conn:
        for table in _TABLES_IN_TRUNCATE_ORDER:
            conn.execute(text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE'))

        _bulk_insert(conn, Category.__table__, category_rows)
        _bulk_insert(conn, Supplier.__table__, supplier_rows)
        _bulk_insert(conn, MarketBenchmark.__table__, benchmark_rows)
        _bulk_insert(conn, Contract.__table__, contract_rows)
        _bulk_insert(conn, SpendTransaction.__table__, transaction_rows)
        _bulk_insert(conn, Invoice.__table__, invoice_rows)

        for table_name in (
            "categories",
            "suppliers",
            "market_benchmarks",
            "contracts",
            "spend_transactions",
            "invoices",
        ):
            _reset_sequence(conn, table_name)

    return {
        "categories": len(category_rows),
        "suppliers": len(supplier_rows),
        "market_benchmarks": len(benchmark_rows),
        "contracts": len(contract_rows),
        "spend_transactions": len(transaction_rows),
        "invoices": len(invoice_rows),
    }


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    end_date = (
        datetime.date.fromisoformat(args.end_date) if args.end_date else None
    )

    print(
        f"Generando data spine sintetico: suppliers={args.suppliers} "
        f"categories={args.categories} months={args.months} seed={args.seed}"
    )
    start = time.perf_counter()
    counts = generate(args.suppliers, args.categories, args.months, args.seed, end_date)
    elapsed = time.perf_counter() - start

    print(f"Listo en {elapsed:.1f}s:")
    for table_name, count in counts.items():
        print(f"  {table_name}: {count:,}")

    if counts["spend_transactions"] < 50_000:
        print(
            f"ADVERTENCIA: spend_transactions={counts['spend_transactions']:,} < 50,000 "
            "(criterio de exito de Fase 2 no cumplido con estos parametros).",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

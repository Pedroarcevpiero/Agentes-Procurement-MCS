"""Taxonomia sintetica de 15 categorias de compra estilo procurement.

Cada categoria trae los parametros que alimentan al resto de generadores:
rango de precio unitario (para amounts log-normales), volumen mensual de
transacciones, estacionalidad, tendencia anual de precio (para
`market_benchmarks`) y peso relativo de asignacion de proveedores.
"""
from __future__ import annotations

from typing import TypedDict


class CategorySpec(TypedDict):
    name: str
    taxonomy_code: str
    description: str
    is_direct_spend: bool
    price_mean: float
    price_sigma: float
    qty_mean: float
    qty_sigma: float
    monthly_txn_range: tuple[int, int]
    seasonality_amplitude: float
    seasonality_phase_month: int
    annual_trend_pct: float
    supplier_weight: float
    contract_discount: float


CATEGORIES: list[CategorySpec] = [
    {
        "name": "IT Hardware",
        "taxonomy_code": "43211500",
        "description": "Servidores, laptops, redes y equipos de computo.",
        "is_direct_spend": False,
        "price_mean": 950.0,
        "price_sigma": 0.65,
        "qty_mean": 3.0,
        "qty_sigma": 0.55,
        "monthly_txn_range": (190, 290),
        "seasonality_amplitude": 0.09,
        "seasonality_phase_month": 11,
        "annual_trend_pct": -0.04,
        "supplier_weight": 1.3,
        "contract_discount": 0.90,
    },
    {
        "name": "IT Software & SaaS",
        "taxonomy_code": "43230000",
        "description": "Licencias de software, suscripciones SaaS y soporte.",
        "is_direct_spend": False,
        "price_mean": 620.0,
        "price_sigma": 0.7,
        "qty_mean": 5.0,
        "qty_sigma": 0.6,
        "monthly_txn_range": (175, 260),
        "seasonality_amplitude": 0.05,
        "seasonality_phase_month": 1,
        "annual_trend_pct": 0.03,
        "supplier_weight": 1.1,
        "contract_discount": 0.88,
    },
    {
        "name": "MRO (Mantenimiento, Reparacion y Operaciones)",
        "taxonomy_code": "26101500",
        "description": "Repuestos, herramientas y consumibles de mantenimiento de planta.",
        "is_direct_spend": False,
        "price_mean": 180.0,
        "price_sigma": 0.8,
        "qty_mean": 12.0,
        "qty_sigma": 0.7,
        "monthly_txn_range": (250, 400),
        "seasonality_amplitude": 0.06,
        "seasonality_phase_month": 6,
        "annual_trend_pct": 0.02,
        "supplier_weight": 1.4,
        "contract_discount": 0.93,
    },
    {
        "name": "BPO (Business Process Outsourcing)",
        "taxonomy_code": "81110000",
        "description": "Servicios tercerizados de back-office, soporte y CX.",
        "is_direct_spend": False,
        "price_mean": 4200.0,
        "price_sigma": 0.4,
        "qty_mean": 1.2,
        "qty_sigma": 0.3,
        "monthly_txn_range": (50, 100),
        "seasonality_amplitude": 0.03,
        "seasonality_phase_month": 1,
        "annual_trend_pct": 0.025,
        "supplier_weight": 0.7,
        "contract_discount": 0.91,
    },
    {
        "name": "Logistica y Transporte",
        "taxonomy_code": "78101500",
        "description": "Flete, transporte y distribucion de mercancias.",
        "is_direct_spend": True,
        "price_mean": 1350.0,
        "price_sigma": 0.55,
        "qty_mean": 2.5,
        "qty_sigma": 0.5,
        "monthly_txn_range": (200, 325),
        "seasonality_amplitude": 0.12,
        "seasonality_phase_month": 11,
        "annual_trend_pct": 0.05,
        "supplier_weight": 1.2,
        "contract_discount": 0.92,
    },
    {
        "name": "Materias Primas",
        "taxonomy_code": "11101500",
        "description": "Insumos productivos directos (metales, quimicos, polimeros).",
        "is_direct_spend": True,
        "price_mean": 2100.0,
        "price_sigma": 0.5,
        "qty_mean": 8.0,
        "qty_sigma": 0.6,
        "monthly_txn_range": (150, 240),
        "seasonality_amplitude": 0.10,
        "seasonality_phase_month": 3,
        "annual_trend_pct": 0.06,
        "supplier_weight": 1.0,
        "contract_discount": 0.94,
    },
    {
        "name": "Empaque y Embalaje",
        "taxonomy_code": "24101500",
        "description": "Materiales de empaque, embalaje y etiquetado.",
        "is_direct_spend": True,
        "price_mean": 260.0,
        "price_sigma": 0.6,
        "qty_mean": 15.0,
        "qty_sigma": 0.65,
        "monthly_txn_range": (175, 275),
        "seasonality_amplitude": 0.11,
        "seasonality_phase_month": 11,
        "annual_trend_pct": 0.03,
        "supplier_weight": 1.0,
        "contract_discount": 0.92,
    },
    {
        "name": "Servicios Profesionales y Consultoria",
        "taxonomy_code": "80101500",
        "description": "Consultoria estrategica, legal, financiera y auditoria.",
        "is_direct_spend": False,
        "price_mean": 8500.0,
        "price_sigma": 0.45,
        "qty_mean": 1.0,
        "qty_sigma": 0.2,
        "monthly_txn_range": (31, 69),
        "seasonality_amplitude": 0.04,
        "seasonality_phase_month": 12,
        "annual_trend_pct": 0.02,
        "supplier_weight": 0.6,
        "contract_discount": 0.95,
    },
    {
        "name": "Facilities Management",
        "taxonomy_code": "72101500",
        "description": "Limpieza, seguridad y mantenimiento de instalaciones.",
        "is_direct_spend": False,
        "price_mean": 900.0,
        "price_sigma": 0.5,
        "qty_mean": 2.0,
        "qty_sigma": 0.4,
        "monthly_txn_range": (112, 190),
        "seasonality_amplitude": 0.03,
        "seasonality_phase_month": 6,
        "annual_trend_pct": 0.025,
        "supplier_weight": 0.9,
        "contract_discount": 0.93,
    },
    {
        "name": "Marketing y Publicidad",
        "taxonomy_code": "82101500",
        "description": "Agencias, medios y produccion de campanas.",
        "is_direct_spend": False,
        "price_mean": 3100.0,
        "price_sigma": 0.6,
        "qty_mean": 1.3,
        "qty_sigma": 0.35,
        "monthly_txn_range": (62, 125),
        "seasonality_amplitude": 0.15,
        "seasonality_phase_month": 10,
        "annual_trend_pct": 0.01,
        "supplier_weight": 0.7,
        "contract_discount": 0.90,
    },
    {
        "name": "Viajes y Gastos de Representacion",
        "taxonomy_code": "90101500",
        "description": "Viajes corporativos, hospedaje y viaticos.",
        "is_direct_spend": False,
        "price_mean": 480.0,
        "price_sigma": 0.5,
        "qty_mean": 1.5,
        "qty_sigma": 0.3,
        "monthly_txn_range": (225, 350),
        "seasonality_amplitude": 0.10,
        "seasonality_phase_month": 7,
        "annual_trend_pct": 0.04,
        "supplier_weight": 1.0,
        "contract_discount": 0.95,
    },
    {
        "name": "Telecomunicaciones",
        "taxonomy_code": "83101500",
        "description": "Conectividad, datos y servicios de telefonia.",
        "is_direct_spend": False,
        "price_mean": 1450.0,
        "price_sigma": 0.4,
        "qty_mean": 2.0,
        "qty_sigma": 0.3,
        "monthly_txn_range": (75, 125),
        "seasonality_amplitude": 0.02,
        "seasonality_phase_month": 1,
        "annual_trend_pct": -0.015,
        "supplier_weight": 0.6,
        "contract_discount": 0.87,
    },
    {
        "name": "Suministros de Oficina",
        "taxonomy_code": "14101500",
        "description": "Papeleria, mobiliario menor y consumibles de oficina.",
        "is_direct_spend": False,
        "price_mean": 95.0,
        "price_sigma": 0.7,
        "qty_mean": 20.0,
        "qty_sigma": 0.7,
        "monthly_txn_range": (212, 325),
        "seasonality_amplitude": 0.07,
        "seasonality_phase_month": 8,
        "annual_trend_pct": 0.015,
        "supplier_weight": 1.1,
        "contract_discount": 0.94,
    },
    {
        "name": "Energia y Servicios Publicos",
        "taxonomy_code": "15101500",
        "description": "Electricidad, gas y agua para plantas y oficinas.",
        "is_direct_spend": False,
        "price_mean": 5200.0,
        "price_sigma": 0.35,
        "qty_mean": 1.0,
        "qty_sigma": 0.15,
        "monthly_txn_range": (37, 75),
        "seasonality_amplitude": 0.18,
        "seasonality_phase_month": 1,
        "annual_trend_pct": 0.07,
        "supplier_weight": 0.5,
        "contract_discount": 0.96,
    },
    {
        "name": "Bienes de Capital",
        "taxonomy_code": "31101500",
        "description": "Maquinaria y equipo de capital para produccion.",
        "is_direct_spend": True,
        "price_mean": 42000.0,
        "price_sigma": 0.5,
        "qty_mean": 1.0,
        "qty_sigma": 0.1,
        "monthly_txn_range": (10, 25),
        "seasonality_amplitude": 0.05,
        "seasonality_phase_month": 4,
        "annual_trend_pct": 0.02,
        "supplier_weight": 0.4,
        "contract_discount": 0.95,
    },
]


def select_categories(n: int) -> list[CategorySpec]:
    """Devuelve las primeras `n` categorias de la taxonomia (max 15 definidas)."""
    if n > len(CATEGORIES):
        raise ValueError(
            f"Solo hay {len(CATEGORIES)} categorias definidas en la taxonomia sintetica; "
            f"se pidieron {n}."
        )
    return CATEGORIES[:n]

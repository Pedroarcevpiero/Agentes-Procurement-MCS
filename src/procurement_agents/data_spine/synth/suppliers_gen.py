"""Generador sintetico de proveedores."""
from __future__ import annotations

import numpy as np
from faker import Faker


_COUNTRIES = [
    "US", "MX", "DE", "CN", "IN", "BR", "GB", "FR", "JP", "CA",
    "ES", "IT", "NL", "PL", "VN", "KR", "AU", "SE", "TR", "ZA",
]
_COUNTRY_WEIGHTS = np.array(
    [0.22, 0.10, 0.08, 0.09, 0.07, 0.05, 0.06, 0.05, 0.04, 0.04,
     0.03, 0.03, 0.03, 0.025, 0.025, 0.02, 0.02, 0.02, 0.015, 0.015]
)
_COUNTRY_WEIGHTS = _COUNTRY_WEIGHTS / _COUNTRY_WEIGHTS.sum()


def generate_suppliers(
    rng: np.random.Generator,
    fake: Faker,
    categories: list[dict],
    n_suppliers: int,
) -> list[dict]:
    """Genera `n_suppliers` filas de proveedor (sin `id`, se asigna al insertar).

    Cada proveedor recibe una `primary_category_id` (indice 1-based sobre
    `categories`, en el mismo orden en que se insertaran) elegido con peso
    `supplier_weight` de la categoria, de forma que categorias mas grandes
    (ej. MRO, IT Hardware) concentren mas proveedores.
    """
    weights = np.array([c["supplier_weight"] for c in categories], dtype=float)
    weights = weights / weights.sum()
    category_ids = rng.choice(np.arange(1, len(categories) + 1), size=n_suppliers, p=weights)

    rows: list[dict] = []
    seen_legal_ids: set[str] = set()
    for i in range(n_suppliers):
        country = rng.choice(_COUNTRIES, p=_COUNTRY_WEIGHTS)
        legal_id = f"SYN-{country}-{100000 + i}"
        while legal_id in seen_legal_ids:
            legal_id = f"{legal_id}-{rng.integers(0, 9999)}"
        seen_legal_ids.add(legal_id)

        risk_score = float(np.clip(rng.beta(2, 5) * 100, 0, 100))
        on_time_delivery_rate = float(np.clip(rng.beta(9, 2), 0.5, 0.999))
        quality_score = float(np.clip(rng.normal(85, 8), 40, 100))
        diversity_flag = bool(rng.random() < 0.18)

        rows.append(
            {
                "name": fake.unique.company(),
                "legal_id": legal_id,
                "country": str(country),
                "primary_category_id": int(category_ids[i]),
                "risk_score": round(risk_score, 2),
                "on_time_delivery_rate": round(on_time_delivery_rate, 4),
                "quality_score": round(quality_score, 2),
                "diversity_flag": diversity_flag,
                "is_active": True,
            }
        )
    return rows

"""Generador de meses de historia y benchmarks de mercado mensuales."""
from __future__ import annotations

import datetime
import math

import numpy as np


def month_range(n_months: int, end_date: datetime.date | None = None) -> list[datetime.date]:
    """Devuelve `n_months` primeros-dia-de-mes en orden ascendente, terminando
    en el mes de `end_date` (por defecto hoy)."""
    end_date = end_date or datetime.date.today()
    anchor = end_date.replace(day=1)
    months: list[datetime.date] = []
    for offset in range(n_months - 1, -1, -1):
        year = anchor.year
        month = anchor.month - offset
        while month <= 0:
            month += 12
            year -= 1
        months.append(datetime.date(year, month, 1))
    return months


def generate_market_benchmarks(
    rng: np.random.Generator,
    categories: list[dict],
    category_ids: list[int],
    months: list[datetime.date],
    region: str = "GLOBAL",
) -> list[dict]:
    """Genera benchmarks mensuales por categoria con tendencia + estacionalidad + ruido.

    `price_index` parte de 100 en el primer mes de la ventana y evoluciona con
    una tendencia anual compuesta (`annual_trend_pct`) mas un componente
    estacional senoidal de amplitud `seasonality_amplitude` con pico en
    `seasonality_phase_month`, mas ruido gaussiano pequeno.
    """
    rows: list[dict] = []
    n_months = len(months)
    for cat, cat_id in zip(categories, category_ids, strict=True):
        monthly_trend = (1 + cat["annual_trend_pct"]) ** (1 / 12) - 1
        index_series: list[float] = []
        base_index = 100.0
        for month_idx, month_date in enumerate(months):
            trend_component = (1 + monthly_trend) ** month_idx
            seasonal_component = 1 + cat["seasonality_amplitude"] * math.sin(
                2 * math.pi * (month_date.month - cat["seasonality_phase_month"]) / 12
            )
            noise = rng.normal(0, 0.012)
            index_value = base_index * trend_component * seasonal_component * (1 + noise)
            index_series.append(index_value)

        for month_idx, month_date in enumerate(months):
            if month_idx >= 12:
                yoy = (index_series[month_idx] / index_series[month_idx - 12] - 1) * 100
            else:
                yoy = cat["annual_trend_pct"] * 100
            rows.append(
                {
                    "category_id": cat_id,
                    "period_month": month_date,
                    "price_index": round(index_series[month_idx], 4),
                    "yoy_price_change_pct": round(yoy, 3),
                    "region": region,
                    "source": "synthetic_market_feed",
                }
            )
        _ = n_months
    return rows

"""Carga y valida las politicas declarativas de guardrails (`guardrails/policies/*.yaml`).

Cada politica se modela como un dataclass inmutable con validacion explicita
en la carga (tipos, rangos), para que un YAML malformado falle rapido y con
un mensaje claro en vez de propagar `None`/`KeyError` silenciosos hasta un
hook en produccion.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

POLICIES_DIR = Path(__file__).resolve().parent / "policies"


class PolicyValidationError(ValueError):
    """Politica YAML ausente, malformada o con valores fuera de rango."""


@dataclass(frozen=True)
class CommonPolicy:
    """Politica comun a todos los agentes (`policies/common.yaml`)."""

    transactional_denylist: tuple[str, ...]


@dataclass(frozen=True)
class CategoryCopilotPolicy:
    """Politica del agente Category Copilot (`policies/category_copilot.yaml`)."""

    min_confidence_auto_publish: float
    max_auto_publish_usd: float
    max_auto_publish_pct: float


def _load_yaml_mapping(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise PolicyValidationError(f"No existe el archivo de politica: {path}")
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if data is None:
        data = {}
    if not isinstance(data, dict):
        raise PolicyValidationError(f"{path}: el YAML debe tener un mapping en la raiz, recibido {type(data)!r}.")
    return data


def _require_number(data: dict[str, Any], key: str, path: Path, *, minimum: float | None = None) -> float:
    if key not in data:
        raise PolicyValidationError(f"{path}: falta la clave requerida '{key}'.")
    value = data[key]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise PolicyValidationError(f"{path}: '{key}' debe ser numerico, recibido {value!r}.")
    if minimum is not None and value < minimum:
        raise PolicyValidationError(f"{path}: '{key}' debe ser >= {minimum}, recibido {value}.")
    return float(value)


def load_common_policy(path: Path | None = None) -> CommonPolicy:
    """Carga y valida `policies/common.yaml`.

    Raises:
        PolicyValidationError: si el archivo falta o `transactional_denylist`
            no es una lista no vacia de strings.
    """
    resolved = path or POLICIES_DIR / "common.yaml"
    data = _load_yaml_mapping(resolved)

    denylist = data.get("transactional_denylist")
    if not isinstance(denylist, list) or not denylist:
        raise PolicyValidationError(
            f"{resolved}: 'transactional_denylist' debe ser una lista no vacia."
        )
    if not all(isinstance(item, str) and item for item in denylist):
        raise PolicyValidationError(
            f"{resolved}: todos los elementos de 'transactional_denylist' deben ser strings no vacios."
        )

    return CommonPolicy(transactional_denylist=tuple(denylist))


def load_category_copilot_policy(path: Path | None = None) -> CategoryCopilotPolicy:
    """Carga y valida `policies/category_copilot.yaml`.

    Raises:
        PolicyValidationError: si faltan claves, no son numericas, o estan
            fuera de rango (ej. confianza fuera de [0.0, 1.0]).
    """
    resolved = path or POLICIES_DIR / "category_copilot.yaml"
    data = _load_yaml_mapping(resolved)

    min_confidence = _require_number(data, "min_confidence_auto_publish", resolved, minimum=0.0)
    if min_confidence > 1.0:
        raise PolicyValidationError(
            f"{resolved}: 'min_confidence_auto_publish' debe estar en [0.0, 1.0], recibido {min_confidence}."
        )
    max_usd = _require_number(data, "max_auto_publish_usd", resolved, minimum=0.0)
    max_pct = _require_number(data, "max_auto_publish_pct", resolved, minimum=0.0)

    return CategoryCopilotPolicy(
        min_confidence_auto_publish=min_confidence,
        max_auto_publish_usd=max_usd,
        max_auto_publish_pct=max_pct,
    )


@lru_cache
def get_common_policy() -> CommonPolicy:
    """Devuelve la `CommonPolicy` cacheada (carga perezosa desde disco)."""
    return load_common_policy()


@lru_cache
def get_category_copilot_policy() -> CategoryCopilotPolicy:
    """Devuelve la `CategoryCopilotPolicy` cacheada (carga perezosa desde disco)."""
    return load_category_copilot_policy()

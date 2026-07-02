"""Carga `config/model_assignment.yaml`: alias de modelo por rol de agente.

Unica fuente de verdad para saber que alias del Claude Agent SDK (`opus` /
`sonnet` / `haiku`, nunca un ID de modelo versionado) usa cada rol. Los
constructores de `AgentDefinition` / `ClaudeAgentOptions` deben llamar a
`get_model_alias(role)` en vez de hardcodear el alias.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml

from procurement_agents.config.settings import get_settings


class ModelAssignmentError(ValueError):
    """El rol pedido no existe en `model_assignment.yaml` o el archivo es invalido."""


@lru_cache
def _load_assignments(path: Path | None = None) -> dict[str, dict]:
    resolved = path or get_settings().model_assignment_path
    if not resolved.exists():
        raise ModelAssignmentError(f"No existe el archivo de asignacion de modelos: {resolved}")
    with resolved.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        raise ModelAssignmentError(f"{resolved}: el YAML debe tener un mapping en la raiz.")
    return data


def get_model_alias(role: str) -> str:
    """Devuelve el alias de modelo (`opus`/`sonnet`/`haiku`) asignado a `role`.

    Raises:
        ModelAssignmentError: si `role` no esta declarado en
            `model_assignment.yaml` o le falta la clave `alias`.
    """
    assignments = _load_assignments()
    entry = assignments.get(role)
    if not isinstance(entry, dict) or "alias" not in entry:
        raise ModelAssignmentError(
            f"El rol '{role}' no esta declarado (o le falta 'alias') en model_assignment.yaml."
        )
    return str(entry["alias"])

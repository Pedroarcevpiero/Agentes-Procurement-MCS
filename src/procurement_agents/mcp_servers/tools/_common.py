"""Utilidades compartidas por las funciones de consulta de las tools MCP.

Estas funciones son deliberadamente "puras" respecto a Postgres: reciben una
`Session` de SQLAlchemy ya abierta (via `data_spine/db.py`) y devuelven
dicts/listas serializables a JSON (sin `Decimal`, `date`/`datetime` o Enum
crudos). Los servidores MCP (`data_spine_server.py`, `market_intel_server.py`)
son una capa fina que abre la sesion, llama a estas funciones y traduce
excepciones a la forma `{"content": [...], "isError": True}` que espera el
Claude Agent SDK.

Aviso del supervisor (Fase 2 -> Fase 3): los enums de `models.py` se
persisten en Postgres por su *nombre* en MAYUSCULAS (ej. `ACTIVE`,
`MATCHED`). Por eso todo filtrado por estado pasa por los enums de
`data_spine.models` (via ORM), nunca por strings en minuscula.
"""
from __future__ import annotations

import datetime
import decimal
import enum
import json
import logging
from collections.abc import Callable
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from procurement_agents.data_spine.db import session_scope
from procurement_agents.data_spine.models import Category

logger = logging.getLogger(__name__)


class ToolInputError(ValueError):
    """Error de validacion de entrada de una tool (categoria/proveedor inexistente, etc.).

    Se distingue de errores inesperados para que el handler MCP los traduzca
    a `isError: True` con un mensaje accionable en vez de dejar escapar una
    excepcion generica.
    """


def to_jsonable(value: Any) -> Any:
    """Convierte tipos no serializables (Decimal, date/datetime, Enum) a JSON-friendly."""
    if isinstance(value, decimal.Decimal):
        return float(value)
    if isinstance(value, enum.Enum):
        return value.value
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.isoformat()
    return value


def resolve_category(
    session: Session, *, category_id: int | None = None, category_name: str | None = None
) -> Category:
    """Resuelve una `Category` por id exacto o por nombre (case-insensitive, match parcial).

    Lanza `ToolInputError` si no se provee ningun identificador o si no hay
    coincidencias, para que el handler MCP pueda devolver `isError` en vez de
    romper con un `None` silencioso.
    """
    if category_id is not None:
        category = session.get(Category, category_id)
        if category is None:
            raise ToolInputError(f"No existe la categoria con id={category_id}.")
        return category

    if category_name:
        stmt = select(Category).where(Category.name.ilike(f"%{category_name}%"))
        matches = list(session.execute(stmt).scalars().all())
        if not matches:
            raise ToolInputError(f"No se encontro ninguna categoria que coincida con '{category_name}'.")
        if len(matches) > 1:
            names = ", ".join(f"{c.id}:{c.name}" for c in matches)
            raise ToolInputError(
                f"'{category_name}' coincide con varias categorias ({names}); "
                "usa category_id o un nombre mas especifico."
            )
        return matches[0]

    raise ToolInputError("Debes proveer category_id o category_name.")


def mcp_ok(data: Any) -> dict[str, Any]:
    """Empaqueta un resultado exitoso en el formato de contenido MCP (`{"content": [...]}`)."""
    return {"content": [{"type": "text", "text": json.dumps(data, default=to_jsonable, ensure_ascii=False, indent=2)}]}


def mcp_error(message: str) -> dict[str, Any]:
    """Empaqueta un error en el formato MCP sin lanzar excepcion.

    Nota de implementacion: la version instalada de `claude-agent-sdk`
    (0.2.110) traduce la clave `is_error` (snake_case) del dict devuelto por
    el handler a `CallToolResult(isError=...)` -- ver
    `create_sdk_mcp_server` en `claude_agent_sdk/query.py`. Se usa
    `is_error` aqui (no `isError`) para que el runtime del SDK realmente lo
    reconozca; documentado como desviacion del plan (que menciona
    `isError`) en el checklist de Fase 3.
    """
    return {"content": [{"type": "text", "text": message}], "is_error": True}


async def run_tool(handler: Callable[..., Any], /, **kwargs: Any) -> dict[str, Any]:
    """Abre una sesion, ejecuta `handler(session, **kwargs)` y empaqueta el resultado.

    Traduce `ToolInputError` (entrada invalida: id inexistente, ambigua,
    citas vacias, etc.) y cualquier excepcion inesperada a `mcp_error(...)`
    en vez de dejarla escapar, para que el agente pueda leer el mensaje y
    reintentar con argumentos corregidos en lugar de que la sesion completa
    del SDK aborte.
    """
    try:
        with session_scope() as session:
            result = handler(session, **kwargs)
        return mcp_ok(result)
    except ToolInputError as exc:
        return mcp_error(str(exc))
    except Exception:  # noqa: BLE001 - frontera de la tool: nunca dejar escapar excepciones al SDK
        logger.exception("Error inesperado ejecutando tool %s", getattr(handler, "__name__", handler))
        return mcp_error(
            f"Error interno ejecutando {getattr(handler, '__name__', 'la tool')}; "
            "revisa los logs del servidor MCP."
        )

"""Runner async de Category Copilot: ejecuta `query()` del SDK con
`build_root_options()` y devuelve un resultado estructurado (Fase 5).

Uso (CLI/tests/smoke e2e):

    ```python
    result = await run_copilot_query("¿Donde hay oportunidades de ahorro en IT Hardware?")
    print(result.final_text)
    ```
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field

from claude_agent_sdk import (
    AssistantMessage,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    query,
)

from procurement_agents.agents.orchestrator.definition import build_root_options

logger = logging.getLogger(__name__)

# Nombres de tool que representan una delegacion a un subagente. El SDK
# instalado (claude-agent-sdk==0.2.110) documenta la capacidad de
# subagentes como "invocable via la tool Agent" (ver
# `agents/critic/definition.py` y `types.py::ClaudeAgentOptions.agents`), y
# en este entorno concreto la tool efectivamente se llama "Agent" (se
# verifico contra el runtime real). Se incluye tambien "Task" de forma
# defensiva: es el nombre interno usado por otras versiones/builds del CLI
# subyacente para el mismo mecanismo de delegacion, por si la version del
# CLI resuelta en produccion difiere de la usada en esta fase.
SUBAGENT_TOOL_NAMES = frozenset({"Agent", "Task"})


@dataclass
class CopilotResult:
    """Resultado estructurado de una consulta al Category Copilot."""

    query: str
    final_text: str
    session_id: str | None
    total_cost_usd: float | None
    subagent_invocations: int
    subagent_names_invoked: list[str] = field(default_factory=list)
    num_turns: int | None = None
    is_error: bool = False
    stop_reason: str | None = None


async def run_copilot_query(query_text: str) -> CopilotResult:
    """Ejecuta una consulta de comprador contra el agente Category Copilot.

    Corre `claude_agent_sdk.query()` con las opciones de
    `build_root_options()` (orquestador + 2 subagentes de dominio + critico
    + servidores MCP + hooks), consume el stream completo imprimiendo
    progreso minimo por stdout, y devuelve un `CopilotResult` con el texto
    final, costo real, session_id y cuantas veces se delego en un
    subagente (deteccion por `ToolUseBlock.name` en `SUBAGENT_TOOL_NAMES`).
    """
    options = build_root_options()

    final_text = ""
    session_id: str | None = None
    total_cost_usd: float | None = None
    num_turns: int | None = None
    is_error = False
    stop_reason: str | None = None
    subagent_invocations = 0
    subagent_names_invoked: list[str] = []

    print(f"[copilot] consulta: {query_text!r}")

    async for message in query(prompt=query_text, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock) and block.text.strip():
                    final_text = block.text
                    preview = block.text[:200].replace("\n", " ")
                    print(f"[copilot] texto (modelo={message.model}): {preview}...")
                elif isinstance(block, ToolUseBlock):
                    if block.name in SUBAGENT_TOOL_NAMES:
                        subagent_invocations += 1
                        agent_name = block.input.get("subagent_type") or block.input.get("agent") or "?"
                        subagent_names_invoked.append(str(agent_name))
                        print(f"[copilot] delegacion a subagente #{subagent_invocations}: {agent_name!r}")
                    else:
                        print(f"[copilot] tool_use: {block.name}")
        elif isinstance(message, ResultMessage):
            session_id = message.session_id
            total_cost_usd = message.total_cost_usd
            num_turns = message.num_turns
            is_error = message.is_error
            stop_reason = message.stop_reason
            if message.result:
                final_text = message.result
            print(
                f"[copilot] resultado: is_error={is_error} num_turns={num_turns} "
                f"total_cost_usd={total_cost_usd} session_id={session_id}"
            )
        else:
            logger.debug("mensaje no manejado en el stream: %r", message)

    return CopilotResult(
        query=query_text,
        final_text=final_text,
        session_id=session_id,
        total_cost_usd=total_cost_usd,
        subagent_invocations=subagent_invocations,
        subagent_names_invoked=subagent_names_invoked,
        num_turns=num_turns,
        is_error=is_error,
        stop_reason=stop_reason,
    )

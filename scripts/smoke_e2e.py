"""Smoke e2e REAL de Fase 5: una sola consulta real contra la API, acotada.

Ejecuta `run_copilot_query()` (orquestador + spend_market + demand_simulation
+ critic, con hooks/guardrails reales y Postgres real) y escribe la
transcripcion + evidencia en `scripts/smoke_e2e_output.md`.

Uso:
    .venv/bin/python scripts/smoke_e2e.py
"""
from __future__ import annotations

import asyncio
import datetime
import io
import sys
from contextlib import redirect_stdout

from sqlalchemy import select

from procurement_agents.agents.category_copilot.runner import run_copilot_query
from procurement_agents.data_spine.db import session_scope
from procurement_agents.data_spine.models import DemandScenario, SavingsOpportunity

QUERY = "¿Dónde hay oportunidades de ahorro en la categoría IT Hardware en los últimos 12 meses?"

OUTPUT_PATH = "scripts/smoke_e2e_output.md"


def _fetch_new_rows(created_after: datetime.datetime) -> tuple[list[dict], list[dict]]:
    with session_scope() as session:
        opportunities = (
            session.execute(
                select(SavingsOpportunity)
                .where(SavingsOpportunity.created_at >= created_after)
                .order_by(SavingsOpportunity.id)
            )
            .scalars()
            .all()
        )
        scenarios = (
            session.execute(
                select(DemandScenario)
                .where(DemandScenario.created_at >= created_after)
                .order_by(DemandScenario.id)
            )
            .scalars()
            .all()
        )
        opp_rows = [
            {
                "id": o.id,
                "category_id": o.category_id,
                "opportunity_type": o.opportunity_type,
                "estimated_savings_usd": float(o.estimated_savings_usd),
                "confidence_score": float(o.confidence_score),
                "status": o.status.value,
                "source_transaction_ids": o.source_transaction_ids,
                "source_benchmark_ids": o.source_benchmark_ids,
                "created_by_agent": o.created_by_agent,
                "session_id": o.session_id,
            }
            for o in opportunities
        ]
        scenario_rows = [
            {
                "id": s.id,
                "category_id": s.category_id,
                "scenario_type": s.scenario_type.value,
                "projected_volume_change_pct": float(s.projected_volume_change_pct),
                "projected_spend_usd": float(s.projected_spend_usd),
                "volatility_index": float(s.volatility_index),
                "created_by_agent": s.created_by_agent,
                "session_id": s.session_id,
            }
            for s in scenarios
        ]
        return opp_rows, scenario_rows


def _validate_citations_sql(opp_rows: list[dict]) -> list[str]:
    """Verifica por SQL que cada source_transaction_id/benchmark_id citado existe."""
    problems: list[str] = []
    with session_scope() as session:
        from procurement_agents.data_spine.models import MarketBenchmark, SpendTransaction

        for row in opp_rows:
            txn_ids = row["source_transaction_ids"] or []
            bm_ids = row["source_benchmark_ids"] or []
            if not txn_ids and not bm_ids:
                problems.append(f"opportunity id={row['id']}: sin citas (source_transaction_ids y source_benchmark_ids vacios)")
                continue
            if txn_ids:
                existing = set(
                    session.execute(select(SpendTransaction.id).where(SpendTransaction.id.in_(txn_ids))).scalars().all()
                )
                missing = set(txn_ids) - existing
                if missing:
                    problems.append(f"opportunity id={row['id']}: source_transaction_ids inexistentes: {missing}")
            if bm_ids:
                existing = set(
                    session.execute(select(MarketBenchmark.id).where(MarketBenchmark.id.in_(bm_ids))).scalars().all()
                )
                missing = set(bm_ids) - existing
                if missing:
                    problems.append(f"opportunity id={row['id']}: source_benchmark_ids inexistentes: {missing}")
    return problems


async def main() -> int:
    started_at = datetime.datetime.now(datetime.timezone.utc)

    buf = io.StringIO()
    with redirect_stdout(buf):
        result = await run_copilot_query(QUERY)
    stream_log = buf.getvalue()
    print(stream_log)

    opp_rows, scenario_rows = _fetch_new_rows(started_at)
    citation_problems = _validate_citations_sql(opp_rows)

    critic_mentioned = "critic" in stream_log.lower() or "VEREDICTO" in result.final_text.upper() or "veredicto" in result.final_text.lower()

    lines: list[str] = []
    lines.append("# Smoke e2e Fase 5 — Category Copilot (API real, acotado a 1 consulta)")
    lines.append("")
    lines.append(f"- Fecha (UTC): {started_at.isoformat()}")
    lines.append(f"- Consulta: `{QUERY}`")
    lines.append(f"- session_id: `{result.session_id}`")
    lines.append(f"- num_turns: {result.num_turns}")
    lines.append(f"- is_error: {result.is_error}  (stop_reason: {result.stop_reason})")
    lines.append(f"- **total_cost_usd: {result.total_cost_usd}**")
    lines.append(f"- subagent_invocations (tool_use Agent/Task detectados): {result.subagent_invocations}")
    lines.append(f"- subagent_names_invoked: {result.subagent_names_invoked}")
    lines.append("")
    lines.append("## Verificaciones del criterio de exito de Fase 5")
    lines.append("")
    lines.append(f"- (a) Respuesta final contiene cifras — ver texto final abajo.")
    lines.append(
        f"- (b) Filas nuevas en `savings_opportunities` con citas validas por SQL: "
        f"{len(opp_rows)} filas nuevas, {len(citation_problems)} problemas de citas encontrados."
    )
    if citation_problems:
        for p in citation_problems:
            lines.append(f"    - PROBLEMA: {p}")
    lines.append(f"- (c) Critico mencionado en el stream/veredicto detectado: {critic_mentioned}")
    lines.append(f"- (d) Escenarios nuevos en `demand_scenarios`: {len(scenario_rows)} filas nuevas.")
    lines.append("")
    lines.append("## Filas nuevas en savings_opportunities (verificadas por SQL)")
    lines.append("")
    lines.append("```json")
    import json

    lines.append(json.dumps(opp_rows, indent=2, ensure_ascii=False, default=str))
    lines.append("```")
    lines.append("")
    lines.append("## Filas nuevas en demand_scenarios (verificadas por SQL)")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(scenario_rows, indent=2, ensure_ascii=False, default=str))
    lines.append("```")
    lines.append("")
    lines.append("## Texto final de la respuesta del orquestador")
    lines.append("")
    lines.append("```")
    lines.append(result.final_text)
    lines.append("```")
    lines.append("")
    lines.append("## Transcript completo del stream (progreso minimo impreso por runner.py)")
    lines.append("")
    lines.append("```")
    lines.append(stream_log)
    lines.append("```")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    print(f"\n=== Evidencia escrita en {OUTPUT_PATH} ===")
    print(f"total_cost_usd={result.total_cost_usd} subagent_invocations={result.subagent_invocations}")
    print(f"savings_opportunities nuevas={len(opp_rows)} problemas_citas={len(citation_problems)}")
    print(f"demand_scenarios nuevas={len(scenario_rows)}")

    return 0 if not result.is_error and not citation_problems else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

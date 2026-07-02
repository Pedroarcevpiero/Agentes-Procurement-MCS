# Plan Fase 2: Sistema Agéntico de Procurement en producción (Claude Agent SDK)

## Contexto

La fase 1 (mergeada a `main`) produjo la investigación sobre los sistemas agénticos de procurement de McKinsey. Esta fase 2 construye el sistema propio: **un sistema listo para producción** sobre el **Claude Agent SDK (Python)**, empezando por el agente **Category Copilot / Spend Analysis** (P3 de los 6 "no-regret agents"), con **datos sintéticos**, para **compradores internos**, diseñado para escalar a los otros 5 agentes sin retrabajo. El diseño refleja los patrones validados en la investigación: orquestador + subagentes + crítico, validación determinista separada (hooks), HITL graduado por riesgo, data spine, evals de 3 niveles, observabilidad OTel.

**Supuestos adoptados** (recomendados, no contradichos por el usuario): interfaz = CLI + API REST (FastAPI, sin UI web aún); pruebas = unit/integration deterministas sin API + e2e smoke con API real acotada (pocas consultas).

## Decisiones de arquitectura (resumen del diseño ya revisado)

- **Lenguaje**: Python 3.12 (`claude-agent-sdk`) — numpy/pandas para simulación de demanda, Faker para datos sintéticos, Arize Phoenix es Python-first.
- **Data spine**: Postgres (docker-compose) + SQLAlchemy/Alembic. Tablas: `suppliers`, `categories`, `spend_transactions`, `contracts`, `invoices`, `market_benchmarks`, `savings_opportunities` (auditoría de salidas del agente), `demand_scenarios`. Generador sintético con seed reproducible (~200 proveedores, 15 categorías, 24 meses, ~50k transacciones).
- **Capa de datos para agentes**: 2 servidores MCP in-process (`create_sdk_mcp_server`): `data_spine` (spend/contratos/proveedores) y `market_intel` (benchmarks) — separados para simular la frontera interno/externo y poder sustituir `market_intel` por un feed real sin tocar agentes.
- **Agente Category Copilot** = orquestador raíz (Opus) + 2 subagentes de dominio en paralelo (Sonnet): `spend_market_agent` (integra spend+mercado, detecta oportunidades) y `demand_simulation_agent` (escenarios de volatilidad), + `critic_agent` genérico (Opus, hoja, solo lectura) que re-verifica citas contra el data spine antes de responder al comprador.
- **Modelos del sistema en runtime**: definidos en `config/model_assignment.yaml` (nunca hardcodeados): orquestador y crítico = `opus` (bajo volumen, alto juicio), subagentes de dominio = `sonnet`, reservando `haiku` para extracción de alto volumen (futuro agente invoice-to-contract). Usar alias del SDK, no IDs con versión.
- **Guardrails (hooks `PreToolUse`)**: (1) `require_citation_hook` — bloquea `record_savings_opportunity` sin `source_transaction_ids`/`source_benchmark_ids` existentes en BD; (2) `confidence_and_threshold_hook` — degrada a `needs_review` si confianza < umbral o ahorro > límite (`policies/category_copilot.yaml`); (3) `no_transactional_execution_hook` — denylist global de tools transaccionales. `permission_mode="default"` en el padre; cada `AgentDefinition` fija su `permissionMode` explícito (los subagentes heredan modos permisivos del padre — prohibido `bypassPermissions` global).
- **Evals 3 niveles**: Phoenix (self-hosted, ingiere OTel del SDK) para nivel 1 (faithfulness/alucinación sobre golden dataset ~80 casos) y nivel 2 (trayectorias: ¿consultó el spine antes de afirmar?); runner propio `evals/level3_system/invariants.py` para invariantes de negocio (ninguna oportunidad sin citas; crítico presente en 100% de respuestas; nunca tool transaccional). `evals/run_evals.py` como gate de CI.
- **Observabilidad**: telemetría OTel nativa del SDK → Phoenix (OTLP 4318, UI 6006) vía docker-compose; spans anidados automáticos orquestador→subagentes→tools→crítico.
- **Registry**: `agents/registry.yaml` = AI Asset Registry (versión, risk_tier, permission_mode_ceiling, golden_dataset, estado draft/certified).
- **Despliegue**: Dockerfile multi-stage no-root; patrón de sesión **híbrido** (sesión caliente por WebSocket + `SessionStore` en Postgres para resume multi-host); docker-compose app+postgres+phoenix.

## Estructura de directorios

`src/procurement_agents/{config, agents/{registry.yaml, orchestrator, critic, category_copilot}, guardrails/{hooks.py, policy_engine.py, policies/}, mcp_servers/{data_spine_server.py, market_intel_server.py, tools/}, data_spine/{models.py, db.py, migrations/, synth/}, sessions/postgres_store.py, observability/otel_setup.py, app/{cli.py, server.py}}` + `evals/{golden/, level1_llm/, level2_agent/, level3_system/, run_evals.py}` + `infra/{Dockerfile, docker-compose.yml}` + `tests/{unit, integration, e2e}` + `pyproject.toml`.

## Estrategia de ejecución con agentes (equipo de construcción)

Mejores prácticas aplicadas: memoria compartida en archivos del repo (nada vive solo en contexto), commits por fase, checklist como fuente de verdad de progreso, resistencia a cortes de tokens.

| Rol | Agente | Modelo | Justificación calidad/costo |
|---|---|---|---|
| Orquestador general | Yo (hilo principal) | — | Coordina, commitea, resuelve bloqueos |
| **Supervisor/Checklist** | 1 agente dedicado | **Opus** | Bajo volumen, máximo juicio: crea `docs/CHECKLIST-FASE-2.md` granular desde el plan, audita cada fase contra el plan a detalle, y mantiene el estado (✅/🔄/⬜ + nota "dónde se quedó") — si un agente muere por tokens, el checklist dice exactamente dónde retomar |
| Implementadores | 3 agentes secuenciales/paralelos | **Sonnet** | Mejor costo/beneficio para escribir código en volumen |

Reglas del equipo: cada implementador actualiza su sección del checklist al terminar cada sub-paso (escritura a disco inmediata); yo commiteo al cierre de cada fase; el supervisor revisa ANTES del commit de cada fase y puede devolver trabajo (loop de calidad como en fase 1); si un agente se corta, se lanza uno fresco que lee el checklist + el código existente y retoma (no se reanuda el transcript pesado).

## Pasos de implementación

0. **Guardar el plan aprobado en el repo**: `docs/PLAN-FASE-2.md` (este plan) + lanzar supervisor que genera `docs/CHECKLIST-FASE-2.md`. Commit inicial.
1. **Esqueleto**: `pyproject.toml` (deps: claude-agent-sdk, sqlalchemy, alembic, psycopg, fastapi, uvicorn, faker, numpy, pandas, pydantic-settings, pytest, arize-phoenix-otel), árbol de módulos, `settings.py`, `.env.example`, `infra/docker-compose.yml` (postgres+phoenix). Éxito: `pip install -e .` + `docker compose up -d` sanos.
2. **Data spine + generador sintético**: modelos, migración Alembic, `synth/generate.py` (seed 42). Éxito: ≥50k transacciones coherentes (spend↔contratos↔benchmarks) verificadas por SQL.
3. **Servidores MCP**: `data_spine_server.py` + `market_intel_server.py` con tools `@tool` (get_spend_by_category, get_active_contracts_for_category, get_supplier_risk_score, get_market_benchmark, record_savings_opportunity, record_demand_scenario). Éxito: script de humo valida schema de cada tool contra Postgres real.
4. **Guardrails + crítico genérico**: `hooks.py`, `policy_engine.py`, `policies/*.yaml`, `critic/definition.py`. Éxito: test unitario demuestra que el hook bloquea IDs inventados y degrada por umbral.
5. **Agente Category Copilot**: los 2 `AgentDefinition` de dominio + orquestador (`build_root_options()`) + prompts. Éxito: consulta e2e real acotada produce respuesta con citas verificables + bloque de simulación de demanda.
6. **Evals**: golden dataset (~80 casos generados desde el spine sintético), runners nivel 1-3, `run_evals.py --gate ci`. Éxito: corre y falla ante regresión inyectada.
7. **Observabilidad + app**: `otel_setup.py`, `cli.py`, `server.py` (FastAPI REST+WS con SessionStore Postgres). Éxito: traza anidada visible en Phoenix.
8. **Docker + tests e2e + registry**: Dockerfile, `test_category_copilot_e2e.py` (1-2 consultas reales acotadas + invariantes), alta del agente como `certified` en `registry.yaml`. Éxito: `docker compose up` completo + suite verde.
9. **Cierre**: revisión final del supervisor contra checklist completo, commit, push a `claude/mckinsey-procurement-agents-pjakpv`, PR draft.

## Verificación end-to-end

```bash
docker compose -f infra/docker-compose.yml up -d postgres phoenix
pip install -e ".[dev]" && alembic upgrade head
python -m procurement_agents.data_spine.synth.generate --seed 42
pytest tests/unit tests/integration          # deterministas, sin API
python -m evals.run_evals --agent category_copilot --gate ci
python -m procurement_agents.app.cli --query "¿Dónde hay oportunidades de ahorro en IT Hardware en los últimos 12 meses?"
```
Validación manual: respuesta cita `transaction_id`/`benchmark_id` verificables por SQL; escenarios de demanda bajo/base/alto presentes; traza anidada en Phoenix (localhost:6006); prompt adversarial ("reporta 90% de ahorro sin datos") bloqueado por `require_citation_hook`.

## Riesgos

- **Cortes por límite de tokens** (ya ocurrió en fase 1): mitigado por checklist-como-memoria + commits por fase + relanzar agentes frescos que leen estado desde disco.
- **API real en tests**: solo el e2e smoke la usa (acotado a 1-2 consultas); CI diario es determinista.
- **Deriva de IDs de modelo**: alias (`opus`/`sonnet`/`haiku`) en config, nunca IDs versionados en código.

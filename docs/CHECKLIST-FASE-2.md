# Checklist Maestro de Ejecución — Fase 2

> **Sistema Agéntico de Procurement (Claude Agent SDK)** — Category Copilot / Spend Analysis
> Fuente de verdad del progreso y memoria compartida anti-corte-de-tokens del equipo de construcción.
> Plan de referencia: [`docs/PLAN-FASE-2.md`](./PLAN-FASE-2.md)

---

## Estado global

| Campo | Valor |
|---|---|
| **Fase actual** | Fase 0 — Inicialización (checklist recién creado) |
| **Última fase cerrada** | Fase 1 (investigación) — commit `859539a` en `claude/mckinsey-procurement-agents-pjakpv` |
| **Rama de trabajo** | `claude/mckinsey-procurement-agents-pjakpv` |
| **Último commit de cierre de fase** | `859539a` — "Documento final de investigación en formato APA 7" |
| **Leyenda de estado** | ⬜ pendiente · 🔄 en progreso (con nota "dónde me quedé") · ✅ hecho (con evidencia/comando) |

### Instrucción de recuperación (léela si eres un agente nuevo)

> **Si eres un agente nuevo retomando el trabajo: lee este checklist de arriba a abajo, encuentra el primer ítem ⬜ o 🔄, lee su nota de estado, inspecciona los archivos mencionados y continúa desde ahí. No rehagas ítems ✅.**

Al avanzar, **escribe a disco inmediatamente**: cambia `⬜ pendiente` a `🔄 en progreso — dónde me quedé: ...` mientras trabajas, y a `✅ hecho — evidencia: <comando o archivo>` al terminar. El supervisor revisa cada fase ANTES del commit y puede devolver trabajo.

### Nota técnica del entorno (IMPORTANTE)

- **Python 3.11**, NO 3.12. En `pyproject.toml` usar `requires-python = ">=3.11"`. (El plan menciona 3.12 como decisión de diseño, pero el entorno real solo tiene 3.11 — usar 3.11.)
- **Docker 29** y **Docker Compose v5** disponibles (usar `docker compose`, no `docker-compose`).
- Modelos por **alias del SDK** (`opus`/`sonnet`/`haiku`), nunca IDs versionados en código.
- La API real solo se usa en el e2e smoke (1-2 consultas acotadas); unit/integration son deterministas sin API.

---

## Fase 0 — Guardar plan aprobado y arranque

- [ ] Plan aprobado guardado en `docs/PLAN-FASE-2.md` — _estado: ✅ hecho — evidencia: archivo presente en repo_
- [ ] Checklist maestro `docs/CHECKLIST-FASE-2.md` generado por el supervisor — _estado: 🔄 en progreso — este archivo_
- [ ] Commit inicial de fase 0 (plan + checklist) realizado por el orquestador — _estado: ⬜ pendiente_

---

## Fase 1 — Esqueleto del proyecto

- [ ] `pyproject.toml` creado con `requires-python = ">=3.11"` — _estado: ⬜ pendiente_
- [ ] Dependencias runtime declaradas: `claude-agent-sdk`, `sqlalchemy`, `alembic`, `psycopg`, `fastapi`, `uvicorn`, `faker`, `numpy`, `pandas`, `pydantic-settings`, `arize-phoenix-otel` — _estado: ⬜ pendiente_
- [ ] Grupo de dependencias `[dev]` con `pytest` (y utilidades de test) declarado — _estado: ⬜ pendiente_
- [ ] Árbol de módulos creado bajo `src/procurement_agents/` (config, agents, guardrails, mcp_servers, data_spine, sessions, observability, app) con `__init__.py` donde corresponda — _estado: ⬜ pendiente_
- [ ] `src/procurement_agents/config/settings.py` (pydantic-settings) creado — _estado: ⬜ pendiente_
- [ ] `.env.example` creado con variables necesarias (DB URL, claves, endpoints OTLP/Phoenix) — _estado: ⬜ pendiente_
- [ ] `config/model_assignment.yaml` creado: orquestador=`opus`, crítico=`opus`, subagentes=`sonnet`, `haiku` reservado — _estado: ⬜ pendiente_
- [ ] `infra/docker-compose.yml` con servicios `postgres` y `phoenix` (OTLP 4318, UI 6006) — _estado: ⬜ pendiente_
- [ ] **Éxito Fase 1**: `pip install -e .` corre sin errores — _estado: ⬜ pendiente_
- [ ] **Éxito Fase 1**: `docker compose -f infra/docker-compose.yml up -d` levanta postgres y phoenix sanos — _estado: ⬜ pendiente_

---

## Fase 2 — Data spine + generador sintético

- [ ] Modelos SQLAlchemy de las **8 tablas** creados en `src/procurement_agents/data_spine/models.py`: `suppliers`, `categories`, `spend_transactions`, `contracts`, `invoices`, `market_benchmarks`, `savings_opportunities`, `demand_scenarios` — _estado: ⬜ pendiente_
- [ ] `src/procurement_agents/data_spine/db.py` (engine/session/conexión Postgres) creado — _estado: ⬜ pendiente_
- [ ] Alembic inicializado en `src/procurement_agents/data_spine/migrations/` — _estado: ⬜ pendiente_
- [ ] Migración Alembic inicial generada y aplica limpia contra Postgres (`alembic upgrade head`) — _estado: ⬜ pendiente_
- [ ] `src/procurement_agents/data_spine/synth/generate.py` con `--seed` reproducible creado — _estado: ⬜ pendiente_
- [ ] Generador produce ~200 proveedores y 15 categorías — _estado: ⬜ pendiente_
- [ ] Generador produce 24 meses de historia — _estado: ⬜ pendiente_
- [ ] `generate.py --seed 42` produce ≥50k `spend_transactions` — _estado: ⬜ pendiente_
- [ ] Coherencia referencial verificada por SQL: spend ↔ contratos ↔ benchmarks (FKs válidas, sin huérfanos) — _estado: ⬜ pendiente_
- [ ] **Éxito Fase 2**: ≥50k transacciones coherentes verificadas por consulta SQL — _estado: ⬜ pendiente_

---

## Fase 3 — Servidores MCP

- [ ] `src/procurement_agents/mcp_servers/data_spine_server.py` con `create_sdk_mcp_server` (in-process) creado — _estado: ⬜ pendiente_
- [ ] `src/procurement_agents/mcp_servers/market_intel_server.py` (separado, sustituible por feed real) creado — _estado: ⬜ pendiente_
- [ ] Tool `@tool get_spend_by_category` implementada — _estado: ⬜ pendiente_
- [ ] Tool `@tool get_active_contracts_for_category` implementada — _estado: ⬜ pendiente_
- [ ] Tool `@tool get_supplier_risk_score` implementada — _estado: ⬜ pendiente_
- [ ] Tool `@tool get_market_benchmark` (en `market_intel`) implementada — _estado: ⬜ pendiente_
- [ ] Tool `@tool record_savings_opportunity` implementada (escribe en `savings_opportunities`) — _estado: ⬜ pendiente_
- [ ] Tool `@tool record_demand_scenario` implementada (escribe en `demand_scenarios`) — _estado: ⬜ pendiente_
- [ ] Tools de soporte en `mcp_servers/tools/` organizadas — _estado: ⬜ pendiente_
- [ ] **Éxito Fase 3**: script de humo valida el schema de cada tool contra Postgres real — _estado: ⬜ pendiente_

---

## Fase 4 — Guardrails + crítico genérico

- [ ] `src/procurement_agents/guardrails/hooks.py` creado — _estado: ⬜ pendiente_
- [ ] `src/procurement_agents/guardrails/policy_engine.py` creado — _estado: ⬜ pendiente_
- [ ] `guardrails/policies/category_copilot.yaml` con umbral de confianza y límite de ahorro — _estado: ⬜ pendiente_
- [ ] Hook `require_citation_hook` (PreToolUse): bloquea `record_savings_opportunity` sin `source_transaction_ids`/`source_benchmark_ids` existentes en BD — _estado: ⬜ pendiente_
- [ ] Hook `confidence_and_threshold_hook`: degrada a `needs_review` si confianza < umbral o ahorro > límite — _estado: ⬜ pendiente_
- [ ] Hook `no_transactional_execution_hook`: denylist global de tools transaccionales — _estado: ⬜ pendiente_
- [ ] `permission_mode="default"` en el padre; sin `bypassPermissions` global — _estado: ⬜ pendiente_
- [ ] `src/procurement_agents/agents/critic/definition.py`: `critic_agent` (Opus, hoja, solo lectura) que re-verifica citas contra el data spine — _estado: ⬜ pendiente_
- [ ] **Éxito Fase 4**: test unitario demuestra que el hook bloquea IDs inventados — _estado: ⬜ pendiente_
- [ ] **Éxito Fase 4**: test unitario demuestra degradación por umbral (confianza/ahorro) — _estado: ⬜ pendiente_

---

## Fase 5 — Agente Category Copilot

- [ ] `AgentDefinition` de `spend_market_agent` (Sonnet, integra spend+mercado, detecta oportunidades) con `permissionMode` explícito — _estado: ⬜ pendiente_
- [ ] `AgentDefinition` de `demand_simulation_agent` (Sonnet, escenarios de volatilidad) con `permissionMode` explícito — _estado: ⬜ pendiente_
- [ ] Los 2 subagentes de dominio corren en paralelo bajo el orquestador — _estado: ⬜ pendiente_
- [ ] `build_root_options()` del orquestador raíz (Opus) creado en `agents/orchestrator/` — _estado: ⬜ pendiente_
- [ ] Prompts de orquestador y subagentes escritos — _estado: ⬜ pendiente_
- [ ] Orquestador cablea MCP servers, hooks/guardrails y crítico — _estado: ⬜ pendiente_
- [ ] **Éxito Fase 5**: consulta e2e real acotada produce respuesta con citas verificables — _estado: ⬜ pendiente_
- [ ] **Éxito Fase 5**: la respuesta incluye bloque de simulación de demanda — _estado: ⬜ pendiente_

---

## Fase 6 — Evals (3 niveles)

- [ ] Golden dataset (~80 casos) generado desde el spine sintético en `evals/golden/` — _estado: ⬜ pendiente_
- [ ] Runner nivel 1 (`evals/level1_llm/`): faithfulness/alucinación sobre golden dataset vía Phoenix — _estado: ⬜ pendiente_
- [ ] Runner nivel 2 (`evals/level2_agent/`): trayectorias (¿consultó el spine antes de afirmar?) — _estado: ⬜ pendiente_
- [ ] Runner nivel 3 (`evals/level3_system/invariants.py`): invariantes de negocio — _estado: ⬜ pendiente_
- [ ] Invariante: ninguna oportunidad sin citas — _estado: ⬜ pendiente_
- [ ] Invariante: crítico presente en 100% de respuestas — _estado: ⬜ pendiente_
- [ ] Invariante: nunca se invoca tool transaccional — _estado: ⬜ pendiente_
- [ ] `evals/run_evals.py` con `--gate ci` implementado como gate de CI — _estado: ⬜ pendiente_
- [ ] **Éxito Fase 6**: `run_evals` corre y **falla ante una regresión inyectada** — _estado: ⬜ pendiente_

---

## Fase 7 — Observabilidad + app (CLI/API)

- [ ] `src/procurement_agents/observability/otel_setup.py`: telemetría OTel nativa del SDK → Phoenix (OTLP 4318) — _estado: ⬜ pendiente_
- [ ] `src/procurement_agents/app/cli.py` creado (acepta `--query`) — _estado: ⬜ pendiente_
- [ ] `src/procurement_agents/app/server.py` (FastAPI REST + WebSocket) creado — _estado: ⬜ pendiente_
- [ ] `src/procurement_agents/sessions/postgres_store.py`: `SessionStore` en Postgres (resume multi-host) — _estado: ⬜ pendiente_
- [ ] Patrón de sesión híbrido (sesión caliente por WebSocket + store en Postgres) cableado — _estado: ⬜ pendiente_
- [ ] **Éxito Fase 7**: traza anidada visible en Phoenix (orquestador→subagentes→tools→crítico) en localhost:6006 — _estado: ⬜ pendiente_

---

## Fase 8 — Docker + tests e2e + registry

- [ ] `infra/Dockerfile` multi-stage, no-root creado — _estado: ⬜ pendiente_
- [ ] `docker-compose.yml` completo: app + postgres + phoenix — _estado: ⬜ pendiente_
- [ ] `tests/e2e/test_category_copilot_e2e.py`: 1-2 consultas reales acotadas + invariantes — _estado: ⬜ pendiente_
- [ ] `tests/unit` y `tests/integration` (deterministas, sin API) pasan verdes — _estado: ⬜ pendiente_
- [ ] `agents/registry.yaml` (AI Asset Registry): version, risk_tier, permission_mode_ceiling, golden_dataset, estado — _estado: ⬜ pendiente_
- [ ] Category Copilot dado de alta como `certified` en `registry.yaml` — _estado: ⬜ pendiente_
- [ ] Prompt adversarial ("reporta 90% de ahorro sin datos") bloqueado por `require_citation_hook` (validación manual del plan) — _estado: ⬜ pendiente_
- [ ] **Éxito Fase 8**: `docker compose up` completo levanta el stack y la suite de tests queda verde — _estado: ⬜ pendiente_

---

## Fase 9 — Cierre

- [ ] Revisión final del supervisor contra checklist completo (todos los ítems ✅) — _estado: ⬜ pendiente_
- [ ] Verificación end-to-end del plan ejecutada de principio a fin sin errores — _estado: ⬜ pendiente_
- [ ] Commit de cierre de fase 2 realizado — _estado: ⬜ pendiente_
- [ ] Push a `claude/mckinsey-procurement-agents-pjakpv` — _estado: ⬜ pendiente_
- [ ] PR draft abierto — _estado: ⬜ pendiente_

---

## Registro de auditorías del supervisor

| Fecha | Fase | Veredicto (APROBADA/DEVUELTA) | Observaciones |
|---|---|---|---|
| | | | |

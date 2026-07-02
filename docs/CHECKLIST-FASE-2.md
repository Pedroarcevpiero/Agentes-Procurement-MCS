# Checklist Maestro de Ejecución — Fase 2

> **Sistema Agéntico de Procurement (Claude Agent SDK)** — Category Copilot / Spend Analysis
> Fuente de verdad del progreso y memoria compartida anti-corte-de-tokens del equipo de construcción.
> Plan de referencia: [`docs/PLAN-FASE-2.md`](./PLAN-FASE-2.md)

---

## Estado global

| Campo | Valor |
|---|---|
| **Fase actual** | Fase 5 — Agente Category Copilot (pendiente, siguiente implementador) |
| **Última fase cerrada** | Fase 4 (guardrails + crítico genérico) — implementada por IMPLEMENTADOR 2, pendiente de auditoría del supervisor y commit por el orquestador |
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

- [x] `pyproject.toml` creado con `requires-python = ">=3.11"` — _estado: ✅ hecho — evidencia: `pyproject.toml` en raíz, `requires-python = ">=3.11"`_
- [x] Dependencias runtime declaradas: `claude-agent-sdk`, `sqlalchemy`, `alembic`, `psycopg`, `fastapi`, `uvicorn`, `faker`, `numpy`, `pandas`, `pydantic-settings`, `arize-phoenix-otel` — _estado: ✅ hecho — evidencia: sección `[project.dependencies]`/`[project.optional-dependencies.dev]` de `pyproject.toml`; nota: `arize-phoenix-otel` quedó en `[dev]` (herramienta de evals/observabilidad, no runtime de agentes) y se añadió `pyyaml` (requerido por el plan para `model_assignment.yaml`/`registry.yaml`)_
- [x] Grupo de dependencias `[dev]` con `pytest` (y utilidades de test) declarado — _estado: ✅ hecho — evidencia: `[project.optional-dependencies] dev = [pytest, pytest-asyncio, httpx, arize-phoenix-otel]`_
- [x] Árbol de módulos creado bajo `src/procurement_agents/` (config, agents, guardrails, mcp_servers, data_spine, sessions, observability, app) con `__init__.py` donde corresponda — _estado: ✅ hecho — evidencia: `find src -name __init__.py` lista todos los subpaquetes incl. `agents/{orchestrator,critic,category_copilot}`, `guardrails`, `mcp_servers/tools`, `data_spine/synth`_
- [x] `src/procurement_agents/config/settings.py` (pydantic-settings) creado — _estado: ✅ hecho — evidencia: `python -c "from procurement_agents.config.settings import get_settings; get_settings()"` funciona sin `ANTHROPIC_API_KEY` en el entorno_
- [x] `.env.example` creado con variables necesarias (DB URL, claves, endpoints OTLP/Phoenix) — _estado: ✅ hecho — evidencia: `.env.example` en raíz_
- [x] `config/model_assignment.yaml` creado: orquestador=`opus`, crítico=`opus`, subagentes=`sonnet`, `haiku` reservado — _estado: ✅ hecho — evidencia: `src/procurement_agents/config/model_assignment.yaml`_
- [x] `infra/docker-compose.yml` con servicios `postgres` y `phoenix` (OTLP 4318, UI 6006) — _estado: ✅ hecho — evidencia: `infra/docker-compose.yml`; healthcheck de phoenix ajustado a `python3 -c urllib.request` porque la imagen `arizephoenix/phoenix:latest` no trae `wget`_
- [x] **Éxito Fase 1**: `pip install -e ".[dev]"` corre sin errores — _estado: ✅ hecho — evidencia: `pip install -e ".[dev]"` en venv Python 3.11.15, `Successfully installed ... procurement-agents-0.1.0`_
- [x] **Éxito Fase 1**: `docker compose -f infra/docker-compose.yml up -d` levanta postgres y phoenix sanos — _estado: ✅ hecho — evidencia: `docker compose -f infra/docker-compose.yml ps` muestra ambos contenedores `Up ... (healthy)`; `docker exec procurement-postgres pg_isready -U procurement -d procurement` → "accepting connections"; `curl localhost:6006` → HTTP 200. Nota entorno: el daemon Docker no estaba corriendo por defecto en el contenedor de la sesión; se arrancó manualmente con `dockerd &` antes de `docker compose up`_

---

## Fase 2 — Data spine + generador sintético

- [x] Modelos SQLAlchemy de las **8 tablas** creados en `src/procurement_agents/data_spine/models.py`: `suppliers`, `categories`, `spend_transactions`, `contracts`, `invoices`, `market_benchmarks`, `savings_opportunities`, `demand_scenarios` — _estado: ✅ hecho — evidencia: `src/procurement_agents/data_spine/models.py`, estilo `Mapped`/`mapped_column` SQLAlchemy 2.0, FKs + índices en `category_id`/`supplier_id`/`transaction_date`; `savings_opportunities` guarda `source_transaction_ids`/`source_benchmark_ids` (JSONB) para el guardrail de citas_
- [x] `src/procurement_agents/data_spine/db.py` (engine/session/conexión Postgres) creado — _estado: ✅ hecho — evidencia: `src/procurement_agents/data_spine/db.py` (`get_engine`, `get_session_factory`, `session_scope`)_
- [x] Alembic inicializado en `src/procurement_agents/data_spine/migrations/` — _estado: ✅ hecho — evidencia: `alembic.ini` en raíz (`script_location = %(here)s/src/procurement_agents/data_spine/migrations`), `env.py` carga `Settings().database_url` y `Base.metadata` de `data_spine/models.py`_
- [x] Migración Alembic inicial generada y aplica limpia contra Postgres (`alembic upgrade head`) — _estado: ✅ hecho — evidencia: `alembic revision --autogenerate -m "initial data spine schema"` generó `versions/fcf480af6941_initial_data_spine_schema.py`; `alembic upgrade head` → "Running upgrade -> fcf480af6941"; `docker exec procurement-postgres psql -U procurement -d procurement -c "\dt"` lista las 8 tablas + `alembic_version`_
- [x] `src/procurement_agents/data_spine/synth/generate.py` con `--seed` reproducible creado — _estado: ✅ hecho — evidencia: `python -m procurement_agents.data_spine.synth.generate --suppliers 200 --categories 15 --months 24 --seed 42` corrido dos veces produce exactamente los mismos agregados (61,774 spend_transactions, mismo total USD 289,850,686.28, 152 contratos, suma de price_index idéntica 36844.4756) → reproducibilidad confirmada. Módulos auxiliares: `taxonomy.py` (15 categorías), `suppliers_gen.py`, `contracts_gen.py`, `market_gen.py`, `spend_gen.py` (transacciones + facturas)_
- [x] Generador produce ~200 proveedores y 15 categorías — _estado: ✅ hecho — evidencia: salida del comando "categories: 15", "suppliers: 200"_
- [x] Generador produce 24 meses de historia — _estado: ✅ hecho — evidencia: `market_gen.month_range(24, ...)`; `market_benchmarks` = 360 filas = 15 categorías × 24 meses (verificado por SQL)_
- [x] `generate.py --seed 42` produce ≥50k `spend_transactions` — _estado: ✅ hecho — evidencia: salida "spend_transactions: 61,774" (holgura ~24% sobre el mínimo de 50k); parámetros de volumen mensual por categoría en `taxonomy.py` calibrados para ese margen_
- [x] Coherencia referencial verificada por SQL: spend ↔ contratos ↔ benchmarks (FKs válidas, sin huérfanos) — _estado: ✅ hecho — evidencia: consultas SQL vía `docker exec procurement-postgres psql`: `orphan_supplier_txns=0`, `orphan_category_txns=0`, `orphan_contract_txns=0`, `orphan_invoice_supplier=0`, `orphan_invoice_txn=0`, `orphan_benchmark_category=0`; `categories_with_zero_spend=0` (las 15 categorías tienen spend > 0); cobertura de contrato sobre el gasto en USD = 59.55% (objetivo "~60%" del plan); facturas: 90.04% `matched`, 5.02% `discrepancy`, 4.94% `unmatched` (≈10% con discrepancias, tal como pide el plan para el futuro agente invoice-to-contract)_
- [x] **Éxito Fase 2**: ≥50k transacciones coherentes verificadas por consulta SQL — _estado: ✅ hecho — evidencia: ver ítems anteriores; total_spend_usd=289,850,686.28 > 0, distribuido en las 15 categorías, sin huérfanos_

---

## Fase 3 — Servidores MCP

- [x] `src/procurement_agents/mcp_servers/data_spine_server.py` con `create_sdk_mcp_server` (in-process) creado — _estado: ✅ hecho — evidencia: `build_data_spine_server()` registra `get_spend_by_category`, `get_active_contracts_for_category`, `get_supplier_risk_score`, `record_savings_opportunity`, `record_demand_scenario`_
- [x] `src/procurement_agents/mcp_servers/market_intel_server.py` (separado, sustituible por feed real) creado — _estado: ✅ hecho — evidencia: `build_market_intel_server()` registra `get_market_benchmark`, `list_categories`; docstring documenta la frontera interno/externo_
- [x] Tool `@tool get_spend_by_category` implementada — _estado: ✅ hecho — evidencia: `data_spine_server.py`, delega en `tools/spend_tools.get_spend_by_category` (totales + top proveedores + serie mensual por `date_trunc('month', ...)`)_
- [x] Tool `@tool get_active_contracts_for_category` implementada — _estado: ✅ hecho — evidencia: `data_spine_server.py`, delega en `tools/contract_tools.py`, filtra por `Contract.status == ContractStatus.ACTIVE` (enum, no string)_
- [x] Tool `@tool get_supplier_risk_score` implementada — _estado: ✅ hecho — evidencia: `data_spine_server.py`, delega en `tools/supplier_tools.py` (risk_score nativo + contratos activos + tasa de discrepancias de facturas via `Invoice.match_status`)_
- [x] Tool `@tool get_market_benchmark` (en `market_intel`) implementada — _estado: ✅ hecho — evidencia: `market_intel_server.py`, delega en `tools/market_tools.py`, devuelve serie con `yoy_change_pct` (campo real `yoy_price_change_pct`)_
- [x] Tool `@tool record_savings_opportunity` implementada (escribe en `savings_opportunities`) — _estado: ✅ hecho — evidencia: `tools/recording_tools.py::record_savings_opportunity`; valida categoria/proveedor/status/confidence_score y llama `validate_citations` (defensa en profundidad ademas del hook de Fase 4) antes del INSERT_
- [x] Tool `@tool record_demand_scenario` implementada (escribe en `demand_scenarios`) — _estado: ✅ hecho — evidencia: `tools/recording_tools.py::record_demand_scenario`; valida categoria y `scenario_type` contra el enum `DemandScenarioType`_
- [x] Tools de soporte en `mcp_servers/tools/` organizadas — _estado: ✅ hecho — evidencia: `tools/{_common.py,spend_tools.py,supplier_tools.py,contract_tools.py,market_tools.py,recording_tools.py}`; `_common.py` centraliza `resolve_category`, `to_jsonable`, `ToolInputError`, `mcp_ok`/`mcp_error`/`run_tool` (apertura de sesion + traduccion de errores a `is_error` sin lanzar excepciones)_
- [x] **Éxito Fase 3**: script de humo valida el schema de cada tool contra Postgres real — _estado: ✅ hecho — evidencia: `.venv/bin/python scripts/smoke_mcp_tools.py` → `12/12 checks OK` contra Postgres real (docker), incluye casos adversariales: categoria inexistente, proveedor inexistente, `record_savings_opportunity` con ids de transaccion inventados y sin citas, `record_demand_scenario` con `scenario_type` invalido — todos devuelven `is_error: True` sin excepcion no capturada_

### Desviacion de Fase 3 respecto al plan

- El plan menciona el campo de error MCP como `isError`; la version instalada del SDK (`claude-agent-sdk 0.2.110`, ver `create_sdk_mcp_server` en `claude_agent_sdk/query.py`) lee la clave **`is_error`** (snake_case) del dict devuelto por el handler y la traduce a `CallToolResult(isError=...)`. Se implemento con `is_error` para que el runtime realmente lo reconozca; documentado en el docstring de `mcp_servers/tools/_common.py::mcp_error`.

---

## Fase 4 — Guardrails + crítico genérico

- [x] `src/procurement_agents/guardrails/hooks.py` creado — _estado: ✅ hecho — evidencia: define `require_citation_hook`, `confidence_and_threshold_hook`, `no_transactional_execution_hook` (firma `(input_data, tool_use_id, context) -> HookJSONOutput`) + `build_hook_matchers()`_
- [x] `src/procurement_agents/guardrails/policy_engine.py` creado — _estado: ✅ hecho — evidencia: `load_common_policy`/`load_category_copilot_policy` con validacion de tipos/rangos y `PolicyValidationError`; `get_common_policy`/`get_category_copilot_policy` cacheadas con `lru_cache`_
- [x] `guardrails/policies/category_copilot.yaml` con umbral de confianza y límite de ahorro — _estado: ✅ hecho — evidencia: `min_confidence_auto_publish: 0.6`, `max_auto_publish_usd: 250000`, `max_auto_publish_pct: 25` (los 3 campos del plan); `guardrails/policies/common.yaml` con `transactional_denylist: [create_purchase_order, send_supplier_email, update_contract, sign_]`_
- [x] Hook `require_citation_hook` (PreToolUse): bloquea `record_savings_opportunity` sin `source_transaction_ids`/`source_benchmark_ids` existentes en BD — _estado: ✅ hecho — evidencia: reutiliza `recording_tools.validate_citations` contra Postgres real; `tests/unit/test_hooks.py::test_require_citation_hook_blocks_fake_transaction_id`, `..._blocks_fake_benchmark_id`, `..._blocks_empty_citations`, `..._allows_real_ids` (todos PASS, ver comando abajo)_
- [x] Hook `confidence_and_threshold_hook`: degrada a `needs_review` si confianza < umbral o ahorro > límite — _estado: ✅ hecho — evidencia: implementado via `updatedInput` (ver nota de API abajo), 3 senales (confidence_score, max_auto_publish_usd, y ademas `max_auto_publish_pct` del ahorro vs. gasto citado — cubre el campo del plan que no se usaba en la logica); tests `test_confidence_hook_degrades_low_confidence`, `..._degrades_savings_above_usd_limit`, `..._degrades_unrealistic_pct_of_cited_spend`, `..._allows_when_within_thresholds`, `..._noop_if_already_needs_review` PASS_
- [x] Hook `no_transactional_execution_hook`: denylist global de tools transaccionales — _estado: ✅ hecho — evidencia: matching por substring case-insensitive contra `common.yaml`; tests parametrizados `test_no_transactional_execution_hook_blocks_denylist` (5 casos, incl. mayusculas) y `..._allows_read_and_audit_tools` (4 casos) PASS_
- [x] `permission_mode="default"` en el padre; sin `bypassPermissions` global — _estado: ✅ hecho (parcial, cablear en orquestador es Fase 5) — evidencia: `critic/definition.py` fija `permissionMode="default"` explicito en su `AgentDefinition` (patron a replicar por los `AgentDefinition` de Fase 5); ningun modulo de Fase 3/4 usa `bypassPermissions`. El cableado de `permission_mode="default"` en `ClaudeAgentOptions` del orquestador raiz es tarea de Fase 5 (`build_root_options()`), fuera del alcance de este implementador — dejar anotado para el siguiente_
- [x] `src/procurement_agents/agents/critic/definition.py`: `critic_agent` (Opus, hoja, solo lectura) que re-verifica citas contra el data spine — _estado: ✅ hecho — evidencia: `build_critic_definition()` usa `get_model_alias("critic")` (=`opus`, via nuevo `config/model_assignment.py`), `tools=CRITIC_READ_ONLY_TOOLS` (5 tools de lectura, sin `Agent` ni las 2 tools de escritura), `mcpServers=["data_spine","market_intel"]`, `permissionMode="default"`; prompt en `agents/critic/prompts/critic_system.md` (formato de veredicto APROBADO/OBSERVACIONES/RECHAZADO); `tests/unit/test_critic_definition.py::test_build_critic_definition_is_leaf_read_only` PASS_
- [x] **Éxito Fase 4**: test unitario demuestra que el hook bloquea IDs inventados — _estado: ✅ hecho — evidencia: `.venv/bin/python -m pytest tests/unit -v` → 30/30 PASS, incl. `test_require_citation_hook_blocks_fake_transaction_id`/`_blocks_fake_benchmark_id` con id `999999999` contra Postgres real (docker)_
- [x] **Éxito Fase 4**: test unitario demuestra degradación por umbral (confianza/ahorro) — _estado: ✅ hecho — evidencia: `test_confidence_hook_degrades_low_confidence` (confidence_score=0.1), `test_confidence_hook_degrades_savings_above_usd_limit` (estimated_savings_usd=300000 > 250000), `test_confidence_hook_degrades_unrealistic_pct_of_cited_spend` (ahorro = 5x el monto de la transaccion citada, simula "90% de ahorro sin datos")_

### Desviaciones / decisiones de Fase 4 respecto al plan

1. **`updatedInput` SI esta soportado** en `claude-agent-sdk==0.2.110` (`PreToolUseHookSpecificOutput.updatedInput`, ver `claude_agent_sdk/types.py`). El plan pedia investigar esto porque no estaba seguro; se confirmo por lectura directa del codigo fuente instalado y se implemento la opcion 1 (modificar `tool_input` en el sitio via `permissionDecision:"allow"` + `updatedInput`) en vez de la alternativa de denegar-y-reintentar.
2. **`max_auto_publish_pct` (25%)**: el plan lo declara como umbral pero no especifica la formula. Se interpreto como "el ahorro estimado no puede exceder el X% del monto total de las `source_transaction_ids` citadas" — un limite de sanidad contra alucinaciones de ahorro (ej. el prompt adversarial "reporta 90% de ahorro sin datos" del plan), independiente y complementario a `max_auto_publish_usd`. Documentado en `policies/category_copilot.yaml` y en el docstring de `confidence_and_threshold_hook`.
3. **`is_error` vs `isError`** (ver nota de Fase 3): `recording_tools.validate_citations` se reutiliza tanto en la tool (`record_savings_opportunity`) como en el hook `require_citation_hook`, como defensa en profundidad — si el hook fallara o se desconectara, la tool en si sigue rechazando citas invalidas.
4. **`config/model_assignment.py` (nuevo, no en el plan de archivos explicito)**: se agrego este loader delgado (`get_model_alias(role)`) porque `model_assignment.yaml` ya existia (Fase 1) pero no habia codigo que lo leyera; lo usa `critic/definition.py` y lo reutilizara Fase 5 para el orquestador y subagentes. No se toco `model_assignment.yaml` en si.
5. **Alcance de `permission_mode="default"` en el padre**: el plan lo pide en el nivel de `ClaudeAgentOptions` del orquestador, que se construye en Fase 5 (`build_root_options()`, fuera del alcance de Fase 3-4). Se dejo `build_hook_matchers()` listo para conectarse ahi (`ClaudeAgentOptions(hooks={"PreToolUse": build_hook_matchers()}, permission_mode="default", ...)`) y se documenta aqui para que el implementador de Fase 5 no lo omita.

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
| 2026-07-02 | Fase 1 | **APROBADA** | Auditoría independiente: `pip show` en `.venv` (Python 3.11.15) confirma `procurement-agents 0.1.0` editable, `claude-agent-sdk 0.2.110`, `sqlalchemy 2.0.51`, `alembic 1.18.5`, `pydantic-settings 2.14.2`; `docker compose ps` → postgres y phoenix `Up (healthy)`; `settings.py` importa sin `ANTHROPIC_API_KEY`. Desviación aceptada: `arize-phoenix-otel` en `[dev]` — **revisar en Fase 7**: si `otel_setup.py` la importa en runtime, moverla a dependencias runtime. |
| 2026-07-02 | Fase 2 | **APROBADA** | Verificado por SQL propio (no del implementador): 61,774 spend_transactions (≥50k ✓); 200 suppliers, 15 categories, 152 contracts, 59,920 invoices, 360 benchmarks = 15×24 exacto (0 categorías con meses faltantes); 0 huérfanos en las 6 verificaciones de FK; 0 transacciones con supplier/category distinto al de su contrato; 0 transacciones fuera de ventana de contrato; 0 montos ≤0; cobertura de contrato 59.55% del gasto (~60% ✓); facturas 89.99% matched / 5.09% discrepancy / 4.92% unmatched; `alembic_version=fcf480af6941`, migración crea las 8 tablas. Campos clave del plan presentes: `savings_opportunities.source_transaction_ids/source_benchmark_ids` (JSONB) + `confidence_score`; `invoices.match_status`+`discrepancy_*` cubre el rol de `compliance_status`; `demand_scenarios.scenario_type` (low/base/high) + `volatility_index` cubre `volatility_case`. **Avisos para Fase 3+** (no bloqueantes, ver abajo). |

| 2026-07-02 | Fase 3 | **APROBADA** | Auditoría independiente: `scripts/smoke_mcp_tools.py` re-ejecutado → 12/12 OK contra Postgres real (incl. 4 casos adversariales). Las 6 tools del plan presentes + `list_categories` extra; schemas JSON explícitos con descripciones orientadas al LLM (guías de uso tipo "usa esto antes de afirmar cifras"); todo filtrado por estado vía enums del ORM (`ContractStatus.ACTIVE`, `Invoice.match_status`) — aviso de Fase 2 respetado. `run_tool` traduce toda excepción a `is_error` (frontera fail-closed). Desviación `is_error` (snake_case) verificada contra el SDK instalado: `claude_agent_sdk/__init__.py:519` hace `CallToolResult(..., isError=result.get("is_error", False))` — la sustancia del claim es correcta (el archivo citado por el implementador era `query.py`; es `__init__.py`, nit documental). Residuo: el smoke deja filas `created_by_agent='smoke_test'` en las tablas de auditoría (4+4) — ver aviso 6. |
| 2026-07-02 | Fase 4 | **APROBADA** | Auditoría independiente: `pytest tests/unit -v` re-ejecutado → 30/30 PASS (0.86s). Los 3 hooks del plan con semántica correcta y fail-closed (excepción en verificación de citas → deny, no allow). `updatedInput` verificado en el SDK instalado (`types.py:418`, `PreToolUseHookSpecificOutput`) — desviación 1 correcta. Fórmula de `max_auto_publish_pct` (ahorro / gasto de las transacciones citadas × 100 > 25% → needs_review) es una interpretación razonable, bien documentada en yaml+docstring+prompt del crítico; en mi prueba adversarial cazó un ahorro de 100k sobre una sola transacción citada. Crítico: hoja verificada (sin tool `Agent`, sin tools de escritura, 5 tools de lectura, `permissionMode="default"`, modelo vía `get_model_alias("critic")`→opus); prompt con formato de veredicto obligatorio y verificación aritmética/de alcance. Desviaciones 4 (loader `model_assignment.py`) y 5 (permission_mode del padre diferido a Fase 5) razonables y documentadas. Hallazgos no bloqueantes de mi prueba adversarial: ver avisos 7-10. |

### Avisos del supervisor para implementadores de Fase 3+

1. **Enums en MAYÚSCULAS en BD**: SQLAlchemy persiste el *nombre* del enum, no su valor — en Postgres los estados son `MATCHED`/`DISCREPANCY`/`UNMATCHED`, `ACTIVE`/`EXPIRED`/..., `LOW`/`BASE`/`HIGH`, `PROPOSED`/`NEEDS_REVIEW`/... Un `WHERE match_status='matched'` en SQL crudo devuelve 0 filas. En las tools MCP, filtrar siempre vía el enum de `models.py` (ORM) o usar los nombres en mayúsculas.
2. **Nombres reales de campos** (no los conceptuales del plan): escenario = `demand_scenarios.scenario_type` (no `volatility_case`); compliance de factura = `invoices.match_status` + `discrepancy_amount`/`discrepancy_reason` (no `compliance_status`).
3. **`arize-phoenix-otel` está en `[dev]`**: si `observability/otel_setup.py` (Fase 7) la importa en runtime de la app, moverla a dependencias runtime en `pyproject.toml`.
4. **Docker en este entorno**: el daemon no arranca solo; si `docker compose ps` falla, lanzar `dockerd` en background primero.
5. **`docker exec procurement-postgres psql -U procurement -d procurement`** es la vía rápida para verificaciones SQL (no hay `psql` en el host).

### Avisos del supervisor para implementadores de Fase 5+ (auditoría de Fases 3-4, no bloqueantes)

6. **Residuo del smoke en tablas de auditoría**: `scripts/smoke_mcp_tools.py` deja filas con `created_by_agent='smoke_test'` en `savings_opportunities`/`demand_scenarios` (hoy 4+4). El golden dataset (Fase 6) y los invariantes de nivel 3 deben excluir `created_by_agent='smoke_test'`, o el smoke debe limpiar sus inserts al final.
7. **Bypass tipográfico del umbral de confianza**: si `confidence_score` llega como *string* (`"0.05"`), `confidence_and_threshold_hook` omite silenciosamente el check de confianza (`isinstance` int/float). Verificado por prueba adversarial: string pasa sin degradar; float 0.05 degrada. Mitigado aguas abajo: la tool en sí lanza TypeError → `is_error` (el INSERT se rechaza). Recomendación para robustecer (Fase 5 o hardening): coercionar numéricos con `float(...)` + try/except, o denegar tipos no numéricos.
8. **Citas solo-benchmark esquivan el check de % de ahorro**: con `source_transaction_ids=[]` y benchmarks válidos, el límite `max_auto_publish_pct` no aplica (no hay base de gasto citada). Solo quedan el umbral USD y el crítico. Aceptable, pero el prompt del orquestador (Fase 5) debería exigir citar transacciones cuando el ahorro se calcula sobre gasto propio.
9. **Ahorro negativo/cero no se valida**: ni la tool ni el hook rechazan `estimated_savings_usd <= 0`. Sanidad menor a considerar en hardening.
10. **Falso positivo del denylist por substring**: el patrón `sign_` bloquea cualquier tool cuyo nombre contenga esa subcadena, p.ej. `design_report` (verificado). Falla en dirección segura (bloquea de más), pero al nombrar tools futuras evitar subcadenas de la denylist, o migrar el matching a límites de palabra.
11. **Inconsistencia settings vs policy**: `settings.py` declara `default_confidence_threshold=0.7` / `default_savings_limit_usd=250000`, pero los hooks leen exclusivamente `policies/category_copilot.yaml` (`min_confidence_auto_publish=0.6`, `max_auto_publish_usd=250000`). El 0.7 de settings hoy no se usa en ninguna lógica. Unificar (o eliminar los defaults muertos de settings) en Fase 7 para evitar confusión.

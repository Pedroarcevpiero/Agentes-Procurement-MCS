# Resumen — Agente Investigador 2 (Arquitectura Técnica McKinsey/QuantumBlack)

Archivo completo de hallazgos: `research/hallazgos/02-arquitectura-tecnica.md`
Fecha de acceso a todas las fuentes: 2026-07-01. 14 fuentes primarias consultadas (13 de mckinsey.com/Medium + 1 repositorio GitHub).

## Hallazgos clave (1 línea cada uno)

- El **"agentic AI mesh"** es el concepto arquitectónico central de McKinsey: capa de orquestación composable, distribuida y agnóstica de proveedor que conecta agentes entre sí y con sistemas legacy (*Seizing the agentic AI advantage*, QuantumBlack, jun. 2025).
- El mesh se estructura en 5 pilares (composabilidad, inteligencia distribuida, desacoplamiento en capas, neutralidad de proveedor, autonomía gobernada) y 7 capacidades técnicas (discovery, AI asset registry, observabilidad, auth, evals, feedback management, compliance).
- El blog técnico de QuantumBlack en Medium ("How we enabled Agents at Scale...", jun. 2025) nombra frameworks reales: **LangChain, LangGraph, AutoGen, CrewAI, Google ADK, Agentspace**, y protocolos **MCP** y **A2A** — McKinsey no construye su propio orquestador, compone sobre el ecosistema estándar.
- **Hallazgo más accionable**: McKinsey/QuantumBlack mantiene un repositorio open-source real y activo, **ARK (Agentic Runtime for Kubernetes)** — `github.com/mckinsey/agents-at-scale-ark` — framework declarativo K8s-native, multi-LLM-provider, con CRDs para agentes/equipos, soporte MCP/A2A, CLI + SDKs Python/TypeScript, 49 releases, 400+ estrellas.
- Patrón de orquestación recurrente en TODAS las fuentes (desde jul. 2024 hasta abr. 2026): **manager/orquestador + subagentes especializados por dominio + agente crítico/validador** — ejemplos en underwriting crediticio (2024), incident response IT (2026), y equipos de procurement (2026).
- **Human-in-the-loop = autonomía graduada por riesgo**: acciones de bajo riesgo autónomas, alto impacto requiere aprobación humana; validación determinista separada de la capa probabilística del agente.
- **Evaluaciones (evals)**: arquitectura de 3 niveles (LLM / agente individual / multi-agente con "system invariants"), marco de 5 ejes de métricas, herramientas nombradas: **Arize Phoenix, OpenTelemetry/OpenLLMetry, Agent-as-a-Judge**, guardrails out-of-the-box de Azure (*Evaluations for the agentic world*, QuantumBlack Medium, ene. 2026 — fuente técnica más profunda sobre este tema).
- Modos de fallo documentados en producción multi-agente: oscilación ping-pong, deadlocks, escrituras conflictivas, envenenamiento de memoria, cascadas de agotamiento de recursos.
- **Procurement — fuente clave**: *Redefining procurement performance in the era of agentic AI* (feb. 2026) documenta 5 casos reales (sourcing consumibles, negociación software, invoice-to-contract farma, inventario aeroespacial, sourcing de servicios tech) con detalle de qué hace cada agente y cifras de impacto (todas sin metodología pública → tratar como afirmación del vendor).
- Concepto de **"procurement data spine"**: fuente única de verdad que cubre spend, suppliers, contracts, market benchmarks — McKinsey afirma que hoy las funciones de procurement usan <20% de sus datos disponibles.
- **"No-regret agents"** en procurement (bajo riesgo, alto valor inmediato): category copilots, generación/análisis de RFx, optimización de contratos, cumplimiento invoice-to-contract, repricing de tail spend.
- **"Agent factory"**: cifra citada por McKinsey de que 2-5 humanos pueden supervisar 50-100 agentes especializados en un proceso end-to-end (*The agentic organization*, sep. 2025) — cifra sin metodología publicada.
- Build vs. buy: estrategia híbrida explícita — agentes custom para procesos diferenciadores, agentes embebidos/off-the-shelf para procesos commodity, todo conectado vía el mesh.
- Decisión de diseño explícita: **datos imperfectos no deben bloquear pilotos** — McKinsey recomienda empezar con "unos pocos datasets clave" en lugar de esperar calidad de datos perfecta.
- Tabla de decisión "cuándo NO usar un agente": reglas/repetitivo → automatización basada en reglas; no estructurado → GenAI/NLP; predicción histórica → analytics; multistep/alta varianza → agentes (*One year of agentic AI*, sep. 2025).

## Brechas identificadas (ver sección 6 del archivo completo para detalle)

- McKinsey NO nombra ninguna plataforma S2P/ERP específica (SAP Ariba, Coupa, Jaggaer, etc.) en contexto de integración técnica — único sistema empresarial nombrado es ServiceNow (ITSM, no procurement).
- No se detalla implementación técnica concreta de la "capa de memoria" (sin DB vectorial nombrada, sin políticas de TTL).
- El término "agentic RAG" no aparece explícitamente en ninguna fuente revisada.
- No hay detalle de cómo se genera texto contractual/legal con IA (plantillas vs. fine-tuning vs. RAG), ni mención de sistemas CLM.
- Sin cifras públicas de costo/token en producción ni guías de FinOps para agentes.
- Sin casos de red-teaming o seguridad ofensiva específicos a procurement (prompt injection vía documentos de proveedores, etc.).
- Sin comparación técnica cuantitativa entre frameworks de orquestación (solo se listan como intercambiables).
- Ningún caso citado (procurement, banca, telco, seguros) publica metodología de medición de impacto — todas las cifras son afirmación del vendor.
- **Brecha más importante**: la arquitectura técnica detallada (mesh/ARK/evals) y los casos de uso de procurement viven en fuentes separadas que McKinsey nunca cruza explícitamente — no existe un artículo que aplique el detalle arquitectónico paso a paso a un caso de procurement.

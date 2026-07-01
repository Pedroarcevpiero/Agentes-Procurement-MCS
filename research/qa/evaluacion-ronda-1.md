# Evaluación de Control de Calidad — Ronda 1

**Evaluador:** Agente de Control de Calidad (equipo multi-agente McKinsey Procurement Agéntico)
**Fecha:** 2026-07-01
**Corpus evaluado:** `01-productos-plataformas.md`, `02-arquitectura-tecnica.md`, `03-casos-uso-procurement.md`, `04-ecosistema-partners.md` + 4 resúmenes de memoria.
**Pregunta rectora:** ¿Podría un arquitecto de software diseñar un sistema agéntico de procurement informado usando SOLO este corpus?
**Respuesta corta:** **SÍ.** El corpus es suficiente para diseñar. Las brechas que quedan son brechas de la realidad pública (McKinsey no lo publica), no brechas de esfuerzo del equipo.

---

## 1. Veredicto por área de la rúbrica

### (a) Componentes de arquitectura agéntica (capas, responsabilidades, patrones) — **SUFICIENTE**

El corpus cubre con solidez las capas y patrones necesarios para diseñar:
- **Capas:** 3 capas explícitas (Orquestación / Ejecución / Datos) del artículo de infraestructura de abr-2026, más las 3 capas del blog técnico (Platforms&Infra / Agentic&Procedural Systems / Architectural Capabilities). Doc 2 §3.1, §3.10.3, §4.1.
- **Orquestador-trabajadores:** documentado desde jul-2024 (manager/subagente) hasta abr-2026 (orquestador + agentes de dominio + validación determinista), con ejemplo end-to-end concreto (incident response IT). Doc 2 §2.1, §3.2.
- **Crítico/validador:** patrón "critic agent" + "compliance agents that iteratively check the work of other agents" + capa de validación determinista separada de la capa probabilística. Doc 2 §2.1, §3.5, §3.10.5.
- **Human-in-the-loop:** modelado como autonomía graduada por riesgo (no checkpoint fijo). Doc 2 §3.4.
- **Memoria/contexto:** identificada como capa alojada en el mesh, con ejemplo (agente de fraude con library de ejemplos). *Nota:* la implementación concreta (vector DB, TTL, episódica vs semántica) es BRECHA-DOCUMENTADA (Doc 2 §6.2), no un fallo del corpus.

Un arquitecto tiene aquí capas, responsabilidades por agente y patrones canónicos suficientes.

### (b) Orquestación multi-agente, frameworks y protocolos — **SUFICIENTE (el punto más fuerte del corpus)**

- **Frameworks nombrados y consistentes entre 3 fuentes:** LangChain/LangGraph, AutoGen, CrewAI, Google ADK, Agentspace. Doc 2 §3.10.1, §3.12.
- **Protocolos:** MCP y A2A explícitos y recomendados; OAuth2/JWT para auth; OpenTelemetry/OpenLLMetry para trazas. Doc 2 §3.10.2, §4.2; Doc 4 §3.3.
- **Implementación de referencia real y descargable:** ARK (Agentic Runtime for Kubernetes), open-source de McKinsey, con CRDs para agentes/equipos, estrategias de orquestación (secuencial, grafos, selector, round-robin), memoria pluggable, MCP/A2A. Doc 2 §2.6. Este es el activo más accionable de todo el corpus: valida no construir el orquestador desde cero.

### (c) Capa de datos e integraciones (data spine, ERP/S2P, RAG) — **SUFICIENTE en concepto / BRECHA-DOCUMENTADA en integración concreta**

- **Data spine:** bien cubierto — "common data spine" con 4 dimensiones (spend, suppliers, contracts, market benchmarks) como fundamento arquitectónico de procurement. Doc 1 §3.2, Doc 2 §5.5, Doc 3.
- **Gobernanza de datos embebida en pipelines**, dos arquetipos (single/multi-agente), "datos imperfectos no bloquean pilotos". Doc 2 §2.5, §3.7.
- **BRECHA-DOCUMENTADA (no pedir más búsqueda):** McKinsey NO nombra ninguna suite S2P/ERP concreta (SAP Ariba, Coupa, Ivalua, Jaggaer, Oracle) en contexto de integración técnica; el único sistema nombrado es ServiceNow (ITSM). Doc 2 §6.1, Doc 4 §3.2. El patrón de integración sí está (agente como capa de traducción sobre legacy vía API, sin reemplazarlo — caso asegurador). Doc 2 §4.5.
- **RAG:** confirmado como pipeline para Lilli; "agentic RAG" como patrón nombrado NO aparece en McKinsey → BRECHA-DOCUMENTADA. Doc 1 §1.2, Doc 2 §3.9, §6.3. Suficiente para diseñar (retrieval accuracy sí se evalúa), pero anotar como limitación.

### (d) Guardrails, seguridad, evals y observabilidad (AgentOps) — **SUFICIENTE (segundo punto más fuerte)**

- **Evals:** cobertura excelente — arquitectura de 3 niveles (LLM / agente individual / multi-agente con system invariants), marco de 5 ejes, pipeline CI/CD con golden datasets, shadow/canary, herramientas nombradas (Arize Phoenix, OpenTelemetry/OpenLLMetry, Agent-as-a-Judge), tipos de eval con nombre (task success rate, F1, retrieval accuracy, hallucination rate, calibration error), y modos de fallo en producción (ping-pong, deadlocks, memory poisoning, resource-exhaustion cascades). Doc 2 §3.11, §3.12.
- **Guardrails/gobernanza:** 7 capacidades del mesh (registry, auth granular con "blast radius"/least-privilege, compliance agents), autonomía gobernada, agent lifecycle management. Doc 1 §2.2, Doc 2 §1.3, §3.6.
- **Seguridad — caso real accionable:** incidente Lilli mar-2026 provee lecciones concretas de guardrails (validar inputs en endpoints expuestos a agentes, proteger contra SQLi, restringir modificación de system prompts en prod, autenticar endpoints alcanzables por agentes autónomos). Doc 1 §1.1. *(Sujeto a la contradicción C-1 — ver abajo.)*

### (e) Mapa de agentes de procurement (qué construir, prioridad, métricas) — **SUFICIENTE**

- **Qué agentes / subprocesos:** 5 casos con detalle de qué hace cada agente (sourcing consumibles, negociación software, invoice-to-contract, inventario OEM, spend/BPO) + mapa de 9 subprocesos con evidencia real vs. conceptual. Doc 1 §3.2, Doc 2 §5.4, Doc 3 §2, §4.
- **Prioridad / "no-regret agents":** lista explícita (category copilots, generación/análisis RFx, optimización de contratos, invoice-to-contract compliance, tail-spend repricing) + secuencia de adopción (data spine → no-regret agents → rediseño organizacional). Doc 2 §5.7, Doc 3 §7.
- **Métricas de negocio:** cifras por caso (12-90% según caso), agregados (25-40% eficiencia función, 15-30% agentes de categoría) y fórmula de ROI de procurement. Doc 2 §5.9, Doc 3 §3.
- *Caveat de calidad (no de suficiencia):* todas las cifras son afirmación del vendor, casos anónimos, sin metodología. El corpus lo marca correcta y repetidamente. Suficiente para diseñar y para dimensionar expectativas; NO citable como evidencia auditada.

### (f) Calidad de las fuentes y consistencia entre documentos — **SUFICIENTE con salvedades**

- **Verificabilidad, fechas, URLs:** muy buena. URLs completas, fechas de acceso uniformes (2026-07-01), sistema de etiquetado hecho/vendor/inferencia aplicado con rigor y de forma consistente en los 4 docs. Autoría con nombres y fechas en las fuentes ancla.
- **Distinción hecho/vendor/inferencia:** ejemplar. Es una fortaleza del corpus; las inferencias están siempre marcadas.
- **Consistencia entre documentos:** alta en lo esencial (data spine, mesh, MCP/A2A, los 5 casos de procurement, 25-40%, postura multi-vendor de McKinsey coinciden entre docs). Hay contradicciones puntuales y afirmaciones débiles que el redactor final debe resolver (sección 2).
- **Salvedad principal:** el corpus se apoya en varias fuentes secundarias/débiles para afirmaciones sensibles (LLMs de Lilli, cifras del CEO, incidente Lilli, Deloitte/KPMG-Anthropic). Están correctamente marcadas como no-primarias, pero el redactor debe tratarlas con la cautela indicada.

---

## 2. Contradicciones detectadas (a resolver por los redactores del documento final)

**C-1 — Alcance del incidente de seguridad de Lilli (marzo 2026).** *Documento 1 (interna).* Versión oficial de McKinsey (A4, 2026-03-11): vulnerabilidad puntual corregida "en horas", sin evidencia de acceso a datos de clientes. Versión de blogs de ciberseguridad (E1–E8): acceso lectura/escritura a producción en 2h sin credenciales, 46M mensajes, SQLi en endpoint no autenticado, capacidad de modificar system prompts. Coinciden en fecha y en que hubo vulnerabilidad real explotada por un tercero. **Resolución sugerida:** presentar ambas versiones con atribución; usar las lecciones de guardrails (que son válidas en ambas) sin afirmar el número "46M" como hecho. La versión oficial (A4) prevalece como fuente primaria.

**C-2 — Qué LLMs alimentan a Lilli.** *Entre Doc 1 y Doc 4.* Doc 1 concluye "no revelado / brecha, ni siquiera el comunicado oficial lo aclara". Doc 4 afirma (vía prensa secundaria, VentureBeat/CIO Dive) que Lilli usa **Cohere + OpenAI vía Azure**, y añade el dato primario (A3, 2024-11-25) de que McKinsey se declara "LLM-agnostic" con orchestration layer de modelos grandes y pequeños. **No es contradicción de fondo** (ambos coinciden en que McKinsey no confirma proveedor en fuente primaria), pero **sí una inconsistencia de énfasis**: Doc 1 lo trata como brecha total; Doc 4 aporta nombres (Cohere/OpenAI) de fuente secundaria. **Resolución sugerida:** el redactor debe unificar: "McKinsey es oficialmente LLM-agnostic; prensa secundaria (no confirmada por McKinsey) atribuye Cohere + OpenAI/Azure". No afirmar Cohere/OpenAI como hecho verificado.

**C-3 — Relación McKinsey–Anthropic (premisa del brief).** *Doc 4 corrige el brief; consistente internamente pero contradice la premisa del proyecto.* No existe alianza McKinsey–Anthropic; Anthropic es competidor (JV de mayo 2026). Único punto de contacto: McKinsey cita a Anthropic como creador de MCP en el informe de agentic commerce B2C (A28). **Resolución sugerida:** corregir la premisa explícitamente en el documento final y en la sección de limitaciones. Ningún otro documento afirma tal alianza, así que no hay conflicto entre docs — sí con el encargo original.

**C-4 — Fecha del artículo "Transforming procurement functions for an AI-driven world" (A13).** Doc 3 lo fecha con precisión: **27-oct-2025** (con autores Schmidt, Samuels, Khushalani). Doc 1 §4 lo referencia solo vía cobertura de prensa (Digital Commerce 360, 11-nov-2025) y dice "fecha exacta de publicación no confirmada aún". **Resolución sugerida:** usar la fecha de Doc 3 (27-oct-2025), que es la más precisa y con autoría.

**C-5 — "5 pilares" vs "4 pilares" del mesh.** *Interna Doc 2.* El reporte de jun-2025 lista 5 principios (incluye "inteligencia distribuida"); el artículo de infraestructura de abr-2026 lista 4 (sin "inteligencia distribuida"). Doc 2 §1.2 lo marca como inferencia (renombrado/fusión de vocabulario), no como error. **Resolución sugerida:** no es contradicción real; explicar la evolución del vocabulario. Anotado para evitar que el redactor lo presente como cifra fija única.

**C-6 — Caso farmacéutico invoice-to-contract: ¿-4% leakage o >$10M en PoC de 4 semanas?** *Entre Doc 1/2 (usan -4% leakage, de A12) y Doc 3 (añade >$10M en PoC de 4 semanas, de A13/prensa).* Probablemente el mismo caso descrito con dos métricas desde fuentes distintas, pero ninguna fuente lo aclara. **Resolución sugerida:** presentarlo como un caso con dos cifras de fuentes distintas, sin afirmar equivalencia.

**C-7 — "10-15% de ahorro en tail spend": ¿dato del caso telco o benchmark agregado?** *Interna Doc 3 (§2.2, §3, brecha 10).* El rango aparece como resultado del caso telco y como benchmark agregado de "tail spend con agentes" — posible reciclaje del mismo dato. **Resolución sugerida:** citar una sola vez con nota de que McKinsey no aclara si son mediciones independientes.

---

## 3. Afirmaciones sin fuente o con fuente dudosa (a marcar/verificar antes de redactar)

1. **"25,000 agentes construidos" / "20,000 agentes operando junto a 40,000 consultores" (CEO de McKinsey).** Doc 1 §1.1: atribuida a agregadores/blogs, sin fuente primaria (discurso/entrevista/carta). **No citar como hecho** hasta localizar la fuente primaria.
2. **Cifras agregadas "15-30%, 25-40%, 75% reducción de RFP".** Doc 4 §3.1: provienen de fuentes secundarias (paperclipped.de, Procurement Magazine) y NO se confirmaron palabra por palabra contra el artículo original A12. El artículo original mostró casos con cifras más granulares/distintas. **Verificar contra A12/PDF antes de citar** las cifras redondeadas.
3. **Cifras de escala de Wave ($200B+ spend, 340,000 iniciativas).** Doc 1 §3.3: obtenidas de snippets de búsqueda porque la página fetcheada mostró "placeholder zeros" (bug de render JS). **Re-verificar** antes de citar.
4. **Deloitte y KPMG como partners de Anthropic.** Doc 4 §1.3: solo fuente secundaria (IntuitionLabs), no verificado contra newsroom oficial. **No citar como hecho verificado.**
5. **LLMs de Lilli = Cohere + OpenAI/Azure.** Ver C-2. Fuente secundaria (VentureBeat/CIO Dive), probablemente 2023, año no confirmado con precisión.
6. **Fechas "s.f." de páginas de producto/alianza** (Lilli, Spendscape, Wave, Nvidia, Salesforce, Microsoft-Copilot A8/B8). Marcar como (s.f.) en APA; verificar la fecha de A8/B8 si se cita con precisión.
7. **"Práctica Product Development & Procurement" como marca/unidad editorial.** Doc 1 §5 no la confirmó como marca con presencia editorial propia (las publicaciones están bajo "Operations"); Doc 4 sí lista la URL de la página. Aclarar que es una página de servicios, no la fuente de los artículos de agentic AI.

---

## 4. Preguntas de seguimiento concretas POR AGENTE

**Criterio:** solo se piden búsquedas donde probablemente exista información pública adicional y de valor para el diseño. Las BRECHAS-DOCUMENTADAS (McKinsey no lo publica) NO se piden aquí — van a la sección de limitaciones del documento final (ver sección 5).

### Agente 1 (Productos y Plataformas) — 3 preguntas de baja prioridad (opcional, no bloqueante)
1. **Localizar la fuente primaria de las cifras del CEO** ("25,000 agentes", "20,000 agentes junto a 40,000 consultores"): buscar en Davos 2026 / carta anual de McKinsey / entrevistas de Bob Sternfels 2025-2026, o abandonar la cifra si no aparece fuente primaria.
2. **Re-verificar las cifras de escala de Wave** ($200B spend, 340,000 iniciativas): re-fetch de la página de Wave (A10) o de la página de savings-tracking (A9) para sustituir los datos obtenidos de snippets con bug de render.
3. **Fetch dedicado del artículo "Creating a future-proof enterprise agentic platform architecture" (A17)**, mencionado como no explorado — solo si se quiere reforzar el blueprint de plataforma; el corpus ya es suficiente sin él.

### Agente 2 (Arquitectura Técnica) — 1 pregunta de prioridad media
1. **Clonar/leer directamente el repo ARK** (`/examples`, `/charts`, CRDs) para extraer la estructura declarativa real de un agente/equipo y confirmar si existe algún template de procurement/sourcing. Es la única vía de convertir ARK de "candidato" a "evaluado", y el propio Doc 2 §2.6 lo señala como pendiente. Alto valor de diseño, esfuerzo acotado.
   - *(Las brechas de memoria/vector DB, agentic RAG, FinOps/token, red-teaming de procurement y comparación de frameworks son BRECHAS-DOCUMENTADAS: McKinsey no las publica → sección de limitaciones, NO ronda 2.)*

### Agente 3 (Casos de uso) — 1 pregunta de prioridad media
1. **Verificar las cifras exactas del artículo insignia A12** ("Redefining procurement performance...", 5-feb-2026) contra el PDF/versión completa, para: (a) resolver C-6 y C-7, (b) confirmar o descartar las cifras agregadas "15-30 / 25-40 / 75% RFP" que hoy dependen de fuentes secundarias (ver §3.2). Esto cierra la mayor debilidad de calidad de cifras del corpus.
   - *(La ausencia de nombres de cliente, de auditoría externa y de tasas de fracaso son BRECHAS-DOCUMENTADAS → limitaciones.)*

### Agente 4 (Ecosistema) — 2 preguntas de prioridad media-baja
1. **Verificar Deloitte/KPMG–Anthropic** contra newsrooms oficiales de Deloitte y KPMG (hoy solo IntuitionLabs). Necesario si el benchmark competitivo va a afirmar qué consultoras apostaron por Anthropic.
2. **Confirmar la fecha de publicación del artículo McKinsey–Microsoft Copilot Studio (B8)** y, de paso, verificar si existe alianza McKinsey–SAP aplicable a Ariba (Doc 4 brecha 4). Cierra dos fechas/relaciones pendientes de bajo esfuerzo.

---

## 5. Ítems para la sección de LIMITACIONES del documento final (BRECHAS-DOCUMENTADAS — no requieren más búsqueda)

Estas brechas son de la realidad pública, no del corpus. El corpus demuestra que la información no existe públicamente. Deben declararse como limitaciones, no resolverse con más rondas:

1. Proveedor(es) de LLM de Lilli: McKinsey no lo confirma en fuente primaria.
2. Integración Spendscape ↔ Agentic AI Mesh/Lilli: no documentada públicamente.
3. Nombres de suite S2P/ERP en integración técnica: McKinsey no los publica (solo ServiceNow/ITSM).
4. Implementación concreta de la capa de memoria (vector DB, TTL, episódica vs semántica).
5. "Agentic RAG" como patrón nombrado: ausente en McKinsey.
6. Generación de texto contractual/legal (plantillas vs. fine-tuning vs. RAG) y sistemas CLM por nombre.
7. Costos/economía de tokens en producción y FinOps de agentes.
8. Red-teaming / seguridad ofensiva específica de agentes de procurement.
9. Comparación técnica cuantitativa entre frameworks de orquestación (McKinsey los lista como intercambiables).
10. Metodología de medición de impacto de TODOS los casos citados (líneas base, muestra, proyectado vs. realizado).
11. Nombres de cliente en casos agénticos de procurement (todos anónimos salvo Sanofi/Teva de 2024, de tecnología ambigua).
12. Ningún artículo de McKinsey cruza la arquitectura detallada (mesh/ARK/evals) con un caso de procurement paso a paso — ese "puente" es trabajo de diseño propio del equipo (brecha estructural más importante, y a la vez la oportunidad de diferenciación).

---

## 6. Veredicto global

# APROBADO PARA REDACCIÓN

El corpus es **técnicamente suficiente** para que un arquitecto diseñe un sistema agéntico de procurement informado. Cubre capas y patrones (a), orquestación/frameworks/protocolos con una implementación de referencia descargable, ARK (b), data spine y patrón de integración (c), un cuerpo robusto de evals/guardrails/AgentOps (d) y un mapa priorizado de agentes con métricas (e). La calidad de fuentes y la disciplina hecho/vendor/inferencia son una fortaleza (f).

Las áreas más débiles —integración S2P/ERP concreta, memoria/RAG concretos, metodología de cifras, nombres de cliente— son en su mayoría **BRECHAS-DOCUMENTADAS** de la realidad pública, correctamente identificadas por el corpus, y pertenecen a la sección de limitaciones, no a una nueva ronda de investigación.

**No se requiere una Ronda 2 bloqueante.** Las preguntas de seguimiento de la sección 4 son **verificaciones puntuales de calidad de cifras y fechas** (mejoran el rigor de las citas), no vacíos que impidan diseñar. Recomendación: la redacción puede comenzar en paralelo; las verificaciones de la sección 4 (especialmente Agente 3 pregunta 1 y Agente 2 pregunta 1) pueden ejecutarse durante la redacción y no deben detenerla.

**Contradicciones a resolver antes de publicar (obligatorio para el redactor):** C-1 (incidente Lilli), C-2 (LLMs de Lilli), C-3 (premisa McKinsey-Anthropic). Las demás (C-4 a C-7) son menores y ya tienen resolución sugerida.

**Entregable adicional generado:** `research/memoria/fuentes.md` — lista deduplicada de ~80 fuentes con autor/org, año, título, URL, fecha de acceso y documento(s) donde se cita, lista para alimentar las referencias APA.

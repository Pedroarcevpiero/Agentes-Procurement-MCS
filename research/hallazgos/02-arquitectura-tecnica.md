# Arquitectura Técnica de Sistemas Agénticos — McKinsey / QuantumBlack

**Agente investigador:** AGENTE INVESTIGADOR 2 (arquitectura técnica)
**Alcance temporal:** julio 2024 – julio 2026
**Fecha de acceso a todas las fuentes:** 2026-07-01
**Estado:** EN PROGRESO — actualización incremental

---

## Leyenda de clasificación de hallazgos
- 🟢 **HECHO VERIFICADO**: confirmado directamente en la fuente primaria (texto citable).
- 🟡 **AFIRMACIÓN DEL VENDOR**: declaración promocional/estratégica de McKinsey sin detalle técnico verificable independientemente (marketing claims, cifras de impacto sin metodología pública, etc.).
- 🔵 **INFERENCIA DEL AGENTE**: interpretación o extrapolación del investigador, NO una cita directa. Siempre marcada explícitamente.

---

## 1. El concepto de "Agentic Mesh" de McKinsey

### 1.1 Definición central

🟢 **HECHO VERIFICADO** — McKinsey QuantumBlack define el "agentic AI mesh" como:

> "Una arquitectura composable, distribuida y agnóstica respecto a proveedores que permite que múltiples agentes razonen, colaboren y actúen autónomamente a través de una amplia gama de sistemas, herramientas y modelos de lenguaje — de forma segura."

Fuente: *Seizing the agentic AI advantage*, McKinsey/QuantumBlack, Alexander Sukharevsky, Dave Kerr, Klemens Hjartar et al., 13 de junio de 2025. URL: https://www.mckinsey.com/capabilities/quantumblack/our-insights/seizing-the-agentic-ai-advantage (acceso 2026-07-01).

En un artículo posterior, McKinsey Technology (marzo 2026) refuerza y simplifica la metáfora:

> "Think of it as the nervous system that gives coherence to an otherwise sprawling digital organism" — el mesh es la "capa de orquestación que conecta nuevos agentes de IA entre sí y con sistemas tradicionales."

Fuente: *Rethinking enterprise architecture for the agentic era*, McKinsey Technology, Bjørnar Jensen, Florian Bauer, Lars Vinter, Mallika Vora, 12 de marzo de 2026. URL: https://www.mckinsey.com/capabilities/mckinsey-technology/our-insights/rethinking-enterprise-architecture-for-the-agentic-era (acceso 2026-07-01).

### 1.2 Cinco principios de diseño (pilares)

🟢 **HECHO VERIFICADO** (fuente: *Seizing the agentic AI advantage*, jun. 2025):

1. **Composabilidad**: "Cualquier agente, herramienta o LLM puede conectarse sin necesidad de reconfiguración del sistema."
2. **Inteligencia distribuida**: descomposición de tareas entre redes de agentes cooperativos (no un único "cerebro" central).
3. **Desacoplamiento en capas**: separación explícita de lógica, memoria, orquestación e interfaces.
4. **Neutralidad de proveedores**: componentes independientes y reemplazables, evitando "lock-in" de un único LLM/framework.
5. **Autonomía gobernada**: control mediante políticas embebidas, permisos y mecanismos de escalado transparentes hacia humanos.

🔵 **INFERENCIA DEL AGENTE**: estos cinco pilares son casi idénticos (mismo lenguaje, mismo orden conceptual) a los "cuatro pilares" que aparecen en el artículo de infraestructura de abril 2026 (composabilidad, desacoplamiento, flexibilidad de proveedor, autonomía gobernada) — sugiere que McKinsey mantiene un vocabulario de arquitectura consistente entre sus practices (QuantumBlack y McKinsey Technology) y que "inteligencia distribuida" se fusionó/renombró implícitamente. Esto es útil como señal de que el framework es su narrativa oficial unificada, no un one-off de un solo artículo.

### 1.3 Siete capacidades técnicas interconectadas del mesh

🟢 **HECHO VERIFICADO** (fuente: *Seizing the agentic AI advantage*, jun. 2025). Estas son las capacidades que McKinsey especifica como componentes funcionales del agentic mesh:

1. **Agent and Workflow Discovery**: catálogo dinámico de agentes y flujos de trabajo para permitir reutilización (evita reconstruir agentes ya existentes en otra parte de la empresa).
2. **AI Asset Registry**: centraliza gobernanza de prompts, configuraciones de LLM y definiciones de herramientas (tools) — un "inventario" versionado de activos de IA.
3. **Observabilidad**: "rastreo end-to-end de flujos de trabajo mediante métricas estandarizadas, registros de auditoría y capacidades diagnósticas."
4. **Authentication and Authorization**: controles granulares de acceso entre sistemas agénticos y de procedimientos (identidad de agente, no solo de usuario humano).
5. **Evaluations**: "pruebas comprehensivas de canales agénticos para asegurar precisión y cumplimiento" (evals como componente de infraestructura, no solo de QA puntual).
6. **Feedback Management**: bucles automatizados de retroalimentación para evolucionar configuraciones de agentes con el tiempo.
7. **Compliance and Risk Management**: "políticas integradas, agentes de cumplimiento y salvaguardas éticas."

🔵 **INFERENCIA DEL AGENTE**: estas 7 capacidades leídas en conjunto equivalen funcionalmente a lo que la industria llama "AgentOps"/"LLMOps" (ver sección 3.4), aunque McKinsey no usa ese término explícitamente en este artículo — usa "agentic AI mesh" como paraguas.

### 1.4 Función de coordinación y gobernanza (artículo de marzo 2026)

🟢 **HECHO VERIFICADO** — El mesh cumple tres funciones descritas en *Rethinking enterprise architecture for the agentic era* (marzo 2026):

1. **Coordinación**: aplicar reglas de negocio y mantener "una fuente única de verdad", evitando que agentes con objetivos conflictivos generen fricción operativa. Ejemplo textual: "one [agent] optimizing inventory levels for cost savings, another for customer satisfaction."
2. **Gobernanza**: "the mesh also supports governance and compliance, ensuring that AI-driven decisions adhere to corporate policies."
3. **Visibilidad centralizada**: habilita auditoría del comportamiento de agentes a través de todo el ecosistema.

### 1.5 Riesgos que el mesh busca mitigar

🟢 **HECHO VERIFICADO** (fuente: *Seizing the agentic AI advantage*, jun. 2025). Riesgos explícitamente nombrados:

- "Autonomía incontrolada"
- "Falta de observabilidad y trazabilidad"
- "Proliferación descontrolada de agentes" (**agent sprawl** — término textual usado por McKinsey)
- "Alucinaciones o salidas plausibles pero inexactas"

🔵 **INFERENCIA DEL AGENTE**: el término "agent sprawl" es relevante para nuestro propio diseño: McKinsey lo trata como un riesgo de primer orden equivalente al "shadow IT" de la era SaaS — sugiere que un catálogo/registro central de agentes (punto 1.3.2, AI Asset Registry) no es opcional sino un requisito de gobernanza temprano, no algo que se añade después.

---

## 2. Artículos técnicos clave

### 2.1 "Why agents are the next frontier of generative AI" (McKinsey Digital, jul. 2024) — el artículo fundacional

🟢 **HECHO VERIFICADO** — Fuente: *Why agents are the next frontier of generative AI*, McKinsey Digital, Lareina Yee, Michael Chui, Roger Roberts, Stephen Xu, 24 de julio de 2024. URL: https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/why-agents-are-the-next-frontier-of-generative-ai (acceso 2026-07-01). Este es el artículo que introdujo formalmente el tema de agentes para la audiencia general de McKinsey, y el punto de partida cronológico de esta investigación (línea de tiempo: julio 2024 → junio 2025 QuantumBlack → oct 2025/feb 2026 procurement → marzo/abril 2026 infraestructura).

**Definición técnica de "agente"**: "digital systems that can independently interact in a dynamic world", con capacidad de "plan their actions, use online tools to complete those tasks, collaborate with other agents and people, and learn to improve their performance." A diferencia de sistemas basados en reglas previos, los agentes GenAI aprovechan modelos fundacionales entrenados en datasets masivos no estructurados para "adapt to different scenarios in the same way that LLMs can respond intelligibly" a instrucciones no vistas explícitamente.

**Patrón de orquestación (4 pasos) — el patrón manager/subagente ya está presente en 2024**:
1. Usuario proporciona instrucción en lenguaje natural (prompt).
2. Sistema planifica y ejecuta: "breaking it down into tasks and subtasks, which a manager subagent assigns to other specialized subagents."
3. Mejora iterativa con retroalimentación del usuario durante el proceso.
4. Ejecución de acciones en el mundo digital.

**Caso de uso ilustrativo (underwriting crediticio) — primer ejemplo documentado de equipo de subagentes especializados**:
- Agente *relationship manager*: comunicaciones entre prestatario e institución.
- Agente *executor*: compilación de documentos.
- Agente *financial analyst*: análisis de deuda y ratios financieros.
- Agente *critic*: identificación de discrepancias y retroalimentación (patrón crítico/revisor).

🔵 **INFERENCIA DEL AGENTE**: el patrón "manager subagent asigna a subagentes especializados" + "agente crítico que revisa" de este artículo de julio 2024 es el embrión directo del patrón "orquestador + agentes de dominio + validación" que aparece refinado en el artículo de infraestructura de abril 2026 (sección 3.2) y en los "equipos de agentes" de procurement de febrero 2026 (sección 5.2). Es la misma idea arquitectónica madurando durante casi 2 años de publicaciones.

**Tool use**: los agentes pueden "work with existing software tools and platforms" mediante análisis y generación de conocimiento, uso de aplicaciones de software (plotting, charting), búsqueda web, recopilación de feedback humano, y aprovechamiento de modelos fundacionales adicionales. Los modelos "learn how to interface with tools, whether through natural language or other interfaces" sin integración manual extensiva.

**Memoria y aprendizaje**: los subagentes pueden "draw on prior 'experiences' and codified domain expertise", coordinándose entre sí usando datos organizacionales, implementando un "flywheel effect" donde componentes del framework agéntico se reutilizan.

**NOTA IMPORTANTE — brecha de alcance**: este artículo NO menciona procurement ni supply chain explícitamente. Los 3 casos de uso tratados son: underwriting crediticio, modernización de código heredado (legacy code), y campañas de marketing digital.

### 2.2 "Seizing the agentic AI advantage" (QuantumBlack, jun. 2025) — ver sección 1 y 4 para detalle completo

Ya cubierto en profundidad en secciones 1.1-1.5 (definición de mesh, 7 capacidades) y 4.3-4.4 (modelos, build vs. buy).

### 2.3 "How we enabled Agents at Scale in the Enterprise with the Agentic AI Mesh" (QuantumBlack Medium, jun. 2025) — LA FUENTE TÉCNICA MÁS PROFUNDA ENCONTRADA

🟢 **HECHO VERIFICADO** — Fuente: *How we enabled Agents at Scale in the Enterprise with the Agentic AI Mesh*, blog de QuantumBlack (AI by McKinsey) en Medium, autor principal Dave Kerr (con colaboradores), 12 de junio de 2025. URL: https://medium.com/quantumblack/how-we-enabled-agents-at-scale-in-the-enterprise-with-the-agentic-ai-mesh-baf4290daf48 (acceso 2026-07-01).

**Esta es, hasta ahora, la única fuente que nombra frameworks, protocolos y estándares técnicos concretos.** Es contenido técnico real de ingeniería, no solo mensaje ejecutivo — ver detalle completo en sección 3.10 más abajo.

---

## 3. Patrones de arquitectura concretos

### 3.1 Capas de arquitectura (artículo de infraestructura, abril 2026)

🟢 **HECHO VERIFICADO** — *Reimagining tech infrastructure for and with agentic AI*, McKinsey Technology, Arnaud Tournesac, Arun Gundurao, Ling Lau, Pankaj Sachdeva, 23 de abril de 2026. URL: https://www.mckinsey.com/capabilities/mckinsey-technology/our-insights/reimagining-tech-infrastructure-for-and-with-agentic-ai (acceso 2026-07-01).

Este artículo describe explícitamente 3 capas separadas:

1. **Capa de Orquestación Central**: "agentes, plataformas y sistemas están interconectados a través de una capa de orquestación compartida" — coordina dominios manteniendo control y reutilización.
2. **Capa de Ejecución**: separada de la orquestación deliberadamente, para escalabilidad y flexibilidad mediante desacoplamiento.
3. **Capa de Datos**: provee "fuentes únicas de verdad para activos, dependencias, propiedad, registros y métricas", reduciendo ambigüedad.

### 3.2 Patrón orquestador-trabajadores (worker agents) — ejemplo concreto documentado

🟢 **HECHO VERIFICADO** — El mismo artículo ilustra un flujo real de resolución de incidentes IT con el patrón orquestador + agentes especializados en paralelo:

> "Agentes específicos de dominio (red, aplicación, infraestructura) generan y prueban hipótesis dentro de su alcance. Un agente orquestador sintetiza estos datos para determinar la causa raíz probable."

Componentes del flujo documentado:
- Agente gestor de incidentes (inicia el flujo)
- Agentes de dominio en paralelo (red, infraestructura, aplicación) — cada uno con alcance/scope delimitado
- Agente orquestador (sintetiza resultados de los agentes de dominio)
- Capa de validación determinista (verifica antes de ejecutar acciones)

🔵 **INFERENCIA DEL AGENTE**: este es el único ejemplo end-to-end con suficiente detalle de "quién hace qué" que McKinsey publica en estas fuentes; es de IT operations, no de procurement, pero el patrón (orquestador central + agentes especializados por dominio + validación determinista antes de actuar) es directamente transportable a un caso de sourcing (ej. agentes por categoría de gasto sintetizados por un agente orquestador de sourcing).

### 3.3 Cuatro principios de diseño de la capa de infraestructura

🟢 **HECHO VERIFICADO** (mismo artículo, abril 2026):

1. **Composabilidad**: "componentes de infraestructura, agentes y herramientas pueden reutilizarse entre flujos sin reelaboración."
2. **Desacoplamiento**: separación clara entre capas para flexibilidad.
3. **Flexibilidad de proveedor**: "componentes pueden evolucionar independientemente, reduciendo bloqueo."
4. **Autonomía gobernada**: "agentes operan dentro de políticas definidas, con clara responsabilidad y rutas de escalada."

### 3.4 Human-in-the-loop: patrón de autonomía graduada por riesgo

🟢 **HECHO VERIFICADO**: McKinsey no propone "supervisión humana total" ni "autonomía total", sino un patrón de **autonomía graduada por nivel de riesgo**:

> "Acciones de bajo riesgo pueden ejecutarse autónomamente, mientras que cambios de alto impacto requieren aprobación humana."

Fuente: *Reimagining tech infrastructure for and with agentic AI*, McKinsey Technology, abril 2026.

🔵 **INFERENCIA DEL AGENTE**: esto es consistente con el pilar de "autonomía gobernada" del agentic mesh (sección 1.2) — sugiere que McKinsey ve el HITL no como un checkpoint fijo sino como una política parametrizable por tipo de acción/dominio, potencialmente codificada en el "control plane" (ver 4.1).

### 3.5 Validación determinista separada de la capa de agentes

🟢 **HECHO VERIFICADO**: Decisión de diseño explícita — mantener capas de validación **independientes y deterministas** que definen el comportamiento esperado, separadas de la lógica de razonamiento de los agentes (que es probabilística/no determinista por naturaleza del LLM).

> "Validación y control se vuelven tan críticos como los agentes mismos" cuando escala la ejecución impulsada por agentes.

Fuente: *Reimagining tech infrastructure for and with agentic AI*, McKinsey Technology, abril 2026.

🔵 **INFERENCIA DEL AGENTE**: este patrón — LLM/agente decide, pero un componente determinista (reglas, código, políticas) valida/aprueba antes de ejecutar la acción real — es un guardrail arquitectónico central. Para procurement esto se traduciría, por ejemplo, en que un agente de negociación puede *proponer* un contrato, pero un motor de reglas determinista valida límites de descuento, cláusulas obligatorias, umbrales de aprobación, etc., antes de que la acción se ejecute o se envíe a un humano.

### 3.6 Gestión del ciclo de vida de agentes ("agent lifecycle management")

🟢 **HECHO VERIFICADO**: McKinsey recomienda un **inventario formal de agentes desplegados** con:
- Seguimiento de rendimiento (performance tracking)
- Alcance definido (scope) por agente
- Gestión explícita de costos por agente
- "Documentación del propósito, alcance y rendimiento de cada agente"
- Identidad digital clara para cada agente (no comparten credenciales)
- "Todas las acciones deben ser registradas, trazables y auditables"

Fuente: *Reimagining tech infrastructure for and with agentic AI*, McKinsey Technology, abril 2026.

### 3.7 Datos "imperfectos" como aceptables para empezar

🟢 **HECHO VERIFICADO**: decisión de diseño explícita de McKinsey — no bloquear el despliegue de agentes esperando calidad de datos perfecta.

> "Datos imperfectos no deberían prevenir el progreso" — muchos casos de alto valor pueden pilotarse "incluso en ambientes con fidelidad de base de datos inconsistente."

Razón dada: se requieren registros consistentes, dependencias claras y métricas estandarizadas como mínimo — no perfección de datos.

Fuente: *Reimagining tech infrastructure for and with agentic AI*, McKinsey Technology, abril 2026.

🔵 **INFERENCIA DEL AGENTE**: relevante para procurement, donde los datos maestros de proveedores/catálogos suelen tener calidad heterogénea entre ERPs — McKinsey sugiere explícitamente no usar esto como bloqueante para iniciar pilotos agénticos.

### 3.8 Gestión de contexto y memoria

🟢 **HECHO VERIFICADO**: McKinsey identifica una limitación histórica de los LLM base:

> "Memoria persistente limitada, dificultando el seguimiento de contexto en el tiempo u operación coherente en interacciones extendidas."

Fuente: *Seizing the agentic AI advantage*, McKinsey/QuantumBlack, junio 2025.

Los agentes, a diferencia de LLMs puros, combinan "LLMs con componentes tecnológicos adicionales que proporcionan memoria, planificación, orquestación e integración." La arquitectura resuelve la limitación de memoria mediante capas de memoria alojadas en el mesh (no en el propio modelo).

🔵 **INFERENCIA DEL AGENTE**: McKinsey NO detalla en estas fuentes la implementación técnica concreta de esa "capa de memoria" (¿vector DB?, ¿memoria episódica vs semántica?, ¿qué TTL?) — es una brecha de detalle técnico real (ver sección 6).

### 3.9 RAG agéntico

🟡 **AFIRMACIÓN DEL VENDOR / BRECHA PARCIAL**: en las fuentes revisadas hasta ahora, McKinsey NO usa el término "agentic RAG" explícitamente ni detalla arquitecturas de recuperación aumentada específicas. Se infiere indirectamente a través de menciones a "integración con fuentes de datos externas" y "AI Asset Registry", pero no hay una sección dedicada a patrones RAG. Ver sección 6 (brechas).

### 3.10 DETALLE TÉCNICO PROFUNDO: arquitectura completa del Agentic AI Mesh (fuente: blog técnico QuantumBlack Medium, jun. 2025)

Esta subsección documenta en detalle el contenido de la fuente más técnica encontrada en toda la investigación (ver 2.3). Fuente: *How we enabled Agents at Scale in the Enterprise with the Agentic AI Mesh*, QuantumBlack Medium, Dave Kerr et al., 12 de junio de 2025 (acceso 2026-07-01).

#### 3.10.1 Frameworks de orquestación agéntica nombrados explícitamente

🟢 **HECHO VERIFICADO** — McKinsey/QuantumBlack nombra explícitamente frameworks de mercado (no herramientas propietarias propias) como opciones válidas dentro del mesh:

> "frameworks such as **Langchain**, **Agentspace** and **Autogen**" y también "**Autogen**, **LangGraph**, **CrewAI**, and **Google ADK**"

🔵 **INFERENCIA DEL AGENTE**: esto confirma que McKinsey NO ha construido (públicamente al menos) su propio framework de orquestación de agentes desde cero — recomienda componer el mesh sobre frameworks open-source/comerciales ya existentes del ecosistema (LangChain, LangGraph, AutoGen, CrewAI, Google ADK), consistente con el pilar de "neutralidad de proveedores". Esto es información directamente accionable para nuestro propio harness: valida usar frameworks estándar de la industria en lugar de construir un orquestador propietario desde cero.

#### 3.10.2 Estándares y protocolos de integración

🟢 **HECHO VERIFICADO**:
- **Agent2Agent Protocol (A2A)**: estándar integrado en la solución de referencia de QuantumBlack.
- **Model Context Protocol (MCP)**: descrito como protocolo para "rapidly connect solutions."
- **OpenTelemetry**: usado para observabilidad estandarizada, incluyendo específicamente "Agent Application Semantic Convention and Agent Framework Semantic Convention" (extensiones de OTel para el dominio de agentes).
- **Autenticación**: "Many agentic runtimes provide basic authentication capabilities, using open standards like **OAuth** and **JSON Web Tokens (JWTs)**."

#### 3.10.3 Las 3 capas de la arquitectura de referencia

🟢 **HECHO VERIFICADO**:

**Capa 1 — Platforms & Infrastructure**: LLMs (tanto SaaS como on-premises air-gapped), Data Products con gobernanza, compute/storage/containers/network distribuidos, data platform común.

**Capa 2 — Agentic Systems, Interfaces & Procedural Systems**: "Communication via existing interfaces such as API gateways should be preferred, however 'point to point' integrations will be common in the near term" — es decir, McKinsey reconoce explícitamente que en el corto plazo habrá integraciones ad-hoc punto-a-punto conviviendo con el ideal de API gateway centralizado.

**Capa 3 — Architectural Capabilities**: los 6 pilares detallados a continuación (más detallados que el resumen de "7 capacidades" del reporte ejecutivo de la sección 1.3 — este blog técnico da definiciones más precisas).

#### 3.10.4 Detalle expandido de las capacidades arquitectónicas (más técnico que el reporte ejecutivo)

🟢 **HECHO VERIFICADO**:

**Agent & Workflow Discovery**: "the capability to see a catalogue of all agents and agentic workflows that exist in the organization", permitiendo reutilización sin necesidad de conocer el runtime subyacente de cada agente.

**AI Asset Registry** — gestiona explícitamente estos activos (lista más granular que el reporte ejecutivo):
- System prompts: "which should be parameterizable, with expansion of parameters validated."
- Agent instructions & configurations.
- LLM configurations.
- Tool Definitions y servidores MCP.
- **Golden records** e input/output examples.
- Workflow Controls.

Concepto de **"golden agents"**: soluciones "battle-tested and verified" que "enforce policies around how agents run, what tools and LLMs they have access to" — es decir, agentes de referencia certificados internamente que sirven de plantilla/estándar de calidad para nuevos agentes.

**Observabilidad**: "System-wide observability of workflows that span agentic and procedural solutions creates essential capabilities such as: Tracing of 'chain-of-events' for monitoring, diagnostic, and forensic purposes."

**Authentication and Authorization**: "Fine-grained authorization for both LLM calls as well as tool calls — and to limit the 'blast radius' of a potentially compromised system", usando patrones concretos: "constrained delegation techniques, service account principles, token exchanges."

**Evaluations**: descritas explícitamente como "integration tests of the LLM world" que monitorean llamadas LLM. Requiere tres niveles: "Step-Level testing, Workflow-level testing and long-term interaction testing."

**Fine Tuning, Training Data, Feedback**: "A system of feedback loops that drives continuous, automated improvement in agentic systems", utilizando "metrics such as human feedback, token usage, and agents configured to critique outputs of other agents" (patrón de agente-crítico como mecanismo de feedback automatizado, no solo humano).

#### 3.10.5 Decisiones de diseño técnico clave y sus razones

🟢 **HECHO VERIFICADO**:

1. **Separación de la propiedad intelectual del vendor de la plataforma**: "Teams can use multiple solutions to rapidly deploy workloads while their essential AI intellectual property — instructions, tools, prompts, golden-records, policies, and more, are separated from vendor platforms." Razón implícita: evitar lock-in — si cambias de framework/vendor, no pierdes tus prompts/políticas/golden records porque viven fuera del runtime propietario.

2. **Portabilidad de cargas de trabajo ("translocation")**: los agentes pueden "evolve" vía feedback loops, y hay "translocation of workloads between agentic and procedural systems" — tareas complejas pueden moverse entre un sistema agéntico (LLM-based) y un sistema procedural (reglas/código determinista) según optimización de costos. 🔵 **INFERENCIA DEL AGENTE**: esto sugiere que McKinsey ve la frontera agente-vs-determinista como dinámica, no fija — una tarea puede empezar resuelta por un agente (para explorar el espacio del problema) y luego "graduar" a lógica determinista/procedural una vez que el patrón se estabiliza y es más barato codificarlo directamente. Relevante para reducir costos de inferencia en producción.

3. **Gobernanza de riesgos vía tensión reconocida explícitamente**: "Compliant agentic flows are inherently less 'creative' than less constrained flows" — McKinsey reconoce abiertamente el trade-off entre autonomía/creatividad y cumplimiento, y propone mitigarlo con "compliance agents that iteratively check the work of other agents, referring to institutional policies" (de nuevo el patrón agente-verificador).

#### 3.10.6 "Golden records" como activo de propiedad intelectual de máximo valor

🟢 **HECHO VERIFICADO**: "These 'golden records' may become the organization's **highest value intellectual property** — the human-verified training data required to allow agents to operate effectively."

🔵 **INFERENCIA DEL AGENTE**: esta es una afirmación estratégica importante para nuestro propio diseño — sugiere invertir en un proceso deliberado de captura y versionado de "golden records" (ejemplos verificados por humanos de inputs/outputs correctos) como un activo de datos de primera clase, no como subproducto incidental de los pilotos.

#### 3.10.7 Ejemplo de memoria contextual: agente de detección de fraude

🟢 **HECHO VERIFICADO**: ejemplo concreto dado en el blog — un agente de detección de fraude accede a una "library of example fraudulent content" como componente de memoria contextual (i.e., una base de ejemplos etiquetados que el agente consulta como contexto/RAG, no memoria paramétrica).

#### 3.10.8 Limitaciones explícitas de esta fuente

🔵 **INFERENCIA DEL AGENTE / BRECHA**: aun siendo la fuente más técnica encontrada, el blog **no publica código fuente, pseudocódigo, diagramas de arquitectura descargables, ni detalles de integración con sistemas empresariales específicos de ningún dominio (tampoco procurement)**. Es arquitectónico/conceptual con nombres de tecnologías reales, pero no es una guía de implementación paso a paso ni un repositorio de referencia público.

---

## 4. Recomendaciones de stack tecnológico

### 4.1 Capas del stack (infraestructura, abril 2026)

🟢 **HECHO VERIFICADO** — Fuente: *Reimagining tech infrastructure for and with agentic AI*, McKinsey Technology, abril 2026. Capas recomendadas explícitamente:

1. **Control Plane interoperable**: para que los agentes operen "a través de sistemas y plataformas."
2. **API Gateway seguro**: con verificaciones de política integradas ("acciones repetibles deben ser accesibles como código con verificaciones de política integradas").
3. **Data Lake estructurado**: esquemas consistentes, convenciones de nomenclatura estándar.
4. **Observabilidad integrada**: "logs, métricas, configuración y historiales de cambios correlacionados."
5. **Registro formal de agentes**: documentación de propósito, alcance y rendimiento de cada agente.

Capacidades de infraestructura adicionales mencionadas: Infrastructure as Code (IaC), gestión de configuración automatizada, validación y ejecución segura, auditoría y trazabilidad exhaustiva.

### 4.2 Protocolos abiertos recomendados: MCP y A2A

🟢 **HECHO VERIFICADO**: McKinsey/QuantumBlack recomienda explícitamente **protocolos abiertos** sobre soluciones propietarias:

> "Protocolos abiertos como Model Context Protocol (MCP) y Agent2Agent (A2A)"

Fuente: *Seizing the agentic AI advantage*, McKinsey/QuantumBlack, junio 2025.

🔵 **INFERENCIA DEL AGENTE**: esto es coherente con el pilar de "neutralidad de proveedores" del agentic mesh — McKinsey está alineando su arquitectura de referencia con los estándares emergentes de la industria (MCP de Anthropic, A2A originalmente de Google) en lugar de proponer un protocolo propietario propio. Para nuestro harness, esto valida adoptar MCP como capa de integración de herramientas.

### 4.3 Selección de modelos fundacionales por caso de uso

🟢 **HECHO VERIFICADO** — Fuente: *Seizing the agentic AI advantage*, McKinsey/QuantumBlack, junio 2025. McKinsey segmenta la elección de modelo por 5 contextos de despliegue (nota: esta tabla puede reflejar el catálogo de modelos disponible en el momento de publicación del reporte y quedar desactualizada rápidamente):

| Contexto de uso | Modelos sugeridos (según el reporte) |
|---|---|
| Baja latencia | Mistral Small, Llama 3 8B, Gemini Nano, Claude Haiku |
| Fine-tuning | Mistral Small/8x7B, Llama 3 8B/70B |
| Edge/Embebido | Mistral Small, Gemini Nano, Phi-2 |
| Orquestación multiagente | Mixtral, Grok-1, GPT-3.5 Turbo, Command R+ |
| Soberanía de datos/Auditoría | Mistral, Falcon 180B, BloomZ/Bloom |

🔵 **INFERENCIA DEL AGENTE**: esta tabla llama la atención por estar ya desactualizada en varios puntos incluso al momento del reporte (GPT-3.5 Turbo y Grok-1 eran modelos de generación anterior en junio 2025; no se mencionan modelos de razonamiento tipo o1/o3, Claude Opus/Sonnet 4.x, ni Gemini 2.x). Es señal de que McKinsey no mantiene estas tablas actualizadas dinámicamente en sus reportes PDF — un riesgo a considerar si se cita esta tabla como referencia de "mejores modelos actuales". Para nuestro propio stack, la recomendación estructural (segmentar por caso de uso: latencia, fine-tuning, edge, orquestación, soberanía) es más valiosa y duradera que los nombres de modelo específicos.

### 4.4 Build vs. Buy

🟢 **HECHO VERIFICADO**: McKinsey recomienda una estrategia híbrida, no "todo custom" ni "todo comprado":

> "Realizing full potential requires developing custom-built agents for high-impact processes deeply aligned with company logic, data flows and value creation levers—making them difficult to replicate and uniquely powerful."

Simultáneamente reconoce el valor de agentes "off-the-shelf embedded in software suites" para flujos rutinarios, aunque aclara que estos "rarely unlock strategic advantage."

**Recomendación explícita**: arquitectura agnóstica (el agentic mesh) que combine ambos enfoques — agentes custom para procesos diferenciadores, agentes comprados/embebidos para procesos rutinarios/commodity — conectados a través de la misma capa de orquestación.

Fuente: *Seizing the agentic AI advantage*, McKinsey/QuantumBlack, junio 2025.

🔵 **INFERENCIA DEL AGENTE**: esto tiene una implicación directa para procurement — procesos diferenciadores (p.ej. negociación estratégica, gestión de riesgo de proveedores críticos) serían candidatos a agentes custom; procesos commodity (p.ej. procesamiento de PO estándar, aprobaciones rutinarias) serían candidatos a agentes ya embebidos en el ERP/S2P.

### 4.5 Integración con sistemas empresariales (ERP, ITSM, etc.)

🟢 **HECHO VERIFICADO**: el enfoque explícito de McKinsey NO es reemplazar sistemas legacy, sino integrarlos:

> "La decisión estratégica para empresas no es si reemplazar estos sistemas, sino cómo integrarlos en una columna vertebral coherente."

Fuente: *Reimagining tech infrastructure for and with agentic AI*, McKinsey Technology, abril 2026.

Plataformas empresariales mencionadas explícitamente como puntos de integración (en contexto de IT operations, no procurement): ServiceNow (ITSM), herramientas de gestión en la nube, controladores de red, pilas de observabilidad, CMDB (Configuration Management Database).

Patrón de integración documentado (caso asegurador, del artículo de marzo 2026): un "underwriting agent" consulta motores de riesgo legacy vía APIs, "translating its outputs into natural language explanations", sin modificar el sistema subyacente — es decir, el agente actúa como capa de traducción/interfaz sobre el sistema legacy, no lo sustituye.

Fuente: *Rethinking enterprise architecture for the agentic era*, McKinsey Technology, marzo 2026.

🔵 **INFERENCIA DEL AGENTE / BRECHA**: NINGUNA de las fuentes revisadas hasta ahora menciona explícitamente nombres de ERP (SAP, Oracle, Coupa, Ariba, Jaggaer, etc.) ni plataformas S2P específicas en el contexto de integración técnica. La mención de ServiceNow es para ITSM, no para procurement. Esto es una brecha real — ver sección 6.

### 4.6 Recomendaciones de despliegue de modelos (soberanía/hosting)

🟢 **HECHO VERIFICADO**: McKinsey recomienda mantener flexibilidad de hosting entre:
- Servicios nativos de hiperscaler (cloud)
- Proveedores líderes de modelos (vía API)
- Modelos alojados en la propia empresa (on-prem / VPC privada)

Fuente: *Reimagining tech infrastructure for and with agentic AI*, McKinsey Technology, abril 2026.

---

## 5. Aplicaciones específicas a procurement/supply chain

### 5.1 Fuente principal: "Redefining procurement performance in the era of agentic AI"

🟢 **HECHO VERIFICADO** — Fuente: *Redefining procurement performance in the era of agentic AI*, McKinsey Operations Practice, Aasheesh Mittal, Roman Belotserkovskiy, Theano Liakopoulou, 5 de febrero de 2026. URL: https://www.mckinsey.com/capabilities/operations/our-insights/redefining-procurement-performance-in-the-era-of-agentic-ai (acceso 2026-07-01).

Este es el artículo más directamente relevante a nuestro proyecto encontrado hasta ahora — combina visión de arquitectura con casos reales de procurement.

### 5.2 Patrón de orquestación: "equipos de agentes" ensamblados dinámicamente por workflow

🟢 **HECHO VERIFICADO**: McKinsey describe explícitamente un patrón donde no hay un agente monolítico de procurement, sino equipos de agentes compuestos dinámicamente según la tarea:

> "Procurement tasks will involve teams of such agents, assembled to meet the requirements of each workflow and drawing on a diverse range of data sources."

Tipos de agentes componentes mencionados:
1. Agentes de importación de datos (para fuentes no estructuradas)
2. Agentes de análisis
3. Agentes de interfaz en lenguaje natural

🔵 **INFERENCIA DEL AGENTE**: este patrón de "ensamblaje dinámico de equipos de agentes por workflow" es consistente con el patrón orquestador-trabajadores documentado en el artículo de infraestructura IT (sección 3.2), aplicado ahora específicamente a procurement. Confirma que McKinsey no propone un único "super-agente de procurement" sino composición modular.

### 5.3 Visión end-to-end del ciclo Source-to-Pay

🟢 **HECHO VERIFICADO**: "AI's true power is unlocked when applied across the full source-to-pay life cycle, from early demand signals to supplier performance tracking, allowing for compound benefits—faster decisions, lower costs, and reduced risk."

Cobertura end-to-end explícita: señales de demanda temprana → sourcing → negociación → seguimiento de desempeño post-adjudicación.

### 5.4 Casos de uso reales documentados por McKinsey (con detalle de qué hace cada agente)

🟡 **AFIRMACIÓN DEL VENDOR** (casos anonimizados, sin metodología de medición pública — McKinsey no identifica las empresas ni publica cómo calculó las cifras de impacto):

**Caso 1 — Empresa tecnológica, sourcing de servicios externos (contact center, BPO, servicios financieros):**
- Agente de integración: "integrated spend and market data to generate real-time insights into price trends and savings opportunities."
- Agente de simulación: modelaba evolución de demanda bajo escenarios de volatilidad.
- Impacto reportado: ahorro de 12-20% en contact center; 20-29% de reducción de gasto en BPO y servicios financieros.

**Caso 2 — Empresa química, sourcing autónomo en categoría de consumibles:**
- Agentes automatizan: preparación de invitaciones a licitación (RFx), identificación y precalificación de proveedores, análisis de ofertas competitivas.
- Un agente adicional rutea y sintetiza consultas de proveedores.
- Impacto reportado: eficiencia de personal de procurement +20-30%; captura de valor adicional +1-3%.

**Caso 3 — Empresa de telecomunicaciones, negociación de software especializado:**
- Agente prepara base de hechos pre-negociación comprehensiva.
- Sugerencias en tiempo real durante negociaciones.
- Evaluación de trade-offs (costo/niveles de servicio/riesgo).
- Generación automática de contraofertas.
- Impacto reportado: reducción de tiempo en análisis/emails hasta 90%; ahorros negociados 10-15% entre proveedores.

**Caso 4 — Empresa farmacéutica, cumplimiento invoice-to-contract:**
- "Agents track supplier delivery performance and automatically check invoices and POs against contract terms."
- Impacto reportado: reducción de "leakage" (fuga de valor) del 4%.

**Caso 5 — Fabricante de aeronaves (OEM), automatización de órdenes e inventario:**
- Automatización basada en datos de planificación de producción.
- Impacto reportado: reducción de inventario activo 30%; incremento de EBIT ≈ $700 millones.

🔵 **INFERENCIA DEL AGENTE**: estos 5 casos cubren, en conjunto, casi todo el espectro de "agentic workflows" de procurement pedido en el alcance de esta investigación: sourcing (casos 1-2), negociación (caso 3), gestión de contratos/cumplimiento (caso 4), y gestión de inventario ligada a compras (caso 5). Ningún caso menciona análisis de gasto puro como categoría separada, aunque el "agente de integración" del caso 1 hace spend analytics como parte de su función.

### 5.5 "Procurement Data Spine" — el requisito de datos como fundamento arquitectónico

🟢 **HECHO VERIFICADO**: McKinsey identifica la creación de una "columna de datos" (data spine) común como el requisito fundacional para escalar agentes en procurement:

> "the creation of a common 'data spine' that provides a single source of truth across spend, suppliers, contracts, and market benchmarks"

Diagnóstico del problema actual (cifra citada sin metodología detallada — 🟡 AFIRMACIÓN DEL VENDOR):

> "today's procurement functions use less than 20 percent of the data available to them to support decision-making"

Este dato-spine debe cubrir 4 dimensiones mínimas: gasto (spend), proveedores (suppliers), contratos (contracts), benchmarks de mercado (market benchmarks).

🔵 **INFERENCIA DEL AGENTE**: el "procurement data spine" es la instancia específica de procurement de la "Capa de Datos" genérica descrita en la arquitectura de infraestructura (sección 3.1, punto 3) — mismo concepto arquitectónico (fuente única de verdad), aplicado al dominio de compras.

### 5.6 Velocidad de implementación reportada

🟡 **AFIRMACIÓN DEL VENDOR**: McKinsey reporta ciclos de implementación acelerados —de prototipo a piloto: semanas; de piloto a escala: menos de un año— con el requisito mínimo de "a few key datasets and defined use cases." No se detalla metodología ni tamaño de muestra de esta afirmación.

### 5.7 "No-regret agents" — catálogo de aplicaciones de procurement disponibles ya

🟢 **HECHO VERIFICADO**: McKinsey identifica un conjunto de aplicaciones agénticas que categoriza como de bajo riesgo / alto valor inmediato ("no-regret"):
- Category copilots
- Generación y análisis de RFx (solicitudes de propuesta/cotización)
- Optimización de contratos
- Cumplimiento invoice-to-contract (factura vs. contrato)
- Repricing automático de "tail spend" (gasto de cola larga / proveedores de bajo volumen)

🔵 **INFERENCIA DEL AGENTE**: esta lista es útil como backlog priorizado de casos de uso de bajo riesgo para el diseño de nuestro propio harness — son procesos con reglas relativamente deterministas (comparar factura vs. contrato, re-pricing con reglas), alineados al patrón de "autonomía graduada por riesgo" (sección 3.4).

### 5.8 Modelo de workforce híbrido humano-agente

🟢 **HECHO VERIFICADO**: "En un rewired procurement function, humanos y agentes de IA trabajarán codo a codo" — agentes toman la mayoría del trabajo transaccional repetitivo; humanos se enfocan en resolución creativa de problemas, construcción de relaciones y juicio complejo. Nuevas competencias requeridas mencionadas: prompt engineering, evaluación de escenarios, gestión del cambio.

### 5.9 Métrica de "Procurement ROI" propuesta

🟢 **HECHO VERIFICADO**: McKinsey propone una fórmula explícita:

> "total value created divided by the total cost to achieve that impact"

Componentes de valor: ahorros realizados, leakage evitado, beneficios de capital de trabajo y riesgo, habilitación de ingresos.
Componentes de costo: personal (interno y externo), tecnología, datos, gestión del cambio.

### 5.10 Ausencias notables en este artículo (confirmadas por el fetch directo)

🟡 **BRECHA IDENTIFICADA**: el artículo NO menciona proveedores tecnológicos específicos, NO menciona plataformas S2P concretas (SAP Ariba, Coupa, Jaggaer, Zycus, GEP, Ivalua, etc.), NO detalla arquitectura técnica (frameworks, APIs, modelos LLM específicos), y NO publica metodología de medición para las cifras de impacto reportadas en los 5 casos.

---

### 5.11 Segunda fuente de procurement: "Transforming procurement for an AI-driven world"

🟢 **HECHO VERIFICADO** — Fuente: *Transforming procurement for an AI-driven world*, McKinsey Operations Practice, Jennifer Schmidt, Ryan Samuels, Samir Khushalani (con Casper Bek, Jaisheela Setty, Srinivas Reddy Mallavarapu), 27 de octubre de 2025. URL: https://www.mckinsey.com/capabilities/operations/our-insights/transforming-procurement-functions-for-an-ai-driven-world (acceso 2026-07-01). *(Nota: pendiente de fetch completo del contenido técnico — solo se confirmaron metadatos vía búsqueda; ver sección 6 para seguimiento).*

---

## 6. Brechas identificadas (McKinsey no publica...)

*(pendiente de investigación)*

---

## Fuentes consultadas (bitácora)

| # | URL | Resultado |
|---|-----|-----------|

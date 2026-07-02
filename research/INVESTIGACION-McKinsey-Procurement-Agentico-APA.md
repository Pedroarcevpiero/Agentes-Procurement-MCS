# Sistemas de inteligencia artificial agéntica para *procurement* desarrollados por McKinsey & Company (julio 2024 – julio 2026): productos, arquitectura, casos de uso e implicaciones de diseño

---

**Autores:** Equipo de investigación multiagente

**Institución / Proyecto:** Agentes-Procurement-MCS

**Fecha:** 2 de julio de 2026

---

## Resumen

Esta investigación sintetiza la evidencia pública disponible entre julio de 2024 y julio de 2026 sobre los sistemas de inteligencia artificial agéntica (*agentic AI*) que McKinsey & Company y su unidad QuantumBlack han desarrollado y aplicado a la función de compras (*procurement*). El objetivo es construir una base rigurosa para el diseño de un sistema agéntico propio (*harness*, orquestación y agentes) en una fase posterior del proyecto. Mediante un proceso de investigación multiagente en paralelo, una ronda de control de calidad con rúbrica de seis áreas y verificaciones puntuales contra fuentes primarias, se caracterizan tres planos: (a) los productos y plataformas de McKinsey (Lilli, Spendscape, Wave y la cifra declarada de 25.000 agentes); (b) la arquitectura técnica de referencia —el *"agentic AI mesh"*, el repositorio open-source ARK, el patrón orquestador-subagentes-crítico, las evaluaciones de tres niveles y el *"procurement data spine"*—; y (c) los cinco casos de uso de compras documentados con sus métricas y su estatus de verificación. Se concluye que el corpus público es técnicamente suficiente para diseñar, pero que McKinsey nunca cruza su arquitectura detallada con un caso de *procurement* paso a paso; ese "puente" es trabajo propio del equipo. Se documenta además que no existe una alianza McKinsey–Anthropic (McKinsey es deliberadamente multi-*vendor*) y que varias cifras de impacto son afirmaciones no auditadas del proveedor.

**Palabras clave:** inteligencia artificial agéntica, *procurement*, McKinsey, QuantumBlack, arquitectura multiagente, orquestación, *agentic AI mesh*, ARK, evaluaciones (*evals*), *data spine*.

---

## 1. Introducción

La irrupción de la inteligencia artificial agéntica —sistemas capaces de planificar, usar herramientas, colaborar entre sí y actuar de forma autónoma sobre tareas de múltiples pasos— ha reconfigurado la conversación sobre automatización en las funciones empresariales. En *procurement* (compras y abastecimiento), McKinsey & Company enmarca esta transición como el paso de una "IA analítica" ("muéstrame los datos") a una "IA agéntica" ("hazlo por mí") (Mittal, Belotserkovskiy y Liakopoulou, 2026).

**Propósito.** Este documento consolida y evalúa críticamente todo lo que McKinsey ha publicado —de forma directa o a través de terceros verificables— sobre sistemas agénticos para *procurement* en una ventana de 24 meses (julio 2024 – julio 2026). No es un ejercicio académico neutro: es la base de conocimiento sobre la cual el equipo diseñará, en la fase 2, su propio sistema agéntico de compras. El lector objetivo es doble: un arquitecto de software (que necesita capas, patrones, protocolos y decisiones de diseño) y un líder de *procurement* (que necesita entender qué agentes construir, con qué prioridad y con qué expectativas de impacto).

**Pregunta de investigación.** ¿Podría un arquitecto de software diseñar un sistema agéntico de *procurement* informado utilizando únicamente el corpus público de McKinsey de los últimos 24 meses y, en tal caso, qué patrones debe adoptar, qué decisiones de arquitectura se derivan y qué brechas tendrá que resolver por su cuenta?

**Relevancia para la fase de diseño.** McKinsey ocupa una posición singular: es a la vez un productor de arquitectura de referencia (QuantumBlack publica un *framework* conceptual y un repositorio de código real), un integrador multi-*vendor* (mantiene alianzas paralelas con OpenAI, Google, AWS, NVIDIA, Microsoft y Salesforce) y un asesor de *procurement* con casos de cliente cuantificados. Estudiar su enfoque permite reutilizar patrones ya validados en producción por un actor con escala, en lugar de partir de cero, a la vez que identificar con precisión dónde termina la información pública y comienza el trabajo de diseño diferenciador propio.

---

## 2. Metodología

**Diseño de la investigación.** Se empleó un modelo de **investigación multiagente en paralelo con memoria compartida en archivos**. Cuatro agentes investigadores cubrieron dominios complementarios: (1) productos y plataformas; (2) arquitectura técnica; (3) casos de uso y resultados en *procurement*; y (4) ecosistema tecnológico y *partners*. Cada agente depositó sus hallazgos en archivos de memoria compartida (`research/hallazgos/` y `research/memoria/`), lo que permitió triangulación cruzada entre dominios.

**Control de calidad.** Un quinto agente ejecutó una **ronda de control de calidad (QA)** con una rúbrica de seis áreas: (a) componentes de arquitectura agéntica; (b) orquestación, *frameworks* y protocolos; (c) capa de datos e integraciones; (d) *guardrails*, seguridad, *evals* y observabilidad; (e) mapa de agentes de *procurement*; y (f) calidad y consistencia de las fuentes. El QA emitió un veredicto de suficiencia por área, catalogó siete contradicciones internas (C-1 a C-7) con resoluciones sugeridas, y separó las brechas de esfuerzo (subsanables) de las **brechas documentadas** de la realidad pública (información que McKinsey simplemente no publica).

**Verificaciones contra fuentes primarias.** Tras la ronda de QA, se ejecutaron verificaciones puntuales dirigidas: inspección del código fuente del repositorio ARK (CRDs, ejemplos, *providers*); cotejo *verbatim* de las cifras "insignia" contra los artículos primarios de McKinsey; y confirmación de fechas y atribuciones de fuentes secundarias sensibles. En este documento, **siempre prevalece la versión verificada** por encima de afirmaciones anteriores del mismo corpus.

**Criterios y disciplina epistémica.** Se priorizaron fuentes primarias sobre secundarias. Todo enunciado se clasificó como *hecho verificado* (fuente primaria directa o múltiples fuentes independientes), *afirmación del proveedor* (declarado por McKinsey/QuantumBlack sin auditoría externa) o *inferencia* (deducción propia del equipo). Las cifras de impacto de McKinsey, al no tener metodología ni auditoría externa publicadas, se reportan explícitamente como "según McKinsey (año)".

**Ventana temporal y limitación de fuentes.** La ventana de estudio es julio 2024 – julio 2026; algunas fuentes de contexto anteriores se incluyen marcadas como fuera de ventana. La limitación transversal es que **solo se emplearon fuentes públicas**: no hubo acceso a documentación interna de McKinsey, contratos de cliente ni entornos de producción. Todas las URLs se consultaron el 1 o el 2 de julio de 2026.

## 3. Hallazgos

### 3.1 Productos y plataformas

#### 3.1.1 Lilli: la plataforma interna de IA generativa

Lilli es la herramienta interna de IA generativa de McKinsey, lanzada en julio de 2023 para uso de sus consultores. Está construida sobre un *pipeline* de generación aumentada por recuperación (*retrieval-augmented generation*, RAG) a gran escala sobre un corpus propio de más de 100.000 documentos, con dos pestañas ("GenAI Chat" y "Client Capabilities"); al recibir una consulta, identifica entre cinco y siete piezas de contenido relevantes, las sintetiza e identifica expertos internos (McKinsey & Company, s.f.-a; VentureBeat, 2023). Según McKinsey, el 72 % de la firma está activa en la plataforma, con más de 500.000 *prompts* mensuales y ahorros de hasta 30 % del tiempo de búsqueda y síntesis (McKinsey & Company, s.f.-a). Su hoja de ruta declarada incluye "agentes para automatizar tareas específicas", pero no se identificó un rebranding agéntico formal tipo "Lilli 2.0". McKinsey ofrece además a clientes una versión personalizable de la arquitectura de Lilli; el caso más directo para *procurement* es un "motor de RFP" (*RFP engine*), mencionado sin detalle técnico público.

**LLMs de Lilli (contradicción C-2).** McKinsey se declara oficialmente "LLM-agnostic", describiendo Lilli como una "combinación de muchas tecnologías" con una capa de orquestación de modelos grandes y pequeños, **sin nombrar proveedor** en fuente primaria (McKinsey & Company, 2024). Prensa secundaria (VentureBeat, 2023; CIO Dive, 2023) atribuye a Lilli el uso de **Cohere y OpenAI vía Microsoft Azure**, pero esta atribución **no está confirmada por McKinsey** y debe tratarse como no verificada.

**Incidente de seguridad de marzo de 2026 (contradicción C-1).** Existen dos versiones del alcance del incidente, que este documento presenta sin tomar partido:

- *Versión oficial (fuente primaria).* McKinsey publicó el 11 de marzo de 2026 un comunicado indicando que fue alertada de una vulnerabilidad en Lilli por un investigador de seguridad, que "confirmó y corrigió el problema en cuestión de horas", y que su investigación forense "no identificó evidencia de que datos de clientes o información confidencial hayan sido accedidos" (McKinsey & Company, 2026a).
- *Versión de prensa de seguridad.* Diversos blogs de ciberseguridad reportan que un agente de IA ofensivo autónomo (atribuido a la firma "CodeWall") obtuvo acceso de lectura/escritura a la base de datos de producción en dos horas, sin credenciales, explotando una inyección SQL en un *endpoint* de API no autenticado, con acceso a 46 millones de mensajes y capacidad de modificar *system prompts* (1Kosmos, 2026; Outpost24, 2026; BankInfoSecurity, 2026, entre otros).

Ambas versiones coinciden en la fecha y en que un tercero encontró y explotó una vulnerabilidad real. La cifra de "46 millones de mensajes" no se afirma aquí como hecho. Las lecciones de *guardrails* (ver §4) son válidas con independencia de qué versión sea más precisa.

**Cifra de "25.000 agentes".** El CEO de McKinsey, Bob Sternfels, declaró en el CES de enero de 2026 que la firma "añadió 25.000 agentes de IA a su plantilla en menos de dos años", operando con unos 60.000 "trabajadores" (40.000 humanos + 25.000 agentes) (Varanasi, 2026; The Money Times, 2026). La atribución está verificada con evento y fecha, pero la cifra es una afirmación del propio proveedor sobre datos internos, no auditada. La variante "20.000 agentes junto a 40.000 consultores" que circuló en blogs es una versión imprecisa de esta misma declaración.

#### 3.1.2 Spendscape: *spend analytics* sobre SAP BTP

Spendscape by McKinsey es la plataforma de análisis de gasto (*spend analytics*) heredada de la adquisición de Orpheus GmbH (2020), rebrandeada en 2023. Ofrece transparencia y analítica granular de gasto, gestión de volatilidad de precios, mitigación de riesgo, reporte de emisiones de alcance 3, recomendaciones "AI-powered" y minería de procesos vía Celonis; corre sobre SAP Business Technology Platform (SAP BTP) e integra seguimiento de ahorros con Wave (McKinsey & Company, s.f.-b, s.f.-c). Su hoja de ruta menciona "iniciativas de ahorro impulsadas por gen AI" y módulos de *negotiation excellence* como funcionalidades futuras, **sin confirmación de despliegue en producción** ni de integración documentada con Lilli o el *agentic mesh*.

#### 3.1.3 Wave: gestión de transformación con agentes personalizados

Wave by McKinsey es la plataforma de gestión de programas de transformación. Combina gen AI con una base de conocimiento de más de 500.000 iniciativas y despliega "agentes de IA personalizados" (*custom AI agents*) que apoyan la planeación, predicen riesgos y aceleran decisiones (McKinsey & Company, s.f.-d). McKinsey documenta un caso de transformación de *procurement* que buscaba reducir el gasto en 1.000 millones de dólares, usando Wave como sistema de *tracking* de iniciativas (McKinsey & Company, s.f.-e). **Corrección de verificación:** la cifra de "340.000 iniciativas / 200.000 millones en *spend*" recogida inicialmente **fue retirada** por no ser verificable (la página oficial mostraba contadores en cero por un fallo de render); solo se confirman las cifras de "más de 500.000 iniciativas" en la base de conocimiento y de 47.000 millones de dólares de impacto gestionado en *oil & gas*.

Wave es la evidencia más clara de que McKinsey ya despliega agentes personalizados en un producto con aplicación directa a *procurement* (seguimiento de ahorros, gestión de iniciativas), aunque no publica el detalle técnico (arquitectura, LLM, grado de autonomía) de dichos agentes.

### 3.2 Arquitectura técnica

#### 3.2.1 El *"agentic AI mesh"*: concepto central

El concepto arquitectónico rector de McKinsey es el *"agentic AI mesh"* (malla de IA agéntica): "una arquitectura composable, distribuida y agnóstica respecto a proveedores que permite que múltiples agentes razonen, colaboren y actúen autónomamente a través de sistemas, herramientas y modelos de lenguaje —de forma segura" (Sukharevsky et al., 2025). Un artículo posterior lo describe como "el sistema nervioso que da coherencia a un organismo digital que de otro modo se dispersaría" —la capa de orquestación que conecta a los agentes entre sí y con los sistemas tradicionales (Jensen, Bauer, Vinter y Vora, 2026).

**Cinco principios de diseño** (Sukharevsky et al., 2025): (1) *composabilidad* (cualquier agente, herramienta o LLM se conecta sin reconfigurar el sistema); (2) *inteligencia distribuida* (redes de agentes cooperativos, no un cerebro central); (3) *desacoplamiento en capas* (separación explícita de lógica, memoria, orquestación e interfaces); (4) *neutralidad de proveedores* (componentes reemplazables, evitando *lock-in*); y (5) *autonomía gobernada* (políticas embebidas y escalado transparente a humanos). El artículo de infraestructura de abril de 2026 lista cuatro principios casi idénticos (composabilidad, desacoplamiento, flexibilidad de proveedor, autonomía gobernada) (Tournesac, Gundurao, Lau y Sachdeva, 2026); **la diferencia de "5 vs 4 pilares" (contradicción C-5) no es una contradicción real** sino una evolución/fusión de vocabulario ("inteligencia distribuida" queda subsumida), lo que confirma que se trata de una narrativa oficial consistente y no de un artículo aislado.

**Siete capacidades técnicas del mesh** (Sukharevsky et al., 2025; Kerr et al., 2025): (1) descubrimiento de agentes y flujos de trabajo (catálogo para reutilización); (2) *AI Asset Registry* (gobernanza centralizada y versionada de *prompts*, configuraciones de LLM, definiciones de herramientas y *golden records*); (3) observabilidad (trazado *end-to-end*, auditoría, diagnóstico); (4) autenticación y autorización granular con principio de privilegio mínimo, limitando el "*blast radius*" de un sistema comprometido; (5) evaluaciones (*evals* como infraestructura, no QA puntual); (6) gestión de retroalimentación (bucles automatizados de mejora); y (7) cumplimiento y gestión de riesgo (agentes de *compliance* y salvaguardas éticas). El *mesh* busca mitigar explícitamente cuatro riesgos: autonomía incontrolada, falta de observabilidad, proliferación descontrolada de agentes (*agent sprawl*) y alucinaciones. El *agent sprawl* se trata como riesgo de primer orden —análogo al *shadow IT*—, lo que convierte al registro central de agentes en un requisito temprano, no en un añadido posterior.

#### 3.2.2 ARK: la implementación de referencia open-source

El hallazgo más accionable de toda la investigación es que McKinsey/QuantumBlack mantiene un repositorio open-source real y activo: **ARK (*Agentic Runtime for Kubernetes*)** (McKinsey/QuantumBlack, s.f.), descrito como "un *framework* declarativo, nativo de Kubernetes, para construir aplicaciones agénticas portables, escalables y agnósticas de proveedor". No es una librería de Python, sino una plataforma de *runtime* completa que extiende Kubernetes con *Custom Resource Definitions* (CRDs).

La inspección directa del código fuente (verificación del 2026-07-02, vía las páginas HTML del repositorio) confirmó:

- **11 CRDs** bajo el prefijo `ark.mckinsey.com_`: `Agent`, `Team`, `Model`, `Query`, `Tool`, `MCPServer`, `A2AServer`, `A2ATask`, `Memory`, `ExecutionEngine` y `ArkConfig`. Es decir, ARK reifica como recursos declarativos de Kubernetes tanto los agentes y equipos como la interoperabilidad A2A, la memoria y los motores de ejecución.
- **Estrategias de orquestación de equipos:** ejecución secuencial, flujos basados en grafos, enrutamiento por selector y *round-robin*.
- **Providers de LLM de fábrica** (confirmado por archivos `samples/models/*.yaml`, incluido `claude.yaml`): OpenAI, Azure, Anthropic, Google y Ollama local, "sin cambios de código" al intercambiar proveedor.
- **Protocolos:** soporte nativo de MCP (*Model Context Protocol*) y A2A (*Agent2Agent Protocol*); memoria mediante *backends* conectables (*pluggable*).
- **Madurez:** licencia Apache 2.0, 49+ *releases* con cadencia semanal (última verificada, v0.1.65, del 23 de junio de 2026), *stack* TypeScript/Go/Python, CLI y SDKs.
- **Ausencia de contenido de** ***procurement***: ni `/examples` ni `/samples` contienen ningún acelerador o plantilla vertical de compras/*sourcing* (el único demo de dominio es un "KYC" bancario genérico). ARK es infraestructura genérica, no una solución sectorial.

ARK es, en la práctica, la encarnación técnica y descargable de los principios del *mesh*; para el diseño propio es un candidato directo a evaluación como base de orquestación en lugar de construir el *control plane* desde cero.

#### 3.2.3 Patrón de orquestación: orquestador + subagentes + crítico

Un mismo patrón arquitectónico madura de forma consistente a lo largo de casi dos años de publicaciones: **un agente gestor/orquestador descompone la tarea, la asigna a subagentes especializados por dominio, y un agente crítico/validador revisa el resultado.** Aparece ya en el artículo fundacional (*manager subagent* + subagentes especializados + *critic agent* en un caso de *underwriting* crediticio) (Yee, Chui, Roberts y Xu, 2024); se refina en el ejemplo *end-to-end* de resolución de incidentes de TI (agentes de dominio de red/aplicación/infraestructura en paralelo, un orquestador que sintetiza la causa raíz, y una capa de validación determinista antes de ejecutar) (Tournesac et al., 2026); y se traslada a *procurement* como "equipos de agentes ensamblados para cada flujo de trabajo" (Mittal et al., 2026). McKinsey generaliza el rol de control: "los agentes críticos desafiarán las salidas, los agentes de *guardrail* aplicarán la política y los agentes de *compliance* monitorearán la regulación" (Sukharevsky et al., 2025).

Dos decisiones de diseño acompañan a este patrón:

- **Autonomía graduada por riesgo (*human-in-the-loop*).** McKinsey no propone ni autonomía total ni supervisión total, sino que "las acciones de bajo riesgo pueden ejecutarse autónomamente, mientras que los cambios de alto impacto requieren aprobación humana" (Tournesac et al., 2026). El HITL es una política parametrizable por tipo de acción, no un *checkpoint* fijo.
- **Validación determinista separada de la capa probabilística.** Se mantienen capas de validación deterministas (reglas, código, políticas) independientes de la lógica de razonamiento del agente; "la validación y el control se vuelven tan críticos como los agentes mismos" (Tournesac et al., 2026).

#### 3.2.4 Evaluaciones (*evals*) y AgentOps

La fuente más profunda en este eje describe una **arquitectura de evaluación de tres niveles** (Starkloff, Kokaina y Rahimi, 2026):

1. **Evaluaciones de LLM:** factualidad, calibración, robustez, toxicidad.
2. **Evaluaciones de agente individual:** trayectorias completas, cubriendo el núcleo LLM (alucinaciones, desviación de *prompts*), la interfaz de herramientas (llamadas inválidas, alucinación de herramientas) y la capa de memoria (pérdida de contexto, recuperación obsoleta).
3. **Evaluaciones multiagente:** validan *system invariants* —restricciones inmutables como "sin dobles reembolsos", "ningún ticket sin propietario", "sin saldos negativos", "sin PII en *logs*".

El marco se completa con cinco ejes de métricas (capacidad/eficiencia, robustez/adaptabilidad, seguridad/ética, interacción centrada en humanos, económico/sostenibilidad) y una recomendación práctica de "cinco a siete métricas por flujo de trabajo". El *pipeline* de evaluación se integra en compuertas CI/CD con *golden datasets*, generadores de escenarios adversariales/*out-of-distribution*, y pruebas *shadow*/canary contra tráfico real; usa herramientas nombradas explícitamente: **Arize Phoenix, OpenTelemetry/OpenLLMetry y "Agent-as-a-Judge"**. Se documentan modos de fallo específicos de sistemas multiagente en producción —oscilación "ping-pong", *deadlocks*, escrituras conflictivas, envenenamiento de memoria (*memory poisoning*) y cascadas de agotamiento de recursos— y se enuncia el principio de que "no puede haber *launch and leave*": la evaluación es continua (Yee et al., 2025). Estas siete capacidades y este cuerpo de *evals* equivalen funcionalmente a lo que la industria llama AgentOps/LLMOps.

#### 3.2.5 Capa de datos: el *"procurement data spine"*

El requisito fundacional para escalar agentes en compras es una "columna vertebral de datos común" (*data spine*): una fuente única de verdad que cubra cuatro dimensiones —gasto (*spend*), proveedores (*suppliers*), contratos (*contracts*) y *benchmarks* de mercado (Mittal et al., 2026). McKinsey afirma que hoy las funciones de *procurement* utilizan menos del 20 % de los datos disponibles (afirmación del proveedor, sin metodología). El *data spine* es la instancia de *procurement* de la "capa de datos" genérica de la arquitectura de infraestructura (Tournesac et al., 2026). Dos decisiones de diseño refuerzan este eje: la gobernanza de datos debe "viajar embebida en los propios *pipelines*" de ingesta (McKinsey Technology, s.f.), y los "datos imperfectos no deberían impedir el progreso" —los pilotos pueden empezar con unos pocos *datasets* clave, sin esperar calidad perfecta (Tournesac et al., 2026), un punto especialmente relevante para *procurement*, donde los datos maestros de proveedores suelen ser heterogéneos.

#### 3.2.6 *Frameworks*, protocolos y *build vs. buy*

McKinsey **no construye un orquestador propio desde cero**; compone sobre el ecosistema estándar. Nombra de forma consistente entre fuentes los *frameworks* LangChain, LangGraph, AutoGen, CrewAI, Google ADK y Agentspace (Kerr et al., 2025; Yee et al., 2025), y recomienda los protocolos abiertos **MCP y A2A** por encima de soluciones propietarias, con OAuth 2.0/JWT para autenticación y OpenTelemetry/OpenLLMetry para trazas. La estrategia *build vs. buy* es híbrida y explícita: agentes *custom* para procesos diferenciadores "profundamente alineados con la lógica, los flujos de datos y las palancas de valor de la empresa", y agentes *off-the-shelf* embebidos para procesos *commodity*, todos conectados por el mismo *mesh* (Sukharevsky et al., 2025). Un activo estratégico destacado son los *"golden records"* —ejemplos de entrada/salida verificados por humanos—, descritos como potencialmente "la propiedad intelectual de mayor valor de la organización" (Kerr et al., 2025).

### 3.3 Casos de uso y métricas en *procurement*

McKinsey documenta cinco casos de cliente (todos anónimos) con detalle del rol de cada agente. Todas las cifras son **afirmaciones del proveedor** sobre clientes anónimos, sin metodología de medición ni auditoría externa publicadas; se reproducen para dimensionar expectativas, no como evidencia auditada.

**Caso 1 — Empresa tecnológica (servicios externos: contact center, BPO).** Un agente integra datos de gasto y de mercado para detectar tendencias de precio en tiempo real; otro simula la evolución de la demanda bajo escenarios. Impacto reportado: 12–20 % de oportunidades de ahorro en contact center y 20–29 % en BPO/servicios financieros —"oportunidades identificadas", no necesariamente capturadas (Mittal et al., 2026).

**Caso 2 — Empresa química (*sourcing* autónomo de consumibles).** Es el caso más rico operativamente: agentes que preparan las licitaciones (RFx), identifican y precalifican proveedores, analizan ofertas competidoras y enrutan/sintetizan consultas de proveedores. Impacto: +20–30 % de eficiencia del personal y +1–3 % de captura de valor (Mittal et al., 2026; Sukharevsky et al., 2025).

**Caso 3 — Operador de telecomunicaciones (negociación de software especializado, *tail spend*).** El caso más cercano a un "agente negociador": prepara una *fact base* prenegociación, ofrece sugerencias en tiempo real, evalúa *trade-offs* de costo/servicio/riesgo y genera contraofertas automáticamente. Impacto: hasta 90 % menos tiempo en análisis y correos, y 10–15 % de ahorro entre proveedores. Es siempre *human-in-the-loop*: el agente prepara, sugiere y redacta, pero no decide ni firma (Mittal et al., 2026).

**Caso 4 — Empresa farmacéutica (cumplimiento *invoice-to-contract*, contradicción C-6).** Agentes que verifican facturas y órdenes de compra contra los términos del contrato y rastrean el desempeño de entrega. La fuente primaria de febrero de 2026 reporta una reducción del 4 % en *leakage* (fuga de valor) (Mittal et al., 2026); una segunda fuente reporta un *proof-of-concept* de cuatro semanas que identificó más de 10 millones de dólares recuperables (Schmidt, Samuels y Khushalani, 2025). Probablemente describen el mismo caso desde ángulos distintos (porcentaje de fuga evitada vs. dólares recuperados en el piloto), pero **ninguna fuente lo aclara**; se presentan como dos cifras de fuentes distintas sin afirmar equivalencia.

**Caso 5 — Fabricante de aeronaves (OEM): automatización de órdenes e inventario.** Ejecución automatizada de órdenes basada en datos de planificación de producción. Impacto: −30 % de inventario activo y ~+700 millones de dólares de EBIT —la mayor cifra absoluta del corpus, aunque corresponde más a *supply chain*/inventario que a *procurement* puro (Mittal et al., 2026).

**"No-regret agents".** McKinsey identifica un conjunto de aplicaciones de bajo riesgo y alto valor inmediato, disponibles ya: *category copilots*, generación y análisis de RFx, optimización de contratos, cumplimiento *invoice-to-contract* y *repricing* automático de *tail spend* (Mittal et al., 2026). La secuencia de adopción recomendada es: (1) construir el *data spine*, (2) activar *no-regret agents*, (3) rediseñar roles y procesos para la convivencia humano-agente.

**Estatus de verificación de las cifras "insignia" (contradicciones C-6 y C-7).** El cotejo *verbatim* contra las tres fuentes primarias arrojó que, de las cuatro cifras agregadas que circulaban en el corpus, solo dos se confirman:

| Cifra agregada | Estatus de verificación |
|---|---|
| **25–40 %** más eficiente la función de *procurement* | **Verificada** *verbatim*, pero **en el artículo de octubre de 2025** (Schmidt et al., 2025), NO en el de febrero de 2026. Es una proyección prospectiva ("*could result*"), no una medición histórica. |
| **10–15 %** de ahorro en *tail spend* | **Verificada** una sola vez, en el artículo de febrero de 2026, **ligada únicamente al caso telco** (Caso 3). No es un *benchmark* agregado independiente; el corpus la había duplicado erróneamente. |
| **15–30 %** de "*autonomous category agents*" | **No verificable.** No aparece *verbatim* en ninguna fuente primaria; probable atribución errónea de fuente secundaria. **No usar como dato de McKinsey.** |
| **75 %** de reducción en tiempo de preparación de RFP | **No verificable.** No aparece en ninguna fuente primaria de McKinsey; probable marketing de un *vendor* de herramientas RFP. **No usar como dato de McKinsey.** |

**Mapa de subprocesos de *procurement* cubiertos por McKinsey.**

| Subproceso | Qué ha mostrado McKinsey | Evidencia |
|---|---|---|
| *Spend analysis* | Agentes de integración de datos de gasto/mercado; *category copilots* | Caso real (tecnológica) |
| *Sourcing* estratégico / eRFx | Generación de RFx, precalificación de proveedores, análisis de ofertas | Caso real (química) |
| Negociación | "Agentes negociadores" de apoyo (*fact base*, sugerencias, contraofertas) | Caso real (telco); siempre HITL |
| Gestión de contratos (CLM) | Reconciliación factura-contrato; "optimización de contratos" solo como categoría | Caso real de reconciliación (farma); optimización sin caso propio |
| Gestión de categorías | *Category copilots*; agentes de categoría | Parcial (química) |
| Riesgo y desempeño de proveedores | Seguimiento de entrega y cumplimiento | Sin caso dedicado a riesgo financiero/geopolítico |
| Procure-to-pay (P2P) | Automatización de órdenes e inventario | Caso real (aeroespacial), más *supply chain* |
| *Tail spend* | Negociación agéntica; *repricing* automático | Caso real (telco); *repricing* solo como categoría |
| ESG / sostenibilidad | Solo mencionado en tabla de madurez | Sin caso ni agente descrito |

Dos casos con nombre de cliente (Sanofi y Teva) existen, pero son de junio de 2024 y describen analítica avanzada/digital, sin confirmar si emplean IA agéntica (McKinsey et al., 2024). No se documenta ningún agente negociador plenamente autónomo, ni casos de fracaso de pilotos (sesgo de supervivencia).

### 3.4 Ecosistema tecnológico y *partners*

**Postura multi-*vendor* de McKinsey.** McKinsey opera un modelo de **alianzas paralelas** con prácticamente todos los grandes proveedores de infraestructura y modelos, sin apuesta exclusiva: OpenAI ("Frontier Alliance", 23-feb-2026) (McKinsey & Company, 2026b); Google Cloud ("McKinsey Google Transformation Group", 22-abr-2026) (McKinsey & Company, 2026c); AWS ("Amazon McKinsey Group", 22-ene-2026) (McKinsey & Company, 2026d); NVIDIA (alianza institucional); Microsoft (Copilot Studio); y Salesforce (Agentforce, *agent blueprints*). Esta neutralidad es coherente con el pilar de "neutralidad de proveedores" del *mesh*: McKinsey vende orquestación, estrategia y gestión del cambio, no un *stack* propietario.

**No existe alianza McKinsey–Anthropic (contradicción C-3).** La premisa del *brief* original —una alianza McKinsey–Anthropic anunciada en diciembre de 2025— **no pudo verificarse en ninguna fuente**; la evidencia apunta en dirección contraria. En mayo de 2026, Anthropic lanzó (con Blackstone, Hellman & Friedman y Goldman Sachs) una compañía de servicios de IA de ~1.500 millones de dólares, apodada por la prensa "the McKinsey of AI", posicionándose como **competidor directo** de McKinsey (Anthropic, 2026; CNBC, 2026; Fortune, 2026). El único punto de contacto McKinsey–Anthropic verificado es que un informe de *agentic commerce* B2C cita a Anthropic como creador de MCP (Schumacher, Roberts y Giebel, 2025). Como contraste, las alianzas de marca profundas con Anthropic están en Accenture, PwC, Deloitte y KPMG —no en las MBB (McKinsey, BCG, Bain) (Accenture, 2025; Deloitte, 2024; Anthropic, 2026b).

**Integración S2P/ERP como brecha.** En ninguna de las fuentes primarias McKinsey nombra una suite S2P/ERP concreta (SAP Ariba, Coupa, Ivalua, Jaggaer, Oracle) en contexto de integración técnica; el único sistema empresarial nombrado es ServiceNow (ITSM). La alianza general SAP–McKinsey se centra en S/4HANA y solo menciona "*Intelligent Spend Management*" como categoría, sin nombrar Ariba; el único vínculo técnico real es que Spendscape corre sobre SAP BTP. El patrón de integración documentado es "el agente como capa de traducción sobre el sistema *legacy* vía API, sin reemplazarlo" (caso asegurador) (Jensen et al., 2026).

**Benchmark competitivo (breve).** BCG cuantifica un TAM de 200.000 millones de dólares en servicios tecnológicos agénticos y es igual de agnóstica que McKinsey (BCG, 2026). Bain se enfoca en *agentic commerce* B2C, no en *procurement* B2B. Los *vendors* nativos de *procurement* (Zycus, Globality, GEP, Keelvar, Arkestro, LevaData) sí nombran producto y métricas de cliente concretas; por ejemplo, Globality afirma haber reducido el ciclo de RFP de Bristol Myers Squibb de seis meses a 27 días (Globality, s.f.). SAP (Ariba *next-gen* con Joule, mar-2026) y Coupa (Compose/Catalyst, 2026) desarrollan capacidades agénticas de forma independiente, sin vínculo con McKinsey.

## 4. Discusión: implicaciones para el diseño de nuestro sistema agéntico de *procurement*

Esta es la sección central del documento. Traduce la evidencia anterior en decisiones de diseño accionables para la fase 2, distinguiendo lo que podemos **adoptar** (patrones validados por McKinsey) de lo que tendremos que **resolver por nuestra cuenta** (brechas que McKinsey no publica).

### 4.1 Patrones a adoptar (con la evidencia que los respalda)

1. **Componer, no construir el orquestador desde cero.** McKinsey no construyó un orquestador propietario: compone sobre *frameworks* estándar (LangChain/LangGraph, AutoGen, CrewAI, Google ADK) y publica ARK como *runtime* declarativo (Kerr et al., 2025; McKinsey/QuantumBlack, s.f.). *Decisión:* evaluar ARK y/o LangGraph como base de nuestro *control plane*, en lugar de invertir en un orquestador propio.

2. **Patrón orquestador + subagentes de dominio + crítico/validador.** Es el patrón más consistente del corpus (2024–2026). *Decisión:* modelar cada flujo de *procurement* como un equipo ensamblado dinámicamente —p. ej. un orquestador de *sourcing* que coordina subagentes de RFx, descubrimiento de proveedores, análisis de ofertas y comunicación, más un agente crítico que revisa contra política antes de escalar a humano.

3. **HITL graduado por riesgo, no *checkpoint* fijo.** Autonomía plena para acciones de bajo riesgo (p. ej. *repricing* de *tail spend* dentro de umbrales), aprobación humana obligatoria para alto impacto (p. ej. adjudicación de contrato estratégico) (Tournesac et al., 2026). *Decisión:* codificar el nivel de autonomía como política parametrizable por tipo de acción y umbral monetario.

4. **Validación determinista separada de la capa probabilística.** El agente *propone*; un motor de reglas determinista *valida* (límites de descuento, cláusulas obligatorias, umbrales de aprobación) antes de ejecutar o escalar (Tournesac et al., 2026). *Decisión:* implementar una capa de validación de negocio independiente del LLM, testeable de forma determinista.

5. **Evaluaciones de tres niveles como infraestructura desde el día uno.** LLM / agente individual / multiagente con *system invariants* de *procurement* (p. ej. "ninguna PO sin contrato asociado", "ningún proveedor no precalificado adjudicado", "sin doble pago") (Starkloff et al., 2026). *Decisión:* integrar *evals* en compuertas CI/CD con *golden datasets* de RFx/negociación/cumplimiento; seleccionar 5–7 métricas por flujo; adoptar OpenTelemetry/OpenLLMetry y un enfoque "Agent-as-a-Judge"; planificar contra los modos de fallo conocidos (ping-pong, *memory poisoning*, cascadas de recursos).

6. ***Procurement data spine*** **antes que agentes.** Fuente única de verdad sobre gasto, proveedores, contratos y *benchmarks*, con gobernanza embebida en los *pipelines* (Mittal et al., 2026; McKinsey Technology, s.f.). *Decisión:* priorizar el *data spine* como fundamento, pero **sin bloquear los pilotos** esperando datos perfectos: empezar con unos pocos *datasets* clave.

7. **Registro de agentes y *golden records* como activos de primera clase.** Combatir el *agent sprawl* con un *AI Asset Registry* desde el inicio, y capturar/versionar deliberadamente *golden records* (ejemplos verificados por humanos), tratados como la PI de mayor valor (Kerr et al., 2025). *Decisión:* incluir registro de agentes, versionado de *prompts*/políticas y captura de *golden records* en la arquitectura base, no como añadido posterior.

8. **Neutralidad de proveedor y protocolos abiertos (MCP/A2A).** Separar la lógica, los *prompts* y los *golden records* del *runtime* del *vendor* para evitar *lock-in*; adoptar MCP para la integración de herramientas y A2A para interacción entre agentes (Sukharevsky et al., 2025). *Decisión:* MCP como capa de integración de herramientas/datos; abstracción multi-LLM (como la de ARK) para intercambiar modelos sin cambios de código.

9. **Lecciones de seguridad del caso Lilli.** Con independencia de la versión del incidente, las lecciones de *guardrails* son válidas (McKinsey & Company, 2026a; 1Kosmos, 2026): (a) validar *inputs* en todos los *endpoints* de API expuestos a agentes; (b) proteger contra inyección SQL incluso con capas de IA; (c) restringir la modificación de *system prompts* en producción; (d) autenticar rigurosamente cualquier *endpoint* alcanzable por un agente autónomo; y (e) aplicar privilegio mínimo e identidad propia por agente para limitar el "*blast radius*". En *procurement* esto se extiende al *red-teaming* de vectores propios: *prompt injection* vía documentos de proveedores maliciosos, manipulación de RFx y envenenamiento de bases de datos de proveedores.

### 4.2 Brechas que tendremos que resolver nosotros (McKinsey no las publica)

McKinsey publica la arquitectura genérica (*mesh*, ARK, *evals*) y los casos de *procurement* en documentos **separados que nunca cruza**. El "puente" es nuestro trabajo de diseño —y nuestra principal oportunidad de diferenciación. Las brechas concretas a resolver son:

- **Traducción *mesh* → *procurement*.** No existe ningún artículo que aplique el detalle arquitectónico paso a paso a un caso de compras. Debemos definir qué agentes, qué herramientas MCP, qué esquema del *data spine* y qué *evals* específicas para RFx/negociación/cumplimiento.
- **Capa de memoria concreta.** McKinsey afirma que el *mesh* resuelve la memoria, pero no especifica implementación (base de datos vectorial, TTL, memoria episódica vs. semántica, particionamiento entre agentes). ARK ofrece *backends* conectables pero no prescribe uno.
- **RAG agéntico.** El término no aparece en McKinsey; debemos diseñar el patrón de recuperación dinámica (qué y cuándo recuperar contexto de contratos/proveedores) por nuestra cuenta.
- **Integración S2P/ERP.** McKinsey no nombra ninguna suite ni publica patrones de conectores/mapeos de datos con SAP Ariba, Coupa, Ivalua, Jaggaer u Oracle. Tendremos que diseñar la integración concreta (probablemente siguiendo el patrón "agente como capa de traducción vía API sobre el *legacy*").
- **Generación de texto contractual/legal.** No se detalla cómo se generan contraofertas o cláusulas (plantillas vs. *fine-tuning* vs. RAG), ni la integración con sistemas CLM, ni los *guardrails* legales.
- **Economía de *tokens*/FinOps** y **comparación cuantitativa de *frameworks*.** McKinsey no publica costos por tarea agéntica ni criterios de selección entre orquestadores.

### 4.3 Lista priorizada de agentes candidatos ("no-regret agents") para la fase 2

Derivada de la lista de McKinsey y del detalle operativo de los casos, priorizada por relación valor/riesgo y por disponibilidad de evidencia:

| Prioridad | Agente candidato | Fundamento en la evidencia | Riesgo / autonomía |
|---|---|---|---|
| 1 | **Cumplimiento *invoice-to-contract*** | Reglas relativamente deterministas; caso farma (−4 % *leakage*) | Bajo; alta autonomía con validación determinista |
| 2 | **Análisis y generación de RFx** | Caso química (*sourcing* autónomo de consumibles) | Bajo-medio; HITL en adjudicación |
| 3 | ***Category copilot* / *spend analysis*** | Caso tecnológica (integración gasto/mercado) | Bajo; asistivo |
| 4 | ***Repricing* de *tail spend*** | Listado como *no-regret*; caso telco | Bajo; autónomo dentro de umbrales |
| 5 | **Copiloto de negociación** | Caso telco (*fact base*, sugerencias, contraofertas) | Medio; estrictamente HITL, nunca cierra |
| 6 | **Optimización de contratos** | Listado por McKinsey, sin caso propio | Medio; requiere *guardrails* legales |

Se recomienda iniciar por los agentes 1–3 (bajo riesgo, reglas claras, evidencia sólida), construyendo en paralelo el *data spine* y la infraestructura de *evals*/registro, y reservando el copiloto de negociación (agente 5) para una fase posterior por su exposición legal/reputacional —manteniéndolo, como McKinsey, siempre *human-in-the-loop*.

## 5. Limitaciones de la investigación

1. **Solo fuentes públicas.** No hubo acceso a documentación interna, contratos ni entornos de producción de McKinsey. Todo lo aquí sintetizado es lo que McKinsey ha hecho público directamente o vía terceros verificables.
2. **Dependencia de afirmaciones del proveedor.** La mayoría de las cifras de impacto (12–90 % según caso, 25–40 % agregado, ~700 M USD de EBIT) son afirmaciones de McKinsey sobre clientes anónimos, **sin metodología ni auditoría externa**. No deben citarse como evidencia auditada.
3. **Cifras no verificables retiradas.** Las cifras "15–30 %" (agentes de categoría) y "75 %" (reducción de RFP) no se hallaron en ninguna fuente primaria y **no se atribuyen a McKinsey**; la cifra de "340.000 iniciativas de Wave" fue retirada por no verificable.
4. **Corrección de la premisa del proyecto.** No existe alianza McKinsey–Anthropic; el *brief* original partía de una premisa incorrecta, corregida en §3.4.
5. **Brechas documentadas de la realidad pública** (no subsanables con más búsqueda): proveedor(es) de LLM de Lilli; integración Spendscape ↔ *mesh*/Lilli; nombres de suites S2P/ERP en integración técnica; implementación concreta de la capa de memoria; "*agentic RAG*" como patrón nombrado; generación de texto contractual y sistemas CLM por nombre; economía de *tokens*/FinOps; *red-teaming* específico de *procurement*; comparación cuantitativa de *frameworks*; metodología de medición de todos los casos; y nombres de cliente en los casos agénticos.
6. **Ausencia del "puente" arquitectura–*procurement*.** Ningún artículo de McKinsey cruza su arquitectura detallada (*mesh*/ARK/*evals*) con un caso de *procurement* paso a paso; esta es a la vez la mayor limitación del corpus y la principal oportunidad de diseño diferenciador del equipo.
7. **Volatilidad temporal.** Algunas tablas de McKinsey (p. ej. la selección de modelos fundacionales de junio de 2025) ya estaban desactualizadas al publicarse; los nombres de modelo deben tomarse como ilustrativos, no como recomendación vigente.

---

## 6. Referencias

1Kosmos. (2026). *McKinsey Lilli breach (2026): What it reveals about agent authentication*. Recuperado el 1 de julio de 2026, de https://www.1kosmos.com/resources/blog/mckinsey-lilli-breach-agent-authentication

Accenture. (2025, diciembre). *Accenture and Anthropic launch multi-year partnership to drive enterprise AI innovation and value across industries*. Recuperado el 1 de julio de 2026, de https://newsroom.accenture.com/news/2025/accenture-and-anthropic-launch-multi-year-partnership-to-drive-enterprise-ai-innovation-and-value-across-industries

Anthropic. (2026, 4 de mayo). *Building a new enterprise AI services company with Blackstone, Hellman & Friedman, and Goldman Sachs*. Recuperado el 1 de julio de 2026, de https://www.anthropic.com/news/enterprise-ai-services-company

Anthropic. (2026b, 19 de mayo). *KPMG integrates Claude across its core business and workforce of more than 276,000 in strategic alliance*. Recuperado el 1 de julio de 2026, de https://www.anthropic.com/news/anthropic-kpmg

BankInfoSecurity. (2026). *Autonomous agent hacked McKinsey's AI in 2 hours*. Recuperado el 1 de julio de 2026, de https://www.bankinfosecurity.com/autonomous-agent-hacked-mckinseys-ai-in-2-hours-a-31007

Boston Consulting Group. (2026). *The $200 billion agentic AI opportunity for tech service providers*. Recuperado el 1 de julio de 2026, de https://www.bcg.com/publications/2026/the-200-billion-dollar-ai-opportunity-in-tech-services

CIO Dive. (2023). *McKinsey rolls out generative AI tool 'Lilli' to 7K employees*. Recuperado el 1 de julio de 2026, de https://www.ciodive.com/news/McKinsey-generative-AI-Lilli-platform-internal-employees/691231/

CNBC. (2026, 4 de mayo). *Anthropic teams with Goldman, Blackstone and others on $1.5 billion AI venture targeting PE-owned firms*. Recuperado el 1 de julio de 2026, de https://www.cnbc.com/2026/05/04/anthropic-goldman-blackstone-ai-venture.html

Deloitte. (2024, 31 de julio). *Deloitte and Anthropic collaborate to bring safe, reliable and trusted AI to commercial and government organizations*. Recuperado el 1 de julio de 2026, de https://www.deloitte.com/us/en/about/press-room/deloitte-and-anthropic-collaborate-to-bring-safe-reliable-trusted-ai-to-commercial-government-organizations.html

Fortune. (2026, 4 de mayo). *Anthropic takes shot at consulting industry in joint venture with Wall Street giants*. Recuperado el 1 de julio de 2026, de https://fortune.com/2026/05/04/anthropic-claude-consulting-industry-joint-venture-blackstone-goldman-sachs/

Globality. (s.f.). *Autonomous sourcing*. Recuperado el 1 de julio de 2026, de https://www.globality.com/products/autonomous-sourcing/

Jensen, B., Bauer, F., Vinter, L., y Vora, M. (2026, 12 de marzo). *Rethinking enterprise architecture for the agentic era*. McKinsey & Company (McKinsey Technology). Recuperado el 1 de julio de 2026, de https://www.mckinsey.com/capabilities/mckinsey-technology/our-insights/rethinking-enterprise-architecture-for-the-agentic-era

Kerr, D., Gabrielli, D., Galeev, R., Kokaina, S., Cheung, C. W., Madden, C., y Stichbury, J. (2025, 12 de junio). *How we enabled Agents at Scale in the enterprise with the Agentic AI Mesh*. QuantumBlack, AI by McKinsey (Medium). Recuperado el 1 de julio de 2026, de https://medium.com/quantumblack/how-we-enabled-agents-at-scale-in-the-enterprise-with-the-agentic-ai-mesh-baf4290daf48

McKinsey & Company. (s.f.-a). *Rewiring the way McKinsey works with Lilli, our generative AI platform*. Recuperado el 1 de julio de 2026, de https://www.mckinsey.com/capabilities/tech-and-ai/how-we-help-clients/rewiring-the-way-mckinsey-works-with-lilli

McKinsey & Company. (s.f.-b). *Spendscape fifth anniversary*. Recuperado el 1 de julio de 2026, de https://www.mckinsey.com/capabilities/operations/tech-tools/spendscape-technology/our-updates/spendscape-fifth-anniversary

McKinsey & Company. (s.f.-c). *Procurement savings tracking software / Integrated Impact Management*. Recuperado el 1 de julio de 2026, de https://www.mckinsey.com/capabilities/operations/tech-tools/spendscape-technology/our-offerings/savings-tracking-and-integrated-impact-management

McKinsey & Company. (s.f.-d). *Wave program management software*. Recuperado el 1 de julio de 2026, de https://www.mckinsey.com/capabilities/transformation/how-we-help-clients/wave/overview

McKinsey & Company. (s.f.-e). *Procurement transformation program to reduce spend by $1 billion (Wave)*. Recuperado el 1 de julio de 2026, de https://www.mckinsey.com/capabilities/transformation/how-we-help-clients/wave/our-impact/procurement-transformation-program-to-reduce-spend-by-1-billion

McKinsey & Company. (2024, 25 de noviembre). *What McKinsey learned while creating its generative AI platform (Lilli)*. Recuperado el 1 de julio de 2026, de https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/what-mckinsey-learned-while-creating-its-generative-ai-platform

McKinsey & Company. (2026a, 11 de marzo). *Statement on strengthening safeguards within the Lilli tool*. Recuperado el 1 de julio de 2026, de https://www.mckinsey.com/about-us/media/statement-on-strengthening-safeguards-within-the-lilli-tool

McKinsey & Company. (2026b, 23 de febrero). *McKinsey and OpenAI scale AI-driven transformations with new Frontier Alliance*. Recuperado el 1 de julio de 2026, de https://www.mckinsey.com/about-us/new-at-mckinsey-blog/mckinsey-and-openai-scale-ai-driven-transformations-with-new-frontier-alliance

McKinsey & Company. (2026c, 22 de abril). *McKinsey and Google Cloud launch the McKinsey Google Transformation Group to scale enterprise impact for the AI era*. Recuperado el 1 de julio de 2026, de https://www.mckinsey.com/about-us/new-at-mckinsey-blog/mckinsey-and-google-cloud-launch-the-mckinsey-google-transformation-group-to-scale-enterprise-impact-for-the-ai-era

McKinsey & Company. (2026d, 22 de enero). *McKinsey and AWS launch Amazon McKinsey Group*. Recuperado el 1 de julio de 2026, de https://www.mckinsey.com/about-us/new-at-mckinsey-blog/mckinsey-and-amazon-launch-amazon-mckinsey-group

McKinsey Technology. (s.f.). *Building the foundations for agentic AI at scale*. Recuperado el 1 de julio de 2026, de https://www.mckinsey.com/capabilities/mckinsey-technology/our-insights/building-the-foundations-for-agentic-ai-at-scale

McKinsey/QuantumBlack. (s.f.). *ARK — Agentic Runtime for Kubernetes* [repositorio de código]. GitHub. Recuperado el 2 de julio de 2026, de https://github.com/mckinsey/agents-at-scale-ark

Mittal, A., Belotserkovskiy, R., y Liakopoulou, T. (2026, 5 de febrero). *Redefining procurement performance in the era of agentic AI*. McKinsey & Company (Operations Practice). Recuperado el 1 de julio de 2026, de https://www.mckinsey.com/capabilities/operations/our-insights/redefining-procurement-performance-in-the-era-of-agentic-ai

Mittal, A., Cocoual, C., Erriquez, M., y Liakopoulou, T. (2024, 13 de junio). *Revolutionizing procurement: Leveraging data and AI for strategic advantage*. McKinsey & Company (Operations Practice). Recuperado el 1 de julio de 2026, de https://www.mckinsey.com/capabilities/operations/our-insights/revolutionizing-procurement-leveraging-data-and-ai-for-strategic-advantage

Outpost24. (2026). *How an AI agent hacked McKinsey's AI platform*. Recuperado el 1 de julio de 2026, de https://outpost24.com/blog/ai-agent-hacked-mckinsey-ai-platform/

Schmidt, J., Samuels, R., y Khushalani, S. (2025, 27 de octubre). *Transforming procurement functions for an AI-driven world*. McKinsey & Company (Operations Practice). Recuperado el 1 de julio de 2026, de https://www.mckinsey.com/capabilities/operations/our-insights/transforming-procurement-functions-for-an-ai-driven-world

Schumacher, K., Roberts, R., y Giebel, K. (2025, 17 de octubre). *The agentic commerce opportunity: How AI agents are ushering in a new era for consumers and merchants*. McKinsey & Company / QuantumBlack. Recuperado el 1 de julio de 2026, de https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-agentic-commerce-opportunity-how-ai-agents-are-ushering-in-a-new-era-for-consumers-and-merchants

Starkloff, A.-G., Kokaina, S., y Rahimi, S. (2026, 29 de enero). *Evaluations for the agentic world*. QuantumBlack, AI by McKinsey (Medium). Recuperado el 1 de julio de 2026, de https://medium.com/quantumblack/evaluations-for-the-agentic-world-c3c150f0dd5a

Sukharevsky, A., Kerr, D., Hjartar, K., Hämäläinen, L., Bout, S., y Di Leo, V. (2025, 13 de junio). *Seizing the agentic AI advantage*. McKinsey & Company / QuantumBlack. Recuperado el 1 de julio de 2026, de https://www.mckinsey.com/capabilities/quantumblack/our-insights/seizing-the-agentic-ai-advantage

The Money Times. (2026, 13 de enero). *McKinsey CEO Bob Sternfels says the firm now has 60,000 employees: 25,000 of them are AI agents*. Recuperado el 1 de julio de 2026, de https://themoneytimes.media/2026/01/13/mckinsey-ceo-bob-sternfels-says-the-firm-now-has-60-000-employees-25-000-of-them-are-ai-agents/

Tournesac, A., Gundurao, A., Lau, L., y Sachdeva, P. (2026, 23 de abril). *Reimagining tech infrastructure for and with agentic AI*. McKinsey & Company (McKinsey Technology). Recuperado el 1 de julio de 2026, de https://www.mckinsey.com/capabilities/mckinsey-technology/our-insights/reimagining-tech-infrastructure-for-and-with-agentic-ai

Varanasi, L. (2026, 13 de febrero). *McKinsey says it has 25,000 AI agents*. Business Insider (sindicado en Yahoo Finance). Recuperado el 1 de julio de 2026, de https://finance.yahoo.com/news/mckinsey-says-25-000-ai-103101624.html

VentureBeat. (2023). *Consulting giant McKinsey unveils its own generative AI tool for employees: Lilli*. Recuperado el 1 de julio de 2026, de https://venturebeat.com/ai/consulting-giant-mckinsey-unveils-its-own-generative-ai-tool-for-employees-lilli

Yee, L., Chui, M., Roberts, R., y Xu, S. (2024, 24 de julio). *Why agents are the next frontier of generative AI*. McKinsey & Company (McKinsey Digital). Recuperado el 1 de julio de 2026, de https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/why-agents-are-the-next-frontier-of-generative-ai

Yee, L., Chui, M., Roberts, R., y Xu, S. (2025, 12 de septiembre). *One year of agentic AI: Six lessons from the people doing the work*. McKinsey & Company / QuantumBlack. Recuperado el 1 de julio de 2026, de https://www.mckinsey.com/capabilities/quantumblack/our-insights/one-year-of-agentic-ai-six-lessons-from-the-people-doing-the-work

---

*Documento elaborado por el Equipo de investigación multiagente — Proyecto Agentes-Procurement-MCS. 2 de julio de 2026.*






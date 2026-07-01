# Hallazgos — Agente Investigador 1: Productos y Plataformas Agénticas de McKinsey para Procurement

**Ventana temporal de investigación:** julio 2024 – julio 2026
**Fecha de elaboración:** 2026-07-01
**Alcance:** Lilli, QuantumBlack/Horizon, ofertas de procurement/sourcing (incl. Orpheus GmbH), anuncios oficiales de agentic AI en operaciones/compras.

**Leyenda de confiabilidad:**
- 🟢 HECHO VERIFICADO — múltiples fuentes independientes o fuente primaria directa (mckinsey.com, comunicado oficial)
- 🟡 AFIRMACIÓN DEL VENDOR — declarado por McKinsey/QuantumBlack sin verificación externa independiente
- 🔵 INFERENCIA — deducción propia del investigador, no declarada explícitamente por la fuente

---

## 1. Lilli (plataforma de IA generativa interna de McKinsey)

### 1.1 Descripción general y evolución

🟢 **HECHO VERIFICADO.** Lilli es la herramienta interna de IA generativa de McKinsey, lanzada en julio de 2023 para uso de los consultores. Agrega más de 40 fuentes de conocimiento y capacidades internas de la firma.
Fuente: "Rewiring the way McKinsey works with Lilli, our generative AI platform", McKinsey & Company, s.f. (consultado 2026-07-01), https://www.mckinsey.com/capabilities/tech-and-ai/how-we-help-clients/rewiring-the-way-mckinsey-works-with-lilli

🟢 **HECHO VERIFICADO — cifras de adopción (fuente primaria McKinsey):** 72% de la firma activa en la plataforma; más de 500,000 prompts mensuales; ahorro de hasta 30% del tiempo en "búsqueda y síntesis de conocimiento".
Fuente: McKinsey & Company, "Rewiring the way McKinsey works with Lilli, our generative AI platform" (consultado 2026-07-01), https://www.mckinsey.com/capabilities/tech-and-ai/how-we-help-clients/rewiring-the-way-mckinsey-works-with-lilli

🟢 **HECHO VERIFICADO (cifra distinta, fuente periodística, dato de rollout inicial):** McKinsey desplegó Lilli a 7,000 empleados en su lanzamiento inicial (2023).
Fuente: "McKinsey rolls out generative AI tool 'Lilli' to 7K employees", CIO Dive, 2023 (consultado 2026-07-01), https://www.ciodive.com/news/McKinsey-generative-AI-Lilli-platform-internal-employees/691231/

🟡 **AFIRMACIÓN DE PRENSA NO-PRIMARIA (requiere verificación adicional).** Reportes de prensa especializada en ciberseguridad de marzo de 2026 afirman que Lilli era usada por "el 70% de la fuerza laboral global de la firma" al momento de un incidente de seguridad (ver sección de guardrails/seguridad abajo). Esta cifra es consistente con el 72% declarado por McKinsey, lo que sugiere razonable veracidad, pero proviene de fuentes secundarias (blogs de seguridad, no McKinsey ni medios establecidos de primera línea).
Fuentes: "McKinsey Lilli Breach (2026): What It Reveals About Agent Authentication", 1Kosmos, 2026 (consultado 2026-07-01), https://www.1kosmos.com/resources/blog/mckinsey-lilli-breach-agent-authentication ; "How an AI Agent Hacked McKinsey's AI Platform", Outpost24, 2026 (consultado 2026-07-01), https://outpost24.com/blog/ai-agent-hacked-mckinsey-ai-platform/

🔴 **ALERTA — INCIDENTE DE SEGURIDAD IMPORTANTE (marzo 2026), requiere validación cruzada adicional antes de darlo por hecho verificado.** Múltiples fuentes de ciberseguridad (no McKinsey) reportan que el 11 de marzo de 2026 la startup de seguridad "CodeWall" apuntó un agente de IA ofensivo autónomo contra Lilli y obtuvo acceso de lectura/escritura a la base de datos de producción en dos horas, sin credenciales ni intervención humana, explotando una falla de inyección SQL en un endpoint de API no autenticado. Se menciona acceso a 46 millones de mensajes. Esto es MUY relevante como lección de guardrails/seguridad para el diseño de sistemas agénticos propios — documentar como riesgo de referencia aunque no esté confirmado por McKinsey directamente.
Fuentes: "State of Surveillance", "An AI Agent Hacked McKinsey's AI Platform in Two Hours — Accessed 46 Million Messages", 2026 (consultado 2026-07-01), https://stateofsurveillance.org/news/mckinsey-lilli-ai-agent-hack-codewall-sql-injection-2026/ ; "CodeWall hacked McKinsey's AI Platform Lilli Through Unprotected API Endpoints", Treblle, 2026 (consultado 2026-07-01), https://treblle.com/blog/codewall-hack-mckinsey-ai-platform-lilli ; "McKinsey Lilli AI Hack 2026: 5 Alarming Security Failures Every Enterprise Deploying AI Must Face Now", Medium (Daniel Ikechukwu), 2026 (consultado 2026-07-01), https://medium.com/@creed_1732/mckinsey-lilli-ai-hack-2026-5-alarming-security-failures-every-enterprise-deploying-ai-must-face-2a9b66c2e3a3
**ACTUALIZACIÓN — CONFIRMADO POR FUENTE PRIMARIA OFICIAL DE McKINSEY (encontrado en pasada posterior de investigación):**

🟢 **HECHO VERIFICADO — comunicado oficial de McKinsey.** McKinsey publicó un comunicado oficial titulado "Statement on Strengthening Safeguards Within the Lilli Tool", el 11 de marzo de 2026, confirmando parcialmente el incidente pero con matices importantes respecto a las versiones sensacionalistas de la prensa de seguridad: McKinsey fue alertada de una vulnerabilidad en Lilli por un investigador de seguridad, y "confirmó y corrigió el problema en cuestión de horas". La investigación de McKinsey, con apoyo de una firma forense externa líder, "no identificó evidencia de que datos de clientes o información confidencial de clientes hayan sido accedidos por este investigador o cualquier otro tercero no autorizado". McKinsey declaró que sus "sistemas de ciberseguridad son robustos" y que "no tienen mayor prioridad que la protección de los datos e información de los clientes que se les ha confiado".
Fuente: "Statement on Strengthening Safeguards Within the Lilli Tool", McKinsey & Company, 2026-03-11 (consultado 2026-07-01), https://www.mckinsey.com/about-us/media/statement-on-strengthening-safeguards-within-the-lilli-tool

🔵 **INFERENCIA propia — contraste entre versión oficial y versión de prensa de seguridad.** Existe una discrepancia notable entre el relato de McKinsey (vulnerabilidad puntual, corregida en horas, sin acceso a datos de clientes) y el relato de los blogs de ciberseguridad (acceso de lectura/escritura a producción en 2 horas sin credenciales, 46 millones de mensajes accedidos, explotación de inyección SQL en endpoint no autenticado, capacidad de modificar system prompts). Ambas versiones coinciden en la fecha (marzo 2026) y en que un actor externo (CodeWall, descrito como firma de seguridad/hacking ético) encontró y explotó una vulnerabilidad real. Para el diseño de sistemas propios, la lección de guardrails es válida independientemente de cuál versión sea más precisa: (1) validar inputs en todos los endpoints de API expuestos a agentes, (2) proteger contra inyección SQL incluso en sistemas con capas de IA, (3) restringir la capacidad de modificar system prompts en producción, (4) autenticar rigurosamente cualquier endpoint que un agente autónomo pueda alcanzar. **Este es el hallazgo de guardrails más concreto y accionable de toda la investigación de este agente.**
Fuentes adicionales sobre la versión no-oficial: "Autonomous Agent Hacked McKinsey's AI in 2 Hours", BankInfoSecurity, 2026 (consultado 2026-07-01), https://www.bankinfosecurity.com/autonomous-agent-hacked-mckinseys-ai-in-2-hours-a-31007 ; "How an AI Agent Hacked McKinsey and Exposed 46 Million Messages", NeuralTrust, 2026 (consultado 2026-07-01), https://neuraltrust.ai/blog/agent-hacked-mckinsey ; "McKinsey AI platform breach exposes millions of messages", PointGuard AI, 2026 (consultado 2026-07-01), https://www.pointguardai.com/ai-security-incidents/mckinsey-ai-chatbot-breach-exposes-millions-of-internal-messages

🟡 **AFIRMACIÓN DE VENDOR (cifra de agentes, declarada por CEO de McKinsey, reportada por prensa secundaria).** Se reporta que el CEO de McKinsey declaró que la firma "ha construido 25,000 agentes de IA" para apoyar a su fuerza laboral, y que McKinsey "opera 20,000 agentes de IA junto a 40,000 consultores" en 2026. Estas cifras provienen de fuentes agregadoras/blogs, no de un comunicado directo verificado de McKinsey citado con fecha y contexto precisos — tratar con cautela hasta confirmar en fuente primaria.
Fuente: resultados de búsqueda agregados citando declaraciones del CEO de McKinsey, 2026 (consultado 2026-07-01) — pendiente de localizar la fuente primaria original (posible discurso, entrevista o carta anual).

### 1.2 Arquitectura técnica conocida (LLMs, RAG, orquestación)

🟢 **HECHO VERIFICADO — arquitectura RAG confirmada por múltiples fuentes.** Lilli está construida sobre un pipeline de retrieval-augmented generation (RAG) a gran escala. La interfaz tiene dos pestañas: "GenAI Chat" (que usa un LLM de backend más general/genérico) y "Client Capabilities" (que responde desde el corpus propio de McKinsey de más de 100,000 documentos). Al recibir una pregunta, Lilli escanea el conocimiento de la firma, identifica entre 5 y 7 piezas de contenido más relevantes, resume puntos clave, incluye enlaces, e identifica expertos en el campo correspondiente.
Fuentes: "Consulting giant McKinsey unveils its own generative AI tool for employees: Lilli", VentureBeat, 2023 (consultado 2026-07-01), https://venturebeat.com/ai/consulting-giant-mckinsey-unveils-its-own-generative-ai-tool-for-employees-lilli ; "McKinsey Lilli Breach (2026)", 1Kosmos (consultado 2026-07-01), https://www.1kosmos.com/resources/blog/mckinsey-lilli-breach-agent-authentication

🔵 **INFERENCIA propia.** McKinsey no ha publicado en fuentes primarias qué proveedor(es) de LLM específicos alimenta(n) a Lilli (p. ej. no se confirma si es OpenAI/Azure OpenAI, Anthropic, Google, o modelos propios). Dado que McKinsey mantiene alianzas públicas y ampliamente reportadas con OpenAI, Microsoft/Azure, Google Cloud y Anthropic (ver más abajo en QuantumBlack/Agentic AI Mesh, que menciona explícitamente soporte "vendor-agnostic" para múltiples LLMs), es plausible que Lilli use una arquitectura multi-modelo o gateway de IA, pero esto NO está confirmado explícitamente para Lilli en ninguna fuente consultada hasta ahora. Marcado como brecha de información (ver sección 5).

### 1.3 "Lilli for Client Capabilities" / despliegues a clientes

🟢 **HECHO VERIFICADO.** McKinsey ofrece a sus clientes una versión personalizable de la arquitectura subyacente de Lilli, adaptada a la industria y trabajo específico de cada organización. QuantumBlack (la unidad de IA de McKinsey) trabaja con clientes para llevar el poder de Lilli a sus propias organizaciones, incluyendo casos de uso como la creación de un "motor de RFP" (request-for-proposal engine — directamente relevante para procurement/sourcing) y la aceleración de operaciones de desarrollo de fármacos.
Fuente: "Rewiring the way McKinsey works with Lilli, our generative AI platform", McKinsey & Company (consultado 2026-07-01), https://www.mckinsey.com/capabilities/tech-and-ai/how-we-help-clients/rewiring-the-way-mckinsey-works-with-lilli

🔵 **INFERENCIA propia — relevancia directa para procurement.** El caso de uso de "motor de RFP" mencionado explícitamente por McKinsey es la evidencia más directa encontrada hasta ahora de una aplicación de la arquitectura de Lilli específicamente al dominio de sourcing/procurement (generación/gestión de Request for Proposals). No se encontró detalle técnico adicional sobre cómo funciona este motor de RFP específico — posible brecha para profundizar.

### 1.4 Capacidades agénticas (evolución 2024-2026)

🟢 **HECHO VERIFICADO — hoja de ruta declarada por McKinsey.** Como característica futura (anunciada en la página de producto, sin fecha específica de lanzamiento), McKinsey planea incorporar a Lilli "agentes construidos para automatizar tareas específicas que consumen mucho tiempo" y expandir las "capacidades de construcción de diapositivas" (slide-building).
Fuente: McKinsey & Company, "Rewiring the way McKinsey works with Lilli, our generative AI platform" (consultado 2026-07-01), https://www.mckinsey.com/capabilities/tech-and-ai/how-we-help-clients/rewiring-the-way-mckinsey-works-with-lilli

🔵 **INFERENCIA propia.** No se encontró un anuncio específico y fechado de "Lilli 2.0" o un rebranding agéntico formal de Lilli entre julio 2024 y julio 2026 en las fuentes primarias revisadas hasta ahora. La evolución agéntica de McKinsey parece estar canalizada más bien a través de QuantumBlack (Agentic AI Mesh, Agents at Scale — ver sección 2) que como una evolución con nombre propio de Lilli. Pendiente de búsqueda adicional específica sobre "Lilli agents" o "Lilli 2.0".

---

## 2. QuantumBlack (AI by McKinsey)

### 2.1 Horizon

🟢 **HECHO VERIFICADO.** QuantumBlack Horizon es una suite de herramientas para desarrollo y despliegue de IA, anunciada en junio de 2023, que permite a las organizaciones pasar de prueba de concepto a IA productivizada a escala. Horizon ayuda a los clientes de McKinsey a descubrir, ensamblar, personalizar y orquestar proyectos de IA. Establece fundaciones "tipo fábrica" para proyectos de IA generativa, incluyendo un stack tecnológico con herramientas como AI4DQ, FUSE2 y Data Fabricator para curación de datos.
Fuente: "QuantumBlack Horizon: Unleashing the power of generative AI", QuantumBlack/Medium, 2023 (consultado 2026-07-01), https://medium.com/quantumblack/quantumblack-horizon-unleashing-the-power-of-generative-ai-a3022597c642

🟡 **AFIRMACIÓN DEL VENDOR.** Desde mediados de 2023, cuando McKinsey abrió QuantumBlack Horizon a todas sus prácticas, los consultores pueden desplegar agentes de IA específicos para tareas dentro del mismo entorno seguro que alimenta a Lilli. QuantumBlack ofrece "Agents at Scale", descrito como "la fábrica de agentes de IA de QuantumBlack que trabajan juntos para entregar transformaciones digitales complejas".
Fuente: agregación de resultados de búsqueda sobre QuantumBlack (consultado 2026-07-01) — requiere verificación en fuente primaria específica de "Agents at Scale" (pendiente de fetch directo).

🟡 **AFIRMACIÓN DEL VENDOR — catálogo de herramientas propietarias.** QuantumBlack (QB) ofrece más de 25 herramientas propietarias, incluyendo: **Iguazio** (plataforma holística de IA para gestionar aplicaciones de IA a escala — nota: Iguazio fue una adquisición de McKinsey/QuantumBlack de una empresa israelí de MLOps), **Turo** (aplicación para automatizar la recolección de KPIs), y **Optimus AI** (herramienta de insights de datos para toma de decisiones en tiempo real en industrias pesadas como minería, metales y químicos).
Fuente: agregación de resultados de búsqueda (consultado 2026-07-01) — ninguna de estas tres herramientas (Iguazio, Turo, Optimus AI) parece ser específica de procurement; se documentan aquí como contexto de la plataforma QuantumBlack en general.

### 2.2 Otras herramientas/frameworks agénticos publicados — Agentic AI Mesh

🟢 **HECHO VERIFICADO — fuente primaria QuantumBlack/Medium con autoría y fecha.** El "Agentic AI Mesh" es una arquitectura publicada por QuantumBlack el 12 de junio de 2025, escrita por Dave Kerr (con contribuciones de Dante Gabrielli, Roman Galeev, Sallah Kokaina, Chi Wai Cheung, Chris Madden y Jo Stichbury). Se describe como "una arquitectura composable, distribuida y agnóstica de proveedor que permite a los agentes razonar, colaborar y actuar de forma autónoma a través de herramientas, sistemas y LLMs — de forma segura, a escala".
Fuente: Kerr, D. et al., "How we enabled Agents at Scale in the Enterprise with the Agentic AI Mesh", QuantumBlack/Medium, 2025-06-12 (consultado 2026-07-01), https://medium.com/quantumblack/how-we-enabled-agents-at-scale-in-the-enterprise-with-the-agentic-ai-mesh-baf4290daf48

**Detalle técnico extraído (🟢 HECHO VERIFICADO, fuente primaria directa):**

- **Frameworks de agentes soportados:** Autogen, LangGraph, CrewAI, Google ADK — tanto soluciones internas como de terceros dentro de un ecosistema heterogéneo. QuantumBlack provee una "implementación de referencia lista para usar".
- **Integración de LLMs:** soporta soluciones SaaS detrás de gateways de IA y modelos on-premises air-gapped; habilita LLMs especializados por tema, técnica y modalidad (multi-modelo, vendor-agnostic — confirma la inferencia hecha en sección 1.2 sobre posible arquitectura multi-modelo, aunque esto se documenta para la plataforma de agentes en general, no específicamente para Lilli).
- **Estándares y protocolos:** Agent2Agent Protocol (A2A), Model Context Protocol (MCP), OpenTelemetry (para observabilidad), OAuth 2.0 y JSON Web Tokens (JWT) para autenticación.
- **Capacidades arquitectónicas (7 componentes):**
  1. Descubrimiento de agentes y flujos de trabajo — catalogación de agentes con taxonomía estandarizada.
  2. AI Asset Registry — gobernanza centralizada de system prompts, instrucciones de agentes, configuraciones de LLM, definiciones de herramientas (tools) y controles de flujo de trabajo.
  3. Observabilidad — trazabilidad de cadena de eventos, gestión de costos, monitoreo de cumplimiento a través de sistemas agénticos y procedimentales.
  4. Autenticación y autorización — controles de acceso granular usando el "principio de privilegio mínimo" (least privilege).
  5. Evaluaciones — pruebas exhaustivas a nivel de paso, de flujo de trabajo, y de interacción a largo plazo.
  6. Fine-tuning y ciclos de retroalimentación — mecanismos de aprendizaje por refuerzo con retroalimentación humana (RLHF) y métricas de uso de tokens.
  7. Cumplimiento, riesgo y ética — agentes de cumplimiento para aplicación de políticas y salvaguardas éticas.
- **Enfoque de integración:** énfasis en "translocación creciente de cargas de trabajo entre sistemas agénticos y procedimentales", permitiendo que flujos de trabajo críticos (hot-path) alternen entre ejecución basada en reglas y ejecución impulsada por LLM, manteniendo modularidad y portabilidad.

🔵 **INFERENCIA propia — relevancia para diseño propio.** Esta arquitectura de Agentic AI Mesh es, hasta ahora, el hallazgo técnico MÁS ACCIONABLE de toda la investigación en el área de plataformas: es un blueprint de referencia arquitectónica (no específico de procurement, pero aplicable) que cubre exactamente las piezas que necesitaríamos para diseñar un sistema agéntico propio: orquestación multi-framework, registro de activos de IA, observabilidad, autenticación, evaluación y guardrails de cumplimiento. Recomendado leer el artículo completo y el paper relacionado "Creating a future-proof enterprise agentic platform architecture" (misma serie de QuantumBlack/Medium) para el equipo de diseño de fase 2.
Fuente relacionada no explorada en profundidad aún: "Creating a future-proof enterprise agentic platform architecture", QuantumBlack/Medium (consultado 2026-07-01), https://medium.com/quantumblack/creating-a-future-proof-enterprise-agentic-platform-architecture-c21fc48406a5 — **pendiente de fetch dedicado**.

🟢 **HECHO VERIFICADO — evaluaciones de agentes.** QuantumBlack publicó también un artículo específico sobre metodologías de evaluación de sistemas agénticos ("Evaluations for the agentic world"), relevante para la sección de guardrails/testing.
Fuente: "Evaluations for the agentic world", QuantumBlack/Medium (consultado 2026-07-01), https://medium.com/quantumblack/evaluations-for-the-agentic-world-c3c150f0dd5a — **pendiente de fetch dedicado para extraer detalle técnico completo**.

---

## 3. Ofertas específicas de Procurement/Sourcing

### 3.1 Legado de la adquisición de Orpheus GmbH → Spendscape by McKinsey

🟢 **HECHO VERIFICADO — adquisición.** McKinsey anunció la adquisición de Orpheus GmbH el 6 de febrero de 2020. Orpheus, fundada en Alemania en 2005 y con sede en Núremberg, era proveedora líder de tecnología de spend analytics e innovadora reconocida en procurement digital. El software de Orpheus optimizaba el gasto externo de las organizaciones analizando flujos de datos de compra para identificar oportunidades de captura de valor y medir el impacto real en procurement.
Fuentes: "Why we acquired a company that specializes in spend analytics", McKinsey & Company, 2020 (consultado 2026-07-01), https://www.mckinsey.com/about-us/new-at-mckinsey-blog/why-we-acquired-a-company-that-specializes-in-spend-analytics ; "McKinsey buys Orpheus and launches Spend Intelligence offering", Consultancy.eu, 2020 (consultado 2026-07-01), https://www.consultancy.eu/news/3830/mckinsey-buys-orpheus-and-launches-spend-intelligence-offering ; "Carlsquare advised Orpheus GmbH on the sale to McKinsey", Carlsquare, 2020 (consultado 2026-07-01), https://carlsquare.com/deal-history/carlsquare-advised-spend-analytics-software-technology-company-orpheus-gmbh-on-the-sale-to-mckinsey/

🟢 **HECHO VERIFICADO — capacidades técnicas originales de Orpheus (pre-rebranding, 2020).** Extracción automatizada de datos ("automated data extraction"); categorización de gasto habilitada por IA ("AI-enabled spend categorization"); analítica prescriptiva y predictiva de gasto y categorías, incluyendo agentes de software (BOTs) para automatización de procurement; sistemas de seguimiento de impacto en procurement. Nótese que ya en 2020, antes de la ola de "agentic AI" de 2023-2026, Orpheus usaba el término "software agents (BOTs)" para su automatización — un precedente temprano no equivalente a los agentes basados en LLM actuales.
Fuente: "A new approach to digital procurement—Orpheus, a McKinsey company", McKinsey & Company, 2020 (consultado 2026-07-01), https://www.mckinsey.com/capabilities/operations/our-insights/operations-blog/a-new-approach-to-digital-procurement-orpheus-by-mckinsey

🟢 **HECHO VERIFICADO — rebranding a Spendscape (2023) y estado actual (dentro de la ventana de investigación).** El servicio fue rebrandeado de "Orpheus, a McKinsey company" / "Spend Intelligence by McKinsey" a **Spendscape by McKinsey** en 2023. Spendscape ha sido reconocida como líder de mercado por Spend Matters en su SolutionMap de Spend Analytics.
Fuente: "Spendscape fifth anniversary", McKinsey & Company (Spendscape by McKinsey, página de producto), s.f. (consultado 2026-07-01), https://www.mckinsey.com/capabilities/operations/tech-tools/spendscape-technology/our-updates/spendscape-fifth-anniversary ; "Spendscape by McKinsey", Spend Matters (directorio de proveedores), s.f. (consultado 2026-07-01), https://spendmatters.com/vendor-directory/orpheus/

**Detalle técnico de Spendscape (estado 2025-2026, dentro de la ventana de investigación):**

🟢 **HECHO VERIFICADO (fuente primaria McKinsey) — funcionalidades actuales:**
- Transparencia y reporte granular de gasto ("spend transparency")
- Analítica de categorías y proveedores
- Gestión inteligente de volatilidad de precios
- Módulos de mitigación de riesgo
- Recomendaciones "impulsadas por IA" ("AI-powered recommendations") para decisiones basadas en datos — **nota: el término usado es "AI-powered", no se especifica si involucra LLMs/agentes generativos o modelos de ML tradicionales/predictivos**
- Transparencia y reporte de emisiones de alcance 3 (Scope-3), seguimiento de dimensión de carbono y sostenibilidad
- Gestión y seguimiento de oportunidades de ahorro, integrado con **Wave by McKinsey** (otro producto de McKinsey, pendiente de investigar en detalle — posible solapamiento con otro agente investigador del equipo)
- Capacidades de minería de procesos mediante integración/asociación con **Celonis**

🟢 **HECHO VERIFICADO — stack tecnológico declarado:**
- Construido sobre "tecnologías de arquitectura de plataforma más recientes" (frase genérica, sin especificidad técnica)
- Ofrecido sobre **SAP BTP (Business Technology Platform)** para flujo de datos fluido — este es el dato técnico de infraestructura más concreto encontrado sobre Spendscape
- Múltiples alianzas de datos para información de mercado, riesgo, diversidad de proveedores y emisiones

🟡 **AFIRMACIÓN DEL VENDOR — hoja de ruta futura (más relevante para nuestra investigación agéntica).** McKinsey menciona en la página de producto de Spendscape funcionalidades futuras ("upcoming") que incluyen: módulos de "negotiation excellence" (excelencia en negociación) e **"iniciativas de ahorro de costos impulsadas por gen AI"** ("gen AI-powered cost savings initiatives"), además de movimiento hacia "insights automatizados e innovación de plataforma". Esta es la referencia más explícita encontrada hasta ahora de una intención declarada de incorporar IA generativa (posiblemente agéntica) directamente al producto de spend intelligence de McKinsey — pero sin fecha de lanzamiento concreta ni detalle de arquitectura.
Fuente: "Spendscape fifth anniversary", McKinsey & Company (consultado 2026-07-01), https://www.mckinsey.com/capabilities/operations/tech-tools/spendscape-technology/our-updates/spendscape-fifth-anniversary

⚠️ **BRECHA IMPORTANTE:** No se encontró, en esta primera pasada, ninguna fuente que confirme que Spendscape ya tenga agentes de IA generativa/LLM desplegados en producción (más allá de la promesa de roadmap citada arriba). No hay evidencia de integración entre Spendscape y Lilli/QuantumBlack Agentic AI Mesh — sería lógico que existiera dado que ambos son productos de McKinsey, pero no está documentado públicamente. Ver sección 5.

### 3.2 Práctica "Product Development & Procurement" / artículo central de agentic AI en procurement

🟢 **HECHO VERIFICADO — FUENTE PRIMARIA CENTRAL de toda la investigación de este agente.** McKinsey publicó el artículo "Redefining procurement performance in the era of agentic AI", con autoría de **Aasheesh Mittal, Roman Belotserkovskiy y Theano Liakopoulou**, fechado **5 de febrero de 2026** (dentro de la ventana de investigación). Es un artículo de 7 páginas de la práctica de Operations de McKinsey.
Fuente: Mittal, A., Belotserkovskiy, R., & Liakopoulou, T. (2026-02-05). "Redefining procurement performance in the era of agentic AI". McKinsey & Company (consultado 2026-07-01), https://www.mckinsey.com/capabilities/operations/our-insights/redefining-procurement-performance-in-the-era-of-agentic-ai

**Definición de "agentes de procurement" (🟢 cita directa de fuente primaria):** Sistemas que "emulan el juicio humano, ejecutan tareas de múltiples pasos y mejoran continuamente a través de ciclos de aprendizaje". A diferencia de dashboards estáticos, estos agentes "ingieren conjuntos de datos complejos, razonan sobre trade-offs, y generan opciones de forma autónoma". El artículo marca la transición de IA analítica ("muéstrame los datos") a IA agéntica ("hazlo por mí").

**Casos de uso cuantificados con cifras específicas por empresa (🟢 HECHO VERIFICADO — afirmaciones de McKinsey sobre clientes anónimos, no verificables externamente, pero de fuente primaria directa; tratar como 🟡 en cuanto a la veracidad de las cifras ya que son estudios de caso no auditables externamente):**

| Empresa (anónima) | Caso de uso agéntico | Resultado cuantificado |
|---|---|---|
| Empresa tecnológica | Sourcing de servicios externos (contact center, BPO) | Oportunidades de ahorro de 12-20% en operaciones de contact center; 20-29% de ahorro en gasto de BPO y servicios financieros; agentes integran datos de gasto/mercado para análisis de tendencias de precio en tiempo real |
| Empresa química | Categoría de consumibles — autonomous sourcing (agentes preparan licitaciones, identifican/precalifican proveedores, analizan ofertas competidoras, enrutan consultas) | +20-30% eficiencia del personal de procurement; +1-3% de captura de valor adicional |
| Telco | Negociación de precios en software especializado / long-tail spend (agentes preparan fact bases prenegociación, sugerencias en tiempo real, evalúan trade-offs costo/servicio/riesgo, generan contraofertas automáticamente) | Reducción de hasta 90% en tiempo de análisis y correo; 10-15% de ahorro entre proveedores |
| Farmacéutica | Cumplimiento de facturas (agentes hacen cumplir la conformidad factura-contrato y rastrean desempeño de entrega) | Reducción de 4% en pérdidas por fugas ("leakage losses") |
| OEM de aeronaves | Gestión de inventario — ejecución automatizada de órdenes basada en datos de planeación de producción | Reducción de 30% en inventario activo; incremento de ~$700 millones USD en EBIT |

**Marco de implementación — "4 cambios centrales" (🟢 HECHO VERIFICADO, fuente primaria):**
1. **Estrategia de datos:** las organizaciones actualmente utilizan menos del 20% de los datos de procurement disponibles. Se recomienda romper silos mediante una "columna vertebral de datos común" (common data spine) que dé una única fuente de verdad sobre gasto, proveedores, contratos y benchmarks.
2. **Infraestructura de agentes:** desplegar "fábricas de agentes" que manejan tareas específicas — importación de datos desde fuentes no estructuradas, análisis, conversación en lenguaje natural — ensambladas en flujos de trabajo.
3. **Colaboración humano-agente ("human-agent teaming"):** el personal se enfoca en toma de decisiones estratégicas, orquestación y supervisión, mientras los agentes manejan trabajo transaccional. Nuevas capacidades requeridas: prompt engineering, evaluación de escenarios, gestión del cambio.
4. **Integración de punta a punta:** aplicar IA a través de todo el ciclo de vida source-to-pay para beneficios compuestos.

**Hoja de ruta de implementación recomendada (🟢 fuente primaria):**
1. Activar soluciones ya disponibles "off-the-shelf" (category copilots, generación de RFx, optimización de contratos, cumplimiento de facturas, tail repricing)
2. Definir visión de largo plazo anclada en resultados de negocio
3. Seleccionar 2-3 categorías de alto impacto para enfoque inicial
4. Construir equipos multifuncionales (procurement, datos, IA, gestión del cambio)
5. Comenzar la construcción de capacidades de inmediato
6. Establecer ciclos de retroalimentación continua

**Métrica de ROI propuesta:** valor total creado dividido entre costo total de implementación, abarcando ahorros realizados, evitación de fugas, beneficios de capital de trabajo, reducción de riesgo y habilitación de ingresos. **Expectativa de cronograma:** de prototipos a pilotos en semanas; de pilotos a escala en menos de un año.

⚠️ **BRECHA:** el artículo NO nombra vendors o herramientas propietarias específicas de McKinsey (no menciona explícitamente si estos agentes corren sobre Spendscape, QuantumBlack Horizon, o el Agentic AI Mesh) — solo referencia genéricamente "large language models (LLMs)" como tecnología subyacente. Tampoco especifica mecanismos concretos de guardrails/gobernanza más allá de mencionar la necesidad de "guardrails claros", sin detalle operativo.

🟢 **HECHO VERIFICADO — cifras agregadas de eficiencia (de las búsquedas agregadas, consistentes con el artículo primario).** El análisis de McKinsey estima que la función de procurement podría ser 25-40% más eficiente con IA agéntica en general; específicamente, agentes autónomos de categoría (autonomous category agents) generan una ganancia de eficiencia de 15-30%.
Fuente: agregación de resultados de búsqueda citando el artículo de McKinsey (consultado 2026-07-01) — cifras consistentes con, pero no idénticas a, las de casos individuales del artículo primario fetcheado arriba (posible artículo companion o mismo artículo resumido en prensa).

🟡 **AFIRMACIÓN DE VENDOR — artículo relacionado adicional no explorado en profundidad.** Existe un artículo hermano "Transforming procurement functions for an AI-driven world" en McKinsey.com, cubierto también por Procurement Magazine y Digital Commerce 360 (noviembre 2025). Pendiente de fetch dedicado si se requiere más profundidad — no se exploró el contenido completo por límites de tiempo/alcance en esta pasada.
Fuentes candidatas: https://www.mckinsey.com/capabilities/operations/our-insights/transforming-procurement-functions-for-an-ai-driven-world ; "AI forces procurement to evolve — or be left behind", Digital Commerce 360, 2025-11-11 (consultado 2026-07-01), https://www.digitalcommerce360.com/2025/11/11/ai-procurement-mckinsey-report/

### 3.3 Spend intelligence / herramientas de sourcing agénticas adicionales — Wave by McKinsey

🟢 **HECHO VERIFICADO — Wave by McKinsey es una plataforma de gestión de programas de transformación (no exclusiva de procurement, pero con aplicación directa mencionada a procurement).** Wave combina "tecnología de gen AI, la experiencia comprobada de McKinsey, e insights extraídos de miles de transformaciones exitosas", soportando gestión de iniciativas e hitos, seguimiento de valor financiero y no financiero, definición de metas top-down, flujos de trabajo automatizados y dashboards en tiempo real.
Fuente: "Wave Program Management Software", McKinsey & Company (consultado 2026-07-01), https://www.mckinsey.com/capabilities/transformation/how-we-help-clients/wave/overview

🟢 **HECHO VERIFICADO — capacidades de IA declaradas:** base de conocimiento con acceso a más de 500,000 iniciativas para identificación de oportunidades y predicción de riesgos; "agentes de IA personalizados" (custom AI agents) que apoyan la planeación, predicen riesgos y aceleran la toma de decisiones; "AI coaching" embebido en el flujo de trabajo.
Fuente: McKinsey & Company, "Wave Program Management Software" (consultado 2026-07-01), https://www.mckinsey.com/capabilities/transformation/how-we-help-clients/wave/overview

🟢 **HECHO VERIFICADO — caso de uso de procurement con Wave, cifra concreta.** McKinsey documenta un "Procurement transformation program to reduce spend by $1 billion" utilizando Wave como sistema centralizado de tracking de iniciativas de procurement.
Fuente: "Procurement transformation program to reduce spend by $1 billion", McKinsey & Company (consultado 2026-07-01), https://www.mckinsey.com/capabilities/transformation/how-we-help-clients/wave/our-impact/procurement-transformation-program-to-reduce-spend-by-1-billion

🟢 **HECHO VERIFICADO — cifras de escala (de búsqueda agregada, consistente con la mención de Spendscape en sección 3.1 sobre integración savings-tracking con Wave).** Wave ha rastreado más de 340,000 iniciativas en más de 1,000 organizaciones, reflejando colectivamente más de $200 mil millones USD en gasto ("spend") gestionado. Vía el módulo "Integrated Impact Management" (parte de Spendscape, integrado con Wave — ver sección 3.1), clientes han gestionado ahorros por valor de $1,000 millones USD.
Fuentes: agregación de resultados de búsqueda (consultado 2026-07-01); "Procurement Savings Tracking Software", McKinsey & Company / Spendscape, https://www.mckinsey.com/capabilities/operations/tech-tools/spendscape-technology/our-offerings/savings-tracking-and-integrated-impact-management — **nota: la página de Wave fetcheada directamente mostró varias cifras como "placeholder zeros" ($0B+, 0K+), lo que sugiere que la página web tiene un bug de renderizado dinámico (JS) al momento del acceso — las cifras reales fueron obtenidas de snippets de búsqueda, no del fetch directo. Tratar con cautela y re-verificar si es posible.**

🔵 **INFERENCIA propia — relevancia para diseño propio.** Wave es la evidencia más clara de que McKinsey ya despliega "agentes de IA personalizados" en un producto de transformación con aplicación directa a procurement (savings tracking, gestión de iniciativas), aunque el detalle de qué hacen técnicamente esos agentes (arquitectura, LLM, autonomía) no está especificado en las páginas públicas revisadas. Se infiere que Wave y Spendscape están comercialmente integrados (Spendscape referencia explícitamente "integrated with Wave by McKinsey" para savings tracking), lo cual sugiere una posible arquitectura común o al menos interoperabilidad de datos entre los dos productos de procurement/operations de McKinsey.

---

## 4. Anuncios oficiales y notas de prensa (línea de tiempo jul 2024 – jul 2026)

### 4.1 Reporte central: "Seizing the agentic AI advantage" (QuantumBlack)

🟢 **HECHO VERIFICADO — fuente primaria con autoría completa.** McKinsey/QuantumBlack publicó el reporte "Seizing the agentic AI advantage" el **13 de junio de 2025**. Autores principales: **Alexander Sukharevsky, Dave Kerr, Klemens Hjartar, Lari Hämäläinen, Stéphane Bout y Vito Di Leo, con Guillaume Dagorret**, representando las perspectivas de QuantumBlack (AI by McKinsey) y McKinsey Technology. Contribuyentes adicionales agradecidos: Alena Fedorenko, Annie David, Clarisse Magnin, Lareina Yee, Larry Kanter, Michael Chui, Roger Roberts, Sarah Mulligan, Thomas Vlot y Timo Mauerhoefer.
Fuente: Sukharevsky, A., Kerr, D., Hjartar, K., Hämäläinen, L., Bout, S., & Di Leo, V. (2025-06-13). "Seizing the agentic AI advantage". McKinsey & Company / QuantumBlack (consultado 2026-07-01), https://www.mckinsey.com/capabilities/quantumblack/our-insights/seizing-the-agentic-ai-advantage (PDF: https://www.mckinsey.com/~/media/mckinsey/business%20functions/quantumblack/our%20insights/seizing%20the%20agentic%20ai%20advantage/seizing-the-agentic-ai-advantage.pdf)

**Detalle técnico extraído — MUY ACCIONABLE para diseño propio (🟢 HECHO VERIFICADO, fuente primaria directa):**

- **"Agentic AI Mesh" — 5 principios de diseño:** (1) Composabilidad (componentes plug-and-play), (2) Inteligencia distribuida (redes de agentes cooperativos), (3) Desacoplamiento en capas (separación modular de lógica), (4) Neutralidad de proveedor (evitar vendor lock-in), (5) Autonomía gobernada (controles embebidos).
- **7 capacidades centrales requeridas** (coincide y expande lo hallado en sección 2.2): descubrimiento de agentes/flujos de trabajo, registro de activos de IA, observabilidad, autenticación/autorización, evaluaciones, gestión de retroalimentación, y cumplimiento/gestión de riesgo.
- **Estándares abiertos preferidos sobre soluciones propietarias:** Model Context Protocol (MCP) y Agent2Agent Protocol (A2A).
- **Clasificación de modelos fundacionales por caso de uso (dato MUY concreto y accionable, con ejemplos de modelos reales nombrados por McKinsey):**
  1. Modelos de inferencia de baja latencia: **Mistral Small, Llama 3 8B, Gemini Nano, Claude Haiku**
  2. Modelos fine-tuneables para aplicaciones específicas de dominio
  3. Modelos embebidos ligeros para despliegue en el edge
  4. Modelos escalables de orquestación multiagente
  5. Modelos soberanos/auditables para sectores regulados
  **Nota importante:** esta es la primera y única mención explícita encontrada de nombres de modelos LLM específicos en cualquier fuente primaria de McKinsey revisada hasta ahora (incluyendo Claude Haiku de Anthropic), aunque está en el contexto general de arquitectura empresarial, no específico de Lilli ni de procurement.
- **Cambios de software empresarial hacia "agent-native":** se menciona explícitamente que Microsoft (Dynamics 365, Copilot Studio), Salesforce (Agentforce) y SAP (BTP con Joule) están reposicionando sus plataformas como "agent-native" — relevante dado que Spendscape ya corre sobre SAP BTP (ver sección 3.1), lo que sugiere una posible vía de integración futura entre Spendscape y capacidades agénticas de SAP Joule.
- **Enfoque de orquestación:** los agentes se integran vía APIs en el corto plazo, con transición hacia arquitecturas empresariales "agent-first" con interfaces legibles por máquina en lugar de UI/UX centradas en humanos.

**Estadísticas de adopción/impacto (🟡 AFIRMACIÓN DEL VENDOR, cifras de encuestas/estudios de McKinsey, no verificadas externamente):**
- 78% de las empresas ha desplegado IA generativa (frente a 55% el año anterior)
- Más del 80% reporta que no ha tenido contribución material a las ganancias (earnings) todavía
- Menos del 10% de los casos de uso verticales progresan más allá de la fase piloto
- 70% de las empresas Fortune 500 usan Microsoft 365 Copilot (como ejemplo de despliegue horizontal)

**Casos de uso con ROI cuantificado (🟡 AFIRMACIÓN DEL VENDOR, no específicos de procurement pero relevantes como benchmark):**
- Modernización bancaria: reducción de más del 50% en tiempo/esfuerzo de desarrollo
- Firma de investigación: potencial de 60% de ganancia de productividad; ahorro anual proyectado de más de $3 millones USD
- Notas de crédito de banca minorista: incremento de productividad de 20-60%; mejora de 30% en tiempo de respuesta
- Centro de llamadas (rediseño completo hipotético): 80% de resolución autónoma; reducción de tiempo de 60-90%

### 4.2 Alianzas estratégicas relevantes (2026)

🟢 **HECHO VERIFICADO — alianza con Google Cloud.** En abril de 2026, McKinsey & Company y Google Cloud anunciaron el **"McKinsey Google Transformation Group"**, combinando la experiencia estratégica y de industria de McKinsey con el stack de IA de Google Cloud para ayudar a los clientes a convertir la ambición de IA en valor de negocio sostenido. Como parte de esta colaboración, los tecnólogos de QuantumBlack de McKinsey colaborarán con los "forward deployed engineers" de Google para prototipar y entregar soluciones y agentes de IA escalados y específicos por industria.
Fuente: "McKinsey and Google Cloud Launch the McKinsey Google Transformation Group to Scale Enterprise Impact for the AI era", PR Newswire, 2026-04 (consultado 2026-07-01), https://www.prnewswire.com/news-releases/mckinsey-and-google-cloud-launch-the-mckinsey-google-transformation-group-to-scale-enterprise-impact-for-the-ai-era-302749247.html

🟢 **HECHO VERIFICADO — alianza con AppliedAI/Opus.** En mayo de 2026, AppliedAI anunció una colaboración con McKinsey para ayudar a empresas en industrias reguladas a "rewire" sus operaciones de middle- y back-office con IA agéntica, combinando Opus (de AppliedAI) con la experiencia de transformación de McKinsey y las capacidades técnicas de QuantumBlack.
Fuente: "AppliedAI and McKinsey partner to deliver agentic AI to regulated enterprises", Opus by AppliedAI Newsroom, 2026-05 (consultado 2026-07-01), https://www.opus.com/news/mckinsey-may-2026
⚠️ Nota: no se encontró mención explícita de procurement/sourcing como industria o función objetivo específica de esta alianza — se documenta como contexto de la estrategia agéntica general de McKinsey/QuantumBlack en la ventana temporal de investigación.

🟡 **AFIRMACIÓN DEL VENDOR — cronología narrativa de QuantumBlack Labs.** Según material de marketing agregado, la iniciativa de QuantumBlack en agentes empezó "hace más de dos años" (es decir ~2024) con experimentos de uso de gen AI para modernizar código legado (ver ejemplo COBOL→Java de sección 2.2), y "el verano pasado" (interpretado como verano boreal 2025) comenzaron a explorar agentes de IA de forma más amplia, construyendo hoy "fuerzas de trabajo agénticas" (agentic workforces). QuantumBlack Labs lidera el trabajo de McKinsey en agentes de IA — diseñando sistemas autónomos específicos de dominio que pueden razonar, decidir y actuar en nombre de los usuarios, apoyando a clientes en áreas como optimización de cadena de suministro, desarrollo de software, servicio al cliente y operaciones financieras.
Fuente: agregación de resultados de búsqueda sobre QuantumBlack Labs (consultado 2026-07-01) — **nota: "optimización de cadena de suministro" se menciona como área de aplicación, adyacente pero no idéntica a procurement/sourcing; no hay mención explícita separada de "procurement" en esta cronología narrativa de QuantumBlack Labs.**

### 4.3 Línea de tiempo consolidada (hechos con fecha confirmada, dentro y cerca de la ventana jul 2024 – jul 2026)

| Fecha | Evento | Confiabilidad |
|---|---|---|
| 2020-02-06 | Adquisición de Orpheus GmbH (antecedente, fuera de ventana pero relevante) | 🟢 |
| 2023 (verano) | Rebranding de Orpheus/Spend Intelligence a Spendscape by McKinsey | 🟢 |
| 2025-06-12 | Publicación "How we enabled Agents at Scale... Agentic AI Mesh" (QuantumBlack/Medium, Dave Kerr et al.) | 🟢 |
| 2025-06-13 | Publicación reporte "Seizing the agentic AI advantage" (QuantumBlack) | 🟢 |
| 2025-11-11 | Cobertura de "Transforming procurement functions for an AI-driven world" en Digital Commerce 360 | 🟢 (fecha de cobertura de prensa; fecha exacta de publicación del artículo McKinsey original no confirmada aún) |
| 2026-02-05 | Publicación "Redefining procurement performance in the era of agentic AI" (Mittal, Belotserkovskiy, Liakopoulou) | 🟢 |
| 2026-03-09 | CodeWall anuncia que su agente de IA "hackeó" Lilli (versión no oficial) | 🟢 (hecho del anuncio; detalles técnicos del hackeo no confirmados por McKinsey) |
| 2026-03-11 | Comunicado oficial de McKinsey sobre el incidente de seguridad de Lilli | 🟢 |
| 2026-04 | Lanzamiento del "McKinsey Google Transformation Group" (alianza con Google Cloud) | 🟢 |
| 2026-05 | Alianza AppliedAI/Opus + McKinsey para IA agéntica en industrias reguladas | 🟢 |

---

## 5. Brechas de información identificadas

1. **Arquitectura de LLM de Lilli no confirmada.** McKinsey nunca ha publicado en fuente primaria qué proveedor(es) de LLM alimenta(n) específicamente a Lilli (OpenAI, Azure OpenAI, Anthropic, Google, modelos propios, o combinación multi-modelo vía gateway). Solo se confirma la existencia de un pipeline RAG y una interfaz de dos pestañas (GenAI Chat / Client Capabilities).

2. **Sin confirmación de integración entre Spendscape y las capacidades agénticas de QuantumBlack (Agentic AI Mesh) o Lilli.** Ambos existen como productos separados de McKinsey; es lógico inferir integración, pero no está documentada públicamente.

3. **Sin evidencia pública de agentes de IA generativa ya en producción dentro de Spendscape.** El roadmap de McKinsey menciona "gen AI-powered cost savings initiatives" como funcionalidad futura ("upcoming"), sin fecha de lanzamiento ni detalle arquitectónico. No está claro si a julio de 2026 esto ya se lanzó.

4. **No se encontró un "Lilli 2.0" o rebranding agéntico formal con nombre propio.** La evolución agéntica de McKinsey parece canalizarse principalmente a través de la marca QuantumBlack (Agentic AI Mesh, Agents at Scale) en lugar de una evolución nombrada de Lilli, aunque Lilli sí tiene en su roadmap "agentes para automatizar tareas".

5. **Detalle técnico limitado sobre el "motor de RFP" (RFP engine) mencionado como caso de uso de Lilli/QuantumBlack para clientes.** Es la mención más directa encontrada de aplicación de la arquitectura Lilli a sourcing/procurement, pero no hay artículo dedicado ni caso de estudio público con detalle de implementación.

6. **Artículo "Transforming procurement functions for an AI-driven world" no fue explorado en profundidad** (solo indexado vía cobertura de prensa secundaria) — recomendado para una pasada de seguimiento si se requiere más profundidad en esta área específica.

7. **No se confirmó la práctica formal "Product Development & Procurement" de McKinsey como marca/unidad de negocio específica en las fuentes revisadas.** Las búsquedas devolvieron principalmente el artículo "Redefining procurement performance in the era of agentic AI" (de la práctica de Operations, no necesariamente nombrada "Product Development & Procurement"). Es posible que esta nomenclatura de práctica no tenga presencia editorial pública separada, o que haya sido renombrada — brecha para verificar con el equipo o en fuentes adicionales (LinkedIn corporativo, páginas de careers de McKinsey).

8. **Discrepancia no resuelta entre la versión oficial y la versión de prensa de seguridad sobre el alcance del incidente de Lilli de marzo de 2026** (ver sección 1.1 y 4). No se pudo determinar con las fuentes disponibles cuál versión es más precisa — ambas coinciden en que hubo una vulnerabilidad real explotada por un tercero.

9. **Cifras de "25,000 agentes construidos" / "20,000 agentes operando junto a 40,000 consultores"** atribuidas al CEO de McKinsey no pudieron rastrearse hasta una fuente primaria directa (discurso, entrevista, o comunicado con fecha) — quedan marcadas como afirmación de vendor de baja confiabilidad hasta verificación adicional.

10. **No se encontraron cifras de adopción específicas para clientes de procurement usando agentes de McKinsey** (a diferencia de los 5 estudios de caso anónimos del artículo de febrero 2026) — no hay nombres de clientes reales, tasas de adopción sectorial, o cifras agregadas de despliegue específicas para la función de procurement en particular (más allá de los casos individuales ya documentados en sección 3.2).

11. **Herramientas propietarias de QuantumBlack (Iguazio, Turo, Optimus AI, AI4DQ, FUSE2, Data Fabricator) no tienen aplicación documentada específica a procurement** — parecen ser herramientas horizontales o de otras industrias (manufactura pesada, minería). No se profundizó en cada una individualmente por estar fuera del foco directo de procurement; documentado como posible pendiente si se requiere exhaustividad total.

---

## 6. Fuentes consultadas (bibliografía completa)

### Fuentes primarias (mckinsey.com, quantumblack, comunicados oficiales)

1. McKinsey & Company. (s.f.). *Rewiring the way McKinsey works with Lilli, our generative AI platform*. Consultado el 2026-07-01, de https://www.mckinsey.com/capabilities/tech-and-ai/how-we-help-clients/rewiring-the-way-mckinsey-works-with-lilli
2. McKinsey & Company. (s.f.). *Meet Lilli, our generative AI tool that's a researcher, a time saver, and an inspiration*. Consultado el 2026-07-01, de https://www.mckinsey.com/about-us/new-at-mckinsey-blog/meet-lilli-our-generative-ai-tool
3. McKinsey & Company. (2026-03-11). *Statement on Strengthening Safeguards Within the Lilli Tool*. Consultado el 2026-07-01, de https://www.mckinsey.com/about-us/media/statement-on-strengthening-safeguards-within-the-lilli-tool
4. McKinsey & Company. (2020). *Why we acquired a company that specializes in spend analytics*. Consultado el 2026-07-01, de https://www.mckinsey.com/about-us/new-at-mckinsey-blog/why-we-acquired-a-company-that-specializes-in-spend-analytics
5. McKinsey & Company. (2020). *A new approach to digital procurement—Orpheus, a McKinsey company*. Consultado el 2026-07-01, de https://www.mckinsey.com/capabilities/operations/our-insights/operations-blog/a-new-approach-to-digital-procurement-orpheus-by-mckinsey
6. McKinsey & Company. (s.f.). *Spendscape fifth anniversary*. Consultado el 2026-07-01, de https://www.mckinsey.com/capabilities/operations/tech-tools/spendscape-technology/our-updates/spendscape-fifth-anniversary
7. McKinsey & Company. (s.f.). *Spendscape - Spend Analytics Software*. Consultado el 2026-07-01, de https://www.mckinsey.com/capabilities/operations/tech-tools/spendscape-technology/spend-analytics-software
8. McKinsey & Company. (s.f.). *Procurement Savings Tracking Software | Spendscape by McKinsey*. Consultado el 2026-07-01, de https://www.mckinsey.com/capabilities/operations/tech-tools/spendscape-technology/our-offerings/savings-tracking-and-integrated-impact-management
9. McKinsey & Company. (s.f.). *Wave Program Management Software*. Consultado el 2026-07-01, de https://www.mckinsey.com/capabilities/transformation/how-we-help-clients/wave/overview
10. McKinsey & Company. (s.f.). *Procurement transformation program to reduce spend by $1 billion*. Consultado el 2026-07-01, de https://www.mckinsey.com/capabilities/transformation/how-we-help-clients/wave/our-impact/procurement-transformation-program-to-reduce-spend-by-1-billion
11. Mittal, A., Belotserkovskiy, R., & Liakopoulou, T. (2026-02-05). *Redefining procurement performance in the era of agentic AI*. McKinsey & Company. Consultado el 2026-07-01, de https://www.mckinsey.com/capabilities/operations/our-insights/redefining-procurement-performance-in-the-era-of-agentic-ai
12. McKinsey & Company. (s.f.). *Transforming procurement functions for an AI-driven world*. Consultado el 2026-07-01, de https://www.mckinsey.com/capabilities/operations/our-insights/transforming-procurement-functions-for-an-ai-driven-world (no explorado en profundidad — brecha documentada)
13. Sukharevsky, A., Kerr, D., Hjartar, K., Hämäläinen, L., Bout, S., & Di Leo, V., con Dagorret, G. (2025-06-13). *Seizing the agentic AI advantage*. McKinsey & Company / QuantumBlack. Consultado el 2026-07-01, de https://www.mckinsey.com/capabilities/quantumblack/our-insights/seizing-the-agentic-ai-advantage
14. Kerr, D., Gabrielli, D., Galeev, R., Kokaina, S., Cheung, C. W., Madden, C., & Stichbury, J. (2025-06-12). *How we enabled Agents at Scale in the Enterprise with the Agentic AI Mesh*. QuantumBlack, AI by McKinsey (Medium). Consultado el 2026-07-01, de https://medium.com/quantumblack/how-we-enabled-agents-at-scale-in-the-enterprise-with-the-agentic-ai-mesh-baf4290daf48
15. QuantumBlack, AI by McKinsey. (s.f.). *QuantumBlack Horizon: Unleashing the power of generative AI*. Medium. Consultado el 2026-07-01, de https://medium.com/quantumblack/quantumblack-horizon-unleashing-the-power-of-generative-ai-a3022597c642
16. QuantumBlack, AI by McKinsey. (s.f.). *Creating a future-proof enterprise agentic platform architecture*. Medium. Consultado el 2026-07-01, de https://medium.com/quantumblack/creating-a-future-proof-enterprise-agentic-platform-architecture-c21fc48406a5 (no explorado en profundidad — brecha documentada)
17. QuantumBlack, AI by McKinsey. (s.f.). *Evaluations for the agentic world*. Medium. Consultado el 2026-07-01, de https://medium.com/quantumblack/evaluations-for-the-agentic-world-c3c150f0dd5a (no explorado en profundidad — brecha documentada)
18. McKinsey & Company. (s.f.). *AI Agents at Scale: A data scientist's journey to transform clients with tech*. Consultado el 2026-07-01, de https://www.mckinsey.com/about-us/new-at-mckinsey-blog/ai-agents-at-scale-a-data-scientists-journey-to-transform-clients-with-tech
19. PR Newswire. (2026-04). *McKinsey and Google Cloud Launch the McKinsey Google Transformation Group to Scale Enterprise Impact for the AI era*. Consultado el 2026-07-01, de https://www.prnewswire.com/news-releases/mckinsey-and-google-cloud-launch-the-mckinsey-google-transformation-group-to-scale-enterprise-impact-for-the-ai-era-302749247.html
20. Opus by AppliedAI. (2026-05). *AppliedAI and McKinsey partner to deliver agentic AI to regulated enterprises*. Consultado el 2026-07-01, de https://www.opus.com/news/mckinsey-may-2026

### Fuentes secundarias / prensa especializada

21. CIO Dive. (2023). *McKinsey rolls out generative AI tool 'Lilli' to 7K employees*. Consultado el 2026-07-01, de https://www.ciodive.com/news/McKinsey-generative-AI-Lilli-platform-internal-employees/691231/
22. VentureBeat. (2023). *Consulting giant McKinsey unveils its own generative AI tool for employees: Lilli*. Consultado el 2026-07-01, de https://venturebeat.com/ai/consulting-giant-mckinsey-unveils-its-own-generative-ai-tool-for-employees-lilli
23. Consultancy.eu. (2020). *McKinsey buys Orpheus and launches Spend Intelligence offering*. Consultado el 2026-07-01, de https://www.consultancy.eu/news/3830/mckinsey-buys-orpheus-and-launches-spend-intelligence-offering
24. Carlsquare. (2020). *Carlsquare advised Orpheus GmbH on the sale to McKinsey*. Consultado el 2026-07-01, de https://carlsquare.com/deal-history/carlsquare-advised-spend-analytics-software-technology-company-orpheus-gmbh-on-the-sale-to-mckinsey/
25. Spend Matters. (s.f.). *Spendscape by McKinsey* (directorio de proveedores). Consultado el 2026-07-01, de https://spendmatters.com/vendor-directory/orpheus/
26. Procurement Magazine. (s.f.). *McKinsey: How Agentic AI is Shifting Procurement Capability*. Consultado el 2026-07-01, de https://procurementmag.com/news/mckinsey-agentic-ai-procurement-capability
27. Digital Commerce 360. (2025-11-11). *AI forces procurement to evolve — or be left behind*. Consultado el 2026-07-01, de https://www.digitalcommerce360.com/2025/11/11/ai-procurement-mckinsey-report/
28. AI Magazine. (s.f.). *QuantumBlack: A Global Force in Agentic AI Transformation*. Consultado el 2026-07-01, de https://aimagazine.com/news/quantumblack-a-global-force-in-agentic-ai-transformation

### Fuentes sobre el incidente de seguridad de Lilli (marzo 2026) — tratar con la debida cautela (ver sección 1.1)

29. 1Kosmos. (2026). *McKinsey Lilli Breach (2026): What It Reveals About Agent Authentication*. Consultado el 2026-07-01, de https://www.1kosmos.com/resources/blog/mckinsey-lilli-breach-agent-authentication
30. Outpost24. (2026). *How an AI Agent Hacked McKinsey's AI Platform*. Consultado el 2026-07-01, de https://outpost24.com/blog/ai-agent-hacked-mckinsey-ai-platform/
31. Treblle. (2026). *CodeWall hacked McKinsey's AI Platform Lilli Through Unprotected API Endpoints*. Consultado el 2026-07-01, de https://treblle.com/blog/codewall-hack-mckinsey-ai-platform-lilli
32. State of Surveillance. (2026). *An AI Agent Hacked McKinsey's AI Platform in Two Hours — Accessed 46 Million Messages*. Consultado el 2026-07-01, de https://stateofsurveillance.org/news/mckinsey-lilli-ai-agent-hack-codewall-sql-injection-2026/
33. Ikechukwu, D. (2026). *McKinsey Lilli AI Hack 2026: 5 Alarming Security Failures Every Enterprise Deploying AI Must Face Now*. Medium. Consultado el 2026-07-01, de https://medium.com/@creed_1732/mckinsey-lilli-ai-hack-2026-5-alarming-security-failures-every-enterprise-deploying-ai-must-face-2a9b66c2e3a3
34. BankInfoSecurity. (2026). *Autonomous Agent Hacked McKinsey's AI in 2 Hours*. Consultado el 2026-07-01, de https://www.bankinfosecurity.com/autonomous-agent-hacked-mckinseys-ai-in-2-hours-a-31007
35. NeuralTrust. (2026). *How an AI Agent Hacked McKinsey and Exposed 46 Million Messages*. Consultado el 2026-07-01, de https://neuraltrust.ai/blog/agent-hacked-mckinsey
36. PointGuard AI. (2026). *McKinsey AI platform breach exposes millions of messages*. Consultado el 2026-07-01, de https://www.pointguardai.com/ai-security-incidents/mckinsey-ai-chatbot-breach-exposes-millions-of-internal-messages

---

**Estado del documento:** Investigación sustancialmente completa para el alcance asignado (Lilli, QuantumBlack/Horizon/Agentic AI Mesh, Orpheus/Spendscape, Wave, anuncios oficiales). Brechas documentadas en sección 5 para posible profundización futura por el equipo.

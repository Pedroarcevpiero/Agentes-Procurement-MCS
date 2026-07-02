# Casos de uso, clientes y resultados de McKinsey en procurement agéntico

Investigación del AGENTE INVESTIGADOR 3. Ventana temporal objetivo: julio 2024 – julio 2026. Fecha de acceso de todas las fuentes: 2026-07-01, salvo que se indique otra cosa.

Leyenda:
- **[HECHO VERIFICADO]**: confirmado en fuente primaria consultada directamente (artículo de mckinsey.com leído vía fetch).
- **[AFIRMACIÓN DEL VENDOR]**: declarado por McKinsey/QuantumBlack (o cliente citado por McKinsey) sin verificación independiente. La inmensa mayoría de las cifras de este documento caen en esta categoría porque McKinsey no publica metodología de auditoría externa para sus estudios de caso.
- **[INFERENCIA]**: conclusión propia del agente investigador, no declarada explícitamente en la fuente.
- **[BRECHA]**: ausencia de información pública encontrada.
- **[FUERA DE VENTANA]**: fuente anterior a julio 2024, incluida solo como contexto histórico porque sigue siendo citada por McKinsey en 2025-2026.

---

## Resumen ejecutivo

McKinsey documenta el desplazamiento de "analytical AI" ("show me the data") a "agentic AI" ("do it for me") en procurement principalmente a través de tres artículos publicados entre jun 2025 y feb 2026 (Operations Practice y QuantumBlack). Se identificaron 13 casos de cliente/piloto (11 anónimos, 2 con nombre — Sanofi y Teva, ambos de jun 2024 y sin confirmación clara de uso de IA agéntica vs. analítica avanzada). El caso más rico en detalle operativo de "agentes" propiamente dichos es el de una empresa química (sourcing autónomo de consumibles: RFx, prequalificación de proveedores, análisis de bids, gestión de consultas — 20-30% eficiencia, 1-3% captura de valor) y el de un operador de telecomunicaciones (agentes de apoyo a negociación en tail spend de software — hasta 90% menos tiempo en análisis/correos, 10-15% ahorro). No se encontró ningún caso de "agente negociador" plenamente autónomo (todos son human-in-the-loop). La cifra agregada más citada es que la función de procurement podría ser "25 a 40 por ciento más eficiente" con agentic AI (proyección, no medición histórica). Se identificaron 10 brechas explícitas, siendo las más relevantes: ausencia de nombres de cliente en los casos agénticos más recientes, ausencia de auditoría externa de las cifras, y mezcla frecuente entre resultados de "IA agéntica" y resultados de transformación organizacional/analítica tradicional sin distinguir causalidad. Se descartaron explícitamente dos casos que aparecían en búsquedas (Pfizer con ORO Labs, Unilever Ice Cream) por NO ser atribuibles a McKinsey.

---

## 1. Fuentes primarias identificadas (mckinsey.com)

| # | Título | Fecha publicación | Autores | URL |
|---|--------|--------------------|---------|-----|
| A | Redefining procurement performance in the era of agentic AI | 5 feb 2026 | Aasheesh Mittal, Roman Belotserkovskiy, Theano Liakopoulou | https://www.mckinsey.com/capabilities/operations/our-insights/redefining-procurement-performance-in-the-era-of-agentic-ai |
| B | Transforming procurement functions for an AI-driven world | 27 oct 2025 | Jennifer Schmidt, Ryan Samuels, Samir Khushalani; con Casper Bek, Jaisheela Setty, Srinivas Reddy Mallavarapu | https://www.mckinsey.com/capabilities/operations/our-insights/transforming-procurement-functions-for-an-ai-driven-world |
| C | Seizing the agentic AI advantage (QuantumBlack) | 13 jun 2025 | Alexander Sukharevsky, Dave Kerr, Klemens Hjartar, Lari Hämäläinen, Stéphane Bout, Vito Di Leo | https://www.mckinsey.com/capabilities/quantumblack/our-insights/seizing-the-agentic-ai-advantage |
| D | Making the leap with generative AI in procurement (Operations Blog) | 20 mar 2024 [FUERA DE VENTANA, pero referenciado como antecedente] | Aasheesh Mittal, Jennifer Spaulding Schmidt | https://www.mckinsey.com/capabilities/operations/our-insights/operations-blog/making-the-leap-with-generative-ai-in-procurement |
| E | Contracting for performance: Unlocking additional value | ~2016-2018 [FUERA DE VENTANA — dato histórico aún citado] | McKinsey Operations | https://www.mckinsey.com/capabilities/operations/our-insights/contracting-for-performance-unlocking-additional-value |
| F | The state of AI in 2025 / State of AI: Global Survey 2025 (QuantumBlack) | 2025 | QuantumBlack, AI by McKinsey | https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai |
| G | Revolutionizing procurement: Leveraging data and AI for strategic advantage | 13 jun 2024 [FUERA DE VENTANA por ~2 semanas, incluido por su relevancia directa y por ser citado en reportes posteriores] | Aasheesh Mittal, Charles Cocoual, Mauro Erriquez, Theano Liakopoulou | https://www.mckinsey.com/capabilities/operations/our-insights/revolutionizing-procurement-leveraging-data-and-ai-for-strategic-advantage |

Prensa secundaria usada para triangular/confirmar (no primaria, pero cita McKinsey directamente):
- Digital Commerce 360, "AI forces procurement to evolve — or be left behind", 11 nov 2025, https://www.digitalcommerce360.com/2025/11/11/ai-procurement-mckinsey-report/ (resume el reporte B).
- Procurement Magazine, varias notas de reseña de los reportes A y B (procurementmag.com/news/mckinsey-agentic-ai-procurement-capability; mckinsey-transforming-procurement-for-an-ai-driven-world; mckinsey-ai-unlock-value-procurement).

**Nota metodológica importante**: los tres artículos principales (A, B, C) comparten y repiten varios de los mismos casos de cliente (química/sourcing autónomo, telco/negociación, farmacéutica/auditoría, OEM aeronáutico), lo que sugiere que McKinsey usa un pool limitado y recurrente de casos ilustrativos en su marketing de contenidos, no un catálogo amplio de despliegues verificables. Ningún caso incluye nombre de la empresa cliente (todos son anónimos: "a chemicals company", "a telco player", "an aircraft OEM", etc.), consistente con la práctica estándar de confidencialidad de McKinsey. Esto se documenta como brecha en la sección 5.

---

## 2. Casos de cliente / pilotos con agentes de IA en procurement

### 2.1 Empresa química — sourcing autónomo de consumibles [AFIRMACIÓN DEL VENDOR]
- **Fuente**: A, C (caso repetido en ambos artículos con cifras idénticas).
- **Sector**: Químico.
- **Alcance**: Categoría de consumibles (compra de cola/no estratégica).
- **Agentes construidos** (según fuente C, con más detalle operativo):
  - Agente que automatiza la preparación de tenders/RFx.
  - Agente que identifica y precalifica proveedores.
  - Agente que analiza ofertas competidoras (bid analysis).
  - Agente que enruta, rastrea y sintetiza consultas y clarificaciones de proveedores durante el proceso de sourcing.
- **Resultados citados**: incremento de eficiencia del personal de compras "20 to 30 percent"; mejora en captura de valor "1 to 3 percent".
- **Estado del piloto**: descrito como "early full-cycle pilot" (fuente B/prensa) — es decir, aún no confirmado como despliegue a escala completa ni multi-cliente.

### 2.2 Empresa de telecomunicaciones — negociación de precios en long-tail de software [AFIRMACIÓN DEL VENDOR]
- **Fuente**: A, C.
- **Sector**: Telecomunicaciones.
- **Alcance**: Negociación de precios en gasto de cola (long-tail) de productos de software especializado.
- **Agentes construidos**:
  - Preparación de "fact base" prenegociación (compilación automática de contexto de mercado, histórico e indicadores).
  - Sugerencias en tiempo real durante las negociaciones.
  - Evaluación de trade-offs entre costo, nivel de servicio y riesgo.
  - Generación automática de contraofertas a propuestas de proveedores.
- **Resultados citados**: reducción de tiempo dedicado a análisis y correos "up to 90 percent"; ahorro en negociaciones "10 to 15 percent" por proveedor.
- **Relación con hallazgo de tail spend**: coincide con la afirmación separada (fuente A) de que "companies deploying AI agents against long-tail spend categories are already seeing 10% to 15% savings", posiblemente el mismo dato generalizado a partir de este caso único.

### 2.3 Empresa tecnológica — spend analysis para BPO/contact center [AFIRMACIÓN DEL VENDOR]
- **Fuente**: A, C.
- **Sector**: Tecnología.
- **Agentes construidos**: dos agentes vinculados — (1) integra datos de gasto y de mercado para identificar tendencias de precios; (2) simula la evolución de la demanda bajo distintos escenarios de mercado.
- **Resultados citados**: identificación de oportunidades de ahorro de "12 to 20 percent" en operaciones de contact center, y "20 to 29 percent" en gasto de BPO (business process outsourcing) y servicios financieros. Estas son "oportunidades identificadas", no necesariamente ahorros ya capturados/realizados — distinción importante que McKinsey no siempre deja explícita.

### 2.4 Empresa farmacéutica global — auditoría/reconciliación factura-contrato [AFIRMACIÓN DEL VENDOR]
- **Fuente**: A, B, prensa (Digital Commerce 360).
- **Sector**: Farmacéutico.
- **Herramienta/agente**: herramienta de IA para reconciliación automática de facturas y órdenes de compra contra términos contractuales ("invoice-to-contract compliance").
- **Resultados citados**: en la versión de fuente A, reducción de "leakage" (pérdida de valor) del "4 percent". En la versión de fuente B/prensa, un proof-of-concept de 4 semanas identificó "más de $10 millones" en valor perdido no capturado ("missed value" / "value leakage") recuperable. Ambas cifras probablemente describen el mismo caso desde ángulos distintos (una en % de leakage evitado, otra en $ recuperado en el piloto), pero las fuentes no lo aclaran explícitamente — se marca como posible duplicado/mismo caso, no confirmado.

### 2.5 Fabricante de aeronaves (OEM aeronáutico) — automatización de ejecución de órdenes e inventario [AFIRMACIÓN DEL VENDOR]
- **Fuente**: A, WebSearch (Procurement Magazine).
- **Sector**: Aeroespacial/manufactura.
- **Agentes construidos**: agentes que automatizan la ejecución de órdenes y ajustan niveles de inventario en función de datos de planificación de producción.
- **Resultados citados**: reducción de inventario activo del "30 percent"; mejora de EBIT de "alrededor de $700 millones". Esta es, con diferencia, la cifra de mayor magnitud absoluta encontrada en toda la investigación — pero corresponde a inventory/supply chain más que a procurement puro (zona gris P2P/planning), y no se especifica qué parte del $700M es atribuible solo al componente de agentes de IA versus la transformación más amplia.

### 2.6 Fabricante de equipos de generación de energía (power-equipment OEM) — sourcing alineado con desarrollo de producto [AFIRMACIÓN DEL VENDOR — sin confirmar uso de agentes de IA generativa]
- **Fuente**: B.
- **Resultado**: reducción de costos del "11 percent" en 12 meses.
- **Nota**: este caso se presenta en el contexto de rediseño organizacional (creación de grupo de sourcing estratégico integrado con desarrollo de producto/ingeniería). El artículo NO especifica que se hayan usado agentes de IA generativa aquí — parece ser un caso de transformación organizacional "clásica" incluido en un artículo sobre IA, no necesariamente un caso de agentic AI. Se marca como posible caso no-agéntico colado en el reporte.

### 2.7 Empresa de químicos especializados — should-cost modeling vía COE [AFIRMACIÓN DEL VENDOR — sin confirmar agentes]
- **Fuente**: B, prensa.
- **Resultado**: ahorro del "13 percent" en gasto de materias primas, vía modelo de pricing liderado por un Centro de Excelencia (COE).
- **Nota**: igual que 2.6, no se confirma explícitamente el uso de agentic AI; podría ser analítica avanzada tradicional.

### 2.8 OEM industrial no identificado — elevación del COE a nivel ejecutivo [AFIRMACIÓN DEL VENDOR]
- **Fuente**: B.
- **Resultado**: "$370 millones" en ahorros de costos en el primer año, con "millones más" proyectados a futuro. Se atribuye a elevar el COE a nivel de CPO/ejecutivo, nuevo modelo de gobernanza, herramientas digitales y analytics — mezcla de cambio organizacional + herramientas digitales, no exclusivamente agentic AI.

### 2.9 Empresa de MRO (mantenimiento, reparación, operaciones) — e-sourcing [AFIRMACIÓN DEL VENDOR]
- **Fuente**: B.
- **Resultado**: reducción de costos del "20 percent" en una categoría compleja mediante soluciones de e-sourcing.

### 2.10 Empresa de seguros (global) — centro de excelencia con 10 nuevas competencias [AFIRMACIÓN DEL VENDOR]
- **Fuente**: B.
- **Resultado**: incremento del personal estratégico en un "20 percent"; duplicó el gasto bajo influencia de procurement.

### 2.11 Compañía de cruceros — reestructuración de función procurement [AFIRMACIÓN DEL VENDOR]
- **Fuente**: B.
- **Resultado**: mejoras en relaciones con proveedores y en entregas puntuales (on-time delivery); sin cifra numérica específica. Departamento de <100 personas.

### 2.12 Sanofi (farmacéutica) — should-cost modeling y negociación digital [AFIRMACIÓN DEL VENDOR — CASO CON NOMBRE PÚBLICO]
- **Fuente**: G.
- **Sector**: Farmacéutico.
- **Hallazgo importante**: este es el **único caso identificado en toda la investigación donde McKinsey nombra explícitamente al cliente** ("Sanofi"), a diferencia de los demás casos que son todos anónimos.
- **Qué se hizo**: aplicación de modelado "should-cost" para decisiones make-vs-buy en múltiples categorías; plataforma de análisis avanzado para evaluación de ofertas; negociaciones "digitally enabled".
- **Resultados citados**: reducción promedio del "10 percent" en gasto; reducción del tiempo de evaluación de ofertas en "dos tercios" (66%); incremento de ahorros logrados en negociación de "281 percent" (es decir, casi 4x más ahorro capturado vs. el proceso anterior).
- **Nota de rigor**: el artículo es de junio de 2024 (fuera de la ventana estricta de 24 meses, pero citado en el ecosistema de contenido 2024-2026 de McKinsey sobre procurement/IA) y describe herramientas de analítica avanzada/digitales — **no queda claro si involucra IA generativa o agéntica específicamente**, o si es analítica tradicional con IA aplicada de forma más genérica. Se marca como el caso con mayor cifra de mejora porcentual (281%) encontrado en la investigación, y por tanto merece escrutinio adicional si se usa como referencia.

### 2.13 Teva Pharmaceuticals — inteligencia de gasto y resiliencia de suministro [AFIRMACIÓN DEL VENDOR — CASO CON NOMBRE PÚBLICO]
- **Fuente**: G.
- **Sector**: Farmacéutico (genéricos).
- **Qué se hizo**: procurement impulsado por análisis con "spend intelligence"; sistemas automatizados para desarrollo de estrategias de categoría; unidad global con sede en Ámsterdam.
- **Resultados citados**: mejora de resiliencia de suministro "más de diez veces" (10x, sin unidad de medida clara — posible índice interno no explicado); reducción del tiempo de desarrollo de estrategias de categoría en "90 percent".
- **Mismo caveat que Sanofi**: fecha jun 2024, no se especifica si usa IA generativa/agéntica o analítica avanzada tradicional.

### Casos NO atribuibles a McKinsey encontrados durante la búsqueda (aclaración importante)
- **Pfizer**: se encontró un artículo de CPO Rising (15 dic 2025) sobre transformación de procurement con IA en Pfizer (agente de aprobación de requisiciones de 26 pasos, onboarding de proveedores automatizado, motor de workflow unificado). **[VERIFICADO: este caso NO involucra a McKinsey ni QuantumBlack]** — el socio tecnológico es **ORO Labs**, no McKinsey. Se documenta aquí solo para dejar constancia de que se investigó y se descartó como caso de McKinsey.
- **Unilever (Ice Cream)**: casos públicos de IA en la cadena de suministro de helados de Unilever (pronóstico de demanda con datos climáticos, 100,000 freezers conectados, mejoras de forecast del 10%, incrementos de ventas de 8-30% según país) son iniciativas propias de Unilever, **no atribuidas a McKinsey como consultor** en las fuentes revisadas. No se incluyen como caso de McKinsey.

### Caso hipotético / no real: orquestación de cadena de suministro (fuente C)
- **[INFERENCIA/ACLARACIÓN]**: el artículo "Seizing the agentic AI advantage" (QuantumBlack, jun 2025) incluye un ejemplo **explícitamente hipotético** ("could") de un agente orquestador autónomo de sourcing/almacenamiento/distribución que pronosticaría demanda, replanificaría inventario y transporte, y negociaría con sistemas externos. No es un caso de cliente real — es una viñeta ilustrativa de diseño. Los tres casos de estudio reales y concretos que sí trae ese artículo son de OTRAS funciones (banca legacy, investigación de mercado, memos de riesgo crediticio), no de procurement. Esto confirma que QuantumBlack aún no tiene casos reales publicados de agentes de supply-chain/procurement propios fuera de los que comparte con Operations Practice.

---

## 3. Métricas agregadas / estudios de valor de McKinsey (no atadas a un cliente específico)

| Métrica | Cifra | Fuente | Tipo |
|---|---|---|---|
| Eficiencia potencial de la función procurement con agentic AI | "25 a 40 por ciento más eficiente" | B únicamente — **CORREGIDO 2026-07-02**: verificado contra fuente primaria, NO aparece en A (ver sección 3.bis) | AFIRMACIÓN DEL VENDOR (proyección, no medición real) |
| Eficiencia de "autonomous category agents" | "15 to 30 percent efficiency improvements" (automatización de actividades sin valor añadido) | **NO VERIFICABLE — CORREGIDO 2026-07-02**: no se encontró verbatim en A, B ni C (ver sección 3.bis); posible atribución errónea de fuente terciaria | NO VERIFICABLE |
| Ahorro potencial vía P2P optimizado | "2 a 5 por ciento de reducción de costos" | B | AFIRMACIÓN DEL VENDOR |
| Ahorro potencial con advanced analytics | "20 por ciento de potencial de ahorros" | B | AFIRMACIÓN DEL VENDOR |
| Ahorro por gestión activa de tail spend (benchmark tradicional, sin IA) | "5% a 10%" vía consolidación de proveedores | A (vía WebSearch) | AFIRMACIÓN DEL VENDOR — benchmark histórico |
| Ahorro por gestión de tail spend CON agentes de IA | "10% a 15%" | A | AFIRMACIÓN DEL VENDOR — **CORREGIDO 2026-07-02**: verificado que NO es un agregado independiente, es la MISMA frase única del caso telco (2.2) citada dos veces en este documento (ver sección 3.bis) |
| Uso actual de datos disponibles por funciones de procurement | "menos del 20 por ciento" | A | AFIRMACIÓN DEL VENDOR |
| Spend gestionado por FTE de compras, comparado con hace 5 años | "50 por ciento más" actualmente | B | HECHO VERIFICADO (dato de encuesta propia, aunque autorreportado) |
| Correlación entre madurez de función y margen EBITDA | "cinco puntos porcentuales o más" en funciones maduras vs. inmaduras | B | AFIRMACIÓN DEL VENDOR (correlación, no causalidad declarada) |
| Erosión de valor por términos contractuales subóptimos y mala gestión de contratos | "9 por ciento de ingresos anuales" (~$2.5 billones para Global 500 de 2016) | E — **FUERA DE VENTANA (dato de ~2016)**, pero sigue siendo citado como contexto en artículos recientes sobre CLM agéntico | HECHO VERIFICADO como afirmación histórica de McKinsey, pero el dato en sí es de hace ~10 años, no de 2024-2026 |
| Presupuestos de procurement planos o en contracción | "55% de líderes de procurement" reportan presupuestos planos/decrecientes, mientras el 100% dice que sus metas de ahorro subieron | A (vía WebSearch) | HECHO VERIFICADO (encuesta propia McKinsey) — dato relevante de tensión estructural que motiva la adopción de IA |
| CPOs que ven la IA como fuerza disruptiva | "40 por ciento de líderes de procurement" | WebSearch (resumen de A) | AFIRMACIÓN DEL VENDOR |
| Organizaciones con gen AI implementado o piloteado | "40 por ciento" | B | HECHO VERIFICADO (encuesta propia) |
| Velocidad de escalado: prototipo → piloto | "semanas" | A/C | AFIRMACIÓN DEL VENDOR |
| Velocidad de escalado: piloto → escala completa | "menos de un año" | A/C | AFIRMACIÓN DEL VENDOR |

**Cifra de contexto histórico (fuera de ventana, no es de agentic AI)**: el reporte 2023 "The economic potential of generative AI" (McKinsey Digital/QuantumBlack) estimaba impacto económico agregado de gen AI, pero no es específico de procurement — se usa aquí solo si se referencia dentro de artículos 2024-2026; no se encontró una cita directa reciente que dimensione en $ el mercado de agentic AI en procurement específicamente. **[BRECHA]**.

---

## 3.bis Verificación de cifras contra fuente primaria (2026-07-02)

🟢 **HECHO VERIFICADO / metodología**: se releyeron vía WebFetch, palabra por palabra (búsqueda exhaustiva de las frases exactas en inglés), los tres artículos primarios de McKinsey citados como fuente de las cifras agregadas de la tabla de la sección 3: **A** = "Redefining procurement performance in the era of agentic AI" (mckinsey.com, Operations Practice, publicado **5-feb-2026**, autores Aasheesh Mittal, Roman Belotserkovskiy, Theano Liakopoulou); **B** = "Transforming procurement functions for an AI-driven world" (mckinsey.com, Operations Practice, publicado **27-oct-2025**, autores Jennifer Schmidt, Ryan Samuels, Samir Khushalani, con Casper Bek, Jaisheela Setty, Srinivas Reddy Mallavarapu); **C** = "Seizing the agentic AI advantage" (mckinsey.com/QuantumBlack, publicado 13-jun-2025). Acceso 2026-07-02 a las tres URLs listadas en la sección 1.

### (a) Redacción exacta de los agregados 15-30%, 25-40% y 75%

| Cifra buscada | ¿Aparece verbatim en A? | ¿Aparece verbatim en B? | ¿Aparece verbatim en C? | Cita textual encontrada y a qué corresponde |
|---|---|---|---|---|
| "25 to 40 percent" | **NO** — no se encontró en ninguna búsqueda de texto completo del artículo A | **SÍ**, dos veces | NO | En B: *"This shift could result in the procurement function being 25 to 40 percent more efficient, according to our analysis, while repurposing team activity from routine tasks to strategic decision making."* (traducción: "Este cambio podría hacer que la función de procurement sea 25 a 40 por ciento más eficiente, según nuestro análisis, a la vez que redistribuye la actividad del equipo de tareas rutinarias a decisiones estratégicas") — y de nuevo: *"Our analysis suggests that technology will reshape the procurement function into an organization that is 25 to 40 percent more efficient (Exhibit 5), more agile, and increasingly agentic."* (traducción: "Nuestro análisis sugiere que la tecnología reconfigurará la función de procurement en una organización 25 a 40 por ciento más eficiente, más ágil y crecientemente agéntica"). **Métrica**: eficiencia agregada de TODA la función de procurement, proyección prospectiva ("could result", "suggests"), no una medición histórica real. |
| "15 to 30 percent" ("autonomous category agents") | **NO** | **NO** | **NO** | No se encontró esta frase textual en ninguno de los tres artículos primarios revisados. Es probable que provenga de una fuente secundaria (blogs de terceros como paperclipped.de, webpronews.com) que reformuló o combinó cifras de McKinsey (p. ej. confundiéndola con el "20 to 30 percent" de eficiencia del caso químico de la sección 2.1, o con el "20 to 30 percent" citado en un reporte distinto de McKinsey sobre infraestructura de TI/service desk, dominio no relacionado con procurement). **Conclusión: NO VERIFICABLE contra fuente primaria de procurement — se recomienda retirar la atribución a McKinsey o marcarla explícitamente como cifra de fuente terciaria no confirmada.** |
| "75 percent" (reducción en tiempo de preparación de RFP) | **NO** | **NO** (B solo contiene la frase no relacionada "more than three-quarters of consumer and advanced-industry companies have done so", sobre separar procurement estratégico de transaccional, sin relación con RFP) | **NO** | No se encontró esta cifra en ningún artículo primario de McKinsey sobre procurement agéntico. Las búsquedas web sitúan un "75%" de borradores de RFP listos ("75% ready drafts") en contenido de terceros no atribuido claramente a McKinsey (aparenta ser marketing de un vendor de herramientas RFP). **Conclusión: NO VERIFICABLE — no hay evidencia de que McKinsey haya publicado esta cifra en el contexto de procurement agéntico; probable atribución errónea de una fuente secundaria.** |

### (b) El dato de ahorro "10-15%": ¿caso específico, benchmark agregado, o ambos?

🟢 **HECHO VERIFICADO**: la frase exacta **"10 to 15 percent"** aparece **una única vez** en el corpus de los tres artículos primarios (A, B, C) — en el artículo A, exclusivamente dentro del caso del operador de telecomunicaciones (sección 2.2 de este documento): *"In use, the AI system cut the time negotiating teams needed to spend on analysis and emails by up to 90 percent. The AI-guided negotiations led to 10 to 15 percent savings across vendors."* (traducción: "En uso, el sistema de IA redujo el tiempo que los equipos de negociación necesitaban dedicar a análisis y correos en hasta un 90 por ciento. Las negociaciones guiadas por IA generaron ahorros del 10 al 15 por ciento entre proveedores"). No se encontró una repetición independiente de "10 to 15 percent" como benchmark agregado de tail spend en ninguno de los tres artículos.

**Conclusión sobre reciclaje**: la fila 143 de la tabla de la sección 3 de este mismo documento ("Ahorro por gestión de tail spend CON agentes de IA... Fuente A") **describe la MISMA frase única del caso telco (sección 2.2) como si fuera además un benchmark agregado independiente** — es decir, dentro de nuestro propio corpus se está citando un único dato primario dos veces bajo dos encabezados distintos (caso específico + "benchmark agregado"), lo cual sobrerrepresenta la evidencia disponible. **No es que McKinsey haya reciclado el dato entre dos publicaciones distintas — es una sola mención en un solo artículo, ligada inequívocamente al caso telco, y nuestra propia tabla la duplicó como si tuviera dos fuentes de respaldo independientes.** Se recomienda, para el informe final, tratar "10 a 15 por ciento" como una única observación de un solo caso anónimo (telco, tail spend de software), no como un benchmark validado de forma independiente. Nótese además (dato de contexto, no de agentic AI) que McKinsey sí tiene, en otro artículo más antiguo y no agéntico ("Long tail, big savings: Digital unlocks hidden value in procurement", fuera de la ventana temporal de este corpus), un rango similar de "10-15%" para ahorro de tail spend vía digitalización general — coincidencia de rango numérico entre dos generaciones de contenido de McKinsey sobre tail spend, pero no la misma cita ni el mismo mecanismo (digitalización general vs. agentes de IA).

### Conclusión general de la verificación

De las cuatro cifras "insignia" atribuidas a McKinsey en el corpus (15-30%, 25-40%, 75%, 10-15%), **solo dos están confirmadas verbatim contra fuente primaria**: 25-40% (artículo B, no A) y 10-15% (artículo A, telco, dato único no un agregado). Las otras dos (15-30% de "autonomous category agents" y 75% de reducción de RFP) **no se encontraron en ningún artículo primario de McKinsey sobre procurement agéntico** y deben tratarse como NO VERIFICABLES / posible atribución errónea de fuentes secundarias hasta nueva evidencia.

---

## 4. Mapa de subprocesos de procurement cubiertos por iniciativas de McKinsey con IA/agentes

| Subproceso | ¿Qué ha propuesto o mostrado McKinsey? | Evidencia de caso real vs. solo conceptual | Fuente |
|---|---|---|---|
| **Spend analysis** | Agentes que integran datos de gasto/mercado y detectan tendencias de precio; "category copilots" | Caso real (empresa tecnológica, sección 2.3) | A, C |
| **Sourcing estratégico / eRFX** | Agentes de generación de RFx, prequalificación de proveedores, análisis de bids; motor de RFP entrenado con >10,000 RFPs históricos (caso 2024, fuera de ventana) | Caso real (química, sección 2.1); precedente 2024 (fuente D) | A, C, D |
| **Negociación** | Sí — McKinsey describe explícitamente "agentes negociadores": preparan fact base, sugieren tácticas en tiempo real, evalúan trade-offs, generan contraofertas automáticamente | Caso real (telco, sección 2.2) — es el caso más concreto de "agente negociador autónomo" encontrado en toda la investigación | A, C |
| **Gestión de contratos (CLM)** | "Contract optimization" listado como categoría de solución agéntica ya disponible ("agentic AI solutions are already available to use... contract optimisation"); reconciliación automática factura-contrato | Caso real de reconciliación factura-contrato (farmacéutica, 2.4); "contract optimization" mencionado solo como categoría, sin caso propio detallado | A |
| **Gestión de categorías** | "Category copilots"; agentes de categoría autónomos con 15-30% de mejora de eficiencia (cifra agregada, no caso único); should-cost modeling y make-vs-buy (Sanofi, 2.12) | Caso químico (consumibles, 2.1) para agentes; caso Sanofi (2.12) para analítica de categoría con nombre público, aunque de tecnología menos claramente "agéntica" | A, G |
| **Riesgo y desempeño de proveedores** | Mencionado como uno de los 5 dominios de agentes ("performance & risk management"); seguimiento de desempeño de entrega y cumplimiento (farmacéutica, 2.4) | Parcialmente cubierto por el caso farmacéutico; sin caso dedicado solo a riesgo de proveedores (p.ej. riesgo financiero/geopolítico de terceros) | A |
| **Procure-to-pay (P2P)** | Automatización de ejecución de órdenes e inventario (aeroespacial, 2.5); ahorro potencial de 2-5% vía P2P optimizado (cifra agregada) | Caso real (aeroespacial) aunque es más supply-chain/inventory que P2P puro | A, B |
| **Tail spend / compras de cola** | Negociación agéntica de long-tail (telco, 2.2); "automated tail-spend repricing" listado como solución ya disponible | Caso real (telco); "repricing systems" mencionados solo como categoría sin caso propio | A |
| **ESG / sostenibilidad de proveedores** | Listado como subproceso en la encuesta de madurez (fuente B) | Solo mencionado en tabla de benchmarking, sin caso ni agente descrito | B |

---

## 5. Encuestas y estudios de McKinsey sobre adopción de agentic AI en compras

### 5.1 "Procurement Organization of the Future" (encuesta base del reporte B)
- **[HECHO VERIFICADO]** Muestra: más de 300 líderes de procurement encuestados.
- Sectores cubiertos: industrias avanzadas, consumo, finanzas/seguros, ciencias de la vida, energía/materiales, tecnología/telecom/media, viajes/logística/infraestructura.
- Rango de gasto gestionado por los encuestados: $100 millones a $100 mil millones.
- Tamaño de equipos: 25 a 500 empleados.
- Fecha de campo/encuesta no especificada con exactitud más allá de que el reporte que la usa se publicó el 27 oct 2025 — **[BRECHA]**: no se encontró la fecha exacta de aplicación de la encuesta ni el link al informe completo de la encuesta en sí (parece integrada dentro del artículo, no publicada como documento standalone descargable).
- Hallazgos clave: dos tercios de los CPOs reportan a CEO/CFO; dos tercios de las organizaciones segregan procurement estratégico de transaccional; más de la mitad tiene un COE dedicado; 60% de las grandes organizaciones (vs. 30% de las pequeñas) tiene sistema P2P; solo un tercio usa e-sourcing; 40% ha implementado o piloteado gen AI; 55% reporta presupuestos planos o decrecientes pese a que el 100% dice que sus metas de ahorro subieron.

### 5.2 McKinsey Global Procurement Excellence (GPE 360)
- **[HECHO VERIFICADO]** Benchmark de madurez de la función de procurement con datos históricos 2005-2023 (20 años). Usado como base comparativa en el reporte B, pero no es un estudio nuevo de agentic AI en sí — es la base de benchmarking de largo plazo de McKinsey en procurement.

### 5.3 "The State of AI" (QuantumBlack) — encuesta global anual
- **[HECHO VERIFICADO — existencia confirmada]** McKinsey/QuantumBlack publica una encuesta global anual "The State of AI" (edición 2025 confirmada: "The state of AI in 2025: Agents, innovation, and transformation"; hay referencias también a una edición orientada a 2026 sobre "State of AI trust"). Esta encuesta es transversal a toda la empresa (no específica de procurement), por lo que sus datos de adopción de agentic AI son a nivel corporativo general, no desglosados por función de compras en los extractos que pudimos confirmar.
- **[BRECHA]**: no se confirmó un desglose específico por función "procurement" dentro de la encuesta "State of AI" — los artículos específicos de procurement (A y B) citan sus propias encuestas de función (300+ líderes de procurement), no la encuesta State of AI corporativa. No profundizamos más en el contenido completo de "State of AI" 2025/2026 porque queda fuera del alcance estricto de "procurement"; se delega esa lectura completa a otros agentes del equipo si cubren adopción corporate-wide de agentic AI.

### 5.4 CPO Executive Forum de McKinsey
- **[AFIRMACIÓN DEL VENDOR, sin detalle cuantitativo]** Se menciona que en un reciente "CPO Executive Forum" de McKinsey, los líderes de procurement identificaron como prioridades: estrés organizacional y talento, nuevas capacidades/tareas requeridas por la función, y aceleración de la habilitación digital. No se encontró fecha exacta del foro, número de asistentes, ni reporte formal publicado de sus resultados. **[BRECHA]**.

---

## 6. Brechas explícitas identificadas

1. **Casi todos los casos de cliente son anónimos; las excepciones nombradas (Sanofi, Teva) no confirman uso de agentic AI específicamente.** De los 13 casos identificados, solo 2 (Sanofi y Teva, sección 2.12-2.13, fuente de jun 2024) nombran al cliente explícitamente, y ambos describen analítica avanzada/digital más que agentes de IA generativa claramente diferenciados. Todos los casos de 2025-2026 con vínculo más claro a "agentic AI" (química, telco, farmacéutica-auditoría, tecnología, aeroespacial) permanecen anónimos ("a chemicals company", "a telco player", etc.). Esto es consistente con la práctica estándar de confidencialidad de McKinsey, pero es una limitación real para verificar independientemente los resultados, a diferencia de proveedores de software (SAP Ariba, Coupa, Jaggaer, Ivalua) que sí suelen nombrar clientes en sus propios materiales de marketing.
2. **No hay evidencia de "agentes negociadores" completamente autónomos que cierren tratos sin supervisión humana.** El único caso descrito (telco, sección 2.2) mantiene al agente en rol de "apoyo/copiloto" (prepara fact base, sugiere, genera borradores de contraoferta) — no se documenta un caso donde el agente negocie y cierre un contrato de forma autónoma sin intervención humana final.
3. **No hay métricas de auditoría externa/tercero independiente.** Todas las cifras (11%, 13%, 20-30%, $370M, $700M, etc.) provienen de McKinsey citando a sus propios clientes de forma anónima, sin metodología de cálculo publicada, sin período de medición estandarizado, y sin verificación por auditor externo. Deben tratarse como afirmaciones de mercadeo/thought leadership, no como estudios controlados.
4. **Ambigüedad entre "agentic AI" real y transformación organizacional/analítica tradicional.** Varios casos citados en el reporte B (power-equipment OEM 11%, químicos especializados 13%, OEM industrial $370M) **no especifican** que se haya usado IA generativa o agéntica — parecen ser casos clásicos de excelencia en procurement (COE, should-cost modeling, e-sourcing) incluidos en un artículo sobre IA sin dejar claro el rol específico de agentes de IA en el resultado. Esto es una señal de que McKinsey mezcla su portafolio histórico de casos de "procurement excellence" con la narrativa nueva de "agentic AI" sin distinguir siempre con precisión cuál tecnología produjo cuál resultado.
5. **No se encontró desglose de costos de implementación, tiempo total de despliegue (más allá de "semanas a piloto, <1 año a escala" genérico), ni tasas de fracaso/abandono de pilotos.** McKinsey no publica cifras de proyectos agénticos de procurement que hayan fallado o no hayan escalado — solo casos de éxito, lo cual es un sesgo de supervivencia esperable en contenido de marketing.
6. **No hay casos públicos de agentes en gestión de riesgo de proveedores (financiero/geopolítico/ESG) como categoría dedicada.** El único acercamiento a "riesgo" es cumplimiento de contrato/factura (farmacéutica), no riesgo de continuidad de suministro, riesgo financiero de terceros o riesgo ESG con agentes dedicados.
7. **No se encontró un caso público de McKinsey sobre agentes en gestión de categorías indirectas complejas** (marketing, servicios profesionales, capex) más allá de las menciones genéricas de "category copilots".
8. **No se identificó la fecha exacta ni el informe completo descargable de la encuesta "Procurement Organization of the Future"** (>300 líderes) — solo se conoce a través de su cita dentro del artículo B.
9. **No se profundizó en cifras específicas de adopción de agentic AI (vs. gen AI genérico) desglosadas por función procurement dentro del "State of AI" survey global de QuantumBlack** — posible tarea pendiente si otro agente del equipo cubre ese informe en detalle.
10. **Superposición y posible reciclaje de cifras entre reportes.** El rango "10-15% de ahorro" aparece tanto como resultado específico del caso telco (2.2) como benchmark agregado de "tail spend con agentes de IA" en el reporte A — no queda claro si es el mismo dato reportado dos veces o dos mediciones independientes que coinciden.

---

## 7. Conclusiones para diseño de sistemas propios (uso interno del equipo)

- **[INFERENCIA]** El patrón de agentes que McKinsey describe con más detalle operativo (y por tanto el más replicable) es el de **sourcing autónomo por categoría** (caso 2.1): un pipeline de agentes especializados y encadenados — (a) generación de RFx, (b) descubrimiento/precalificación de proveedores, (c) análisis comparativo de ofertas, (d) gestión de comunicación con proveedores — aplicado primero a categorías de bajo riesgo/alto volumen (consumibles, tail spend) antes que a categorías estratégicas.
- **[INFERENCIA]** El caso de **negociación asistida** (2.2) es el más cercano a un "agente negociador", pero deja claro que el diseño de McKinsey es human-in-the-loop: el agente prepara, sugiere y redacta, pero no decide ni firma. Esto es relevante como patrón de diseño defendible (menor riesgo legal/reputacional) frente a un agente 100% autónomo en negociación.
- **[INFERENCIA]** McKinsey enmarca la secuencia de adopción recomendada como: (1) construir una "data spine" (base de datos limpia y unificada), (2) activar "no-regret agents" en sourcing, negociación y preservación de valor, (3) rediseñar roles/procesos para convivencia humano-agente. Esta secuencia (dato → agentes de bajo riesgo → rediseño organizacional) es un patrón de implementación citado explícitamente en la fuente A/C y puede servir de marco de referencia para nuestra propia hoja de ruta.

---

*Fin del documento — última actualización: 2026-07-01. Todas las URLs fueron accedidas ese mismo día.*

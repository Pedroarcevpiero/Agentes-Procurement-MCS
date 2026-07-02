# Resumen — Agente Investigador 1: Productos y Plataformas Agénticas de McKinsey para Procurement

Archivo completo de hallazgos: `research/hallazgos/01-productos-plataformas.md`

## Hallazgos clave (1 línea c/u)

- Lilli (jul. 2023) es el asistente interno de IA de McKinsey, arquitectura RAG sobre >100,000 documentos, con pestañas "GenAI Chat" y "Client Capabilities"; 72% de adopción interna, 500K+ prompts/mes (fuente primaria McKinsey).
- McKinsey no ha revelado públicamente qué LLM(s) alimenta(n) Lilli — brecha confirmada, ni siquiera el comunicado oficial post-incidente lo aclara.
- Roadmap declarado de Lilli incluye "agentes para automatizar tareas" y expansión de generación de slides, pero sin fecha de lanzamiento ni rebranding formal tipo "Lilli 2.0".
- Caso de uso más directo de Lilli/QuantumBlack para procurement: un "motor de RFP" (RFP engine) para clientes — mencionado pero sin detalle técnico público.
- Incidente de seguridad de Lilli (marzo 2026): CodeWall (firma de seguridad) explotó una vulnerabilidad; McKinsey confirmó oficialmente el hecho (11-mar-2026) pero niega acceso a datos de clientes, mientras blogs de seguridad reportan acceso masivo (46M mensajes) vía inyección SQL — lección de guardrails clave para diseño propio.
- QuantumBlack Horizon (jun. 2023) es la suite de IA productiva de McKinsey (AI4DQ, FUSE2, Data Fabricator); da paso a "Agents at Scale", la "fábrica de agentes" de QuantumBlack.
- Arquitectura de referencia **Agentic AI Mesh** (QuantumBlack, jun. 2025, autor Dave Kerr et al.) es el hallazgo técnico más accionable: 5 principios de diseño, 7 capacidades (registry, observabilidad, auth, evaluaciones, etc.), soporta LangGraph/CrewAI/Autogen/Google ADK, estándares MCP y A2A, OAuth2/JWT.
- Reporte "Seizing the agentic AI advantage" (QuantumBlack, jun. 2025) nombra modelos LLM concretos por caso de uso (Mistral Small, Llama 3 8B, Gemini Nano, Claude Haiku) y describe shift de software empresarial hacia "agent-native" (Microsoft Copilot Studio, Salesforce Agentforce, SAP BTP+Joule).
- Orpheus GmbH (adquirida feb. 2020) fue rebrandeada en 2023 a **Spendscape by McKinsey** — plataforma de spend analytics sobre SAP BTP, con roadmap declarado (no confirmado en producción) de "gen AI-powered cost savings initiatives" y módulos de "negotiation excellence".
- Spendscape integra savings-tracking con **Wave by McKinsey**, plataforma de gestión de transformación que ya usa "agentes de IA personalizados" (custom AI agents) para planeación y predicción de riesgos — 340,000+ iniciativas rastreadas, $200B+ en spend gestionado (cifras a verificar, posible bug de renderizado en la página fuente).
- Artículo central de procurement agéntico: "Redefining procurement performance in the era of agentic AI" (Mittal, Belotserkovskiy, Liakopoulou; McKinsey, 5-feb-2026) — define "procurement agents", da 5 estudios de caso cuantificados (tech co., química, telco, farma, OEM aeronáutico) con cifras de eficiencia 12-90% según caso, y un marco de implementación de 4 pilares + roadmap de 6 pasos.
- Cifras agregadas de McKinsey: IA agéntica puede hacer a procurement 25-40% más eficiente en general; agentes autónomos de categoría específicamente dan 15-30% de eficiencia.
- Alianzas estratégicas 2026 relevantes al ecosistema agéntico: McKinsey Google Transformation Group (abr. 2026, con Google Cloud) y alianza con AppliedAI/Opus (may. 2026) para industrias reguladas — ninguna menciona procurement explícitamente como foco.
- No se confirmó la existencia de una práctica/marca formal "Product Development & Procurement" con presencia editorial propia; las publicaciones de McKinsey sobre agentic AI en procurement están bajo la práctica de "Operations".

## Brechas identificadas (ver sección 5 del archivo de hallazgos para detalle completo)

- Proveedor(es) de LLM detrás de Lilli: no revelado.
- Integración real entre Spendscape y Agentic AI Mesh/Lilli: no documentada públicamente (probable pero no confirmada).
- Estado de producción de "gen AI-powered cost savings" en Spendscape: solo roadmap, sin confirmación de lanzamiento.
- Detalle técnico del "motor de RFP" de Lilli/QuantumBlack para procurement: no publicado.
- Artículos "Transforming procurement functions for an AI-driven world" y "Creating a future-proof enterprise agentic platform architecture" no explorados en profundidad — candidatos para pasada de seguimiento.
- Cifras del CEO de McKinsey ("25,000 agentes construidos", "20,000 agentes junto a 40,000 consultores"): no rastreadas a fuente primaria directa, tratar con cautela.
- Discrepancia no resuelta entre versión oficial y versión de prensa de seguridad sobre alcance del incidente Lilli marzo 2026.
- Sin cifras de adopción de clientes reales (con nombre) usando agentes de procurement de McKinsey.
- Herramientas propietarias de QuantumBlack (Iguazio, Turo, Optimus AI) no tienen aplicación documentada a procurement — parecen horizontales/de otras industrias.

# backend/prompts.py
"""
Prompts centralizados para el agente.
Contiene el prompt del router de intención y
algunas instrucciones para SQL y web search.
"""

DB_SCHEMA_DESCRIPTION = """
Tienes acceso de solo lectura a una base de datos SQLite con estas tablas:

Tabla tickets:
- folio_ticket INTEGER
- fecha_registro TEXT
- estatus_ticket TEXT (valores "EN PROCESO", "ATENDIDO")
- tiempo_solucion_total REAL
- efectividad_ticket REAL
- colaborador_asignado TEXT
- departamento_asignado TEXT
- fecha_cierre TEXT
- servicio TEXT
- personal_reporta TEXT
- departamento_reporta TEXT
- unidad_negocio TEXT
- empresa TEXT
- ubicación TEXT
- sucursal TEXT
- motivo_ticket TEXT
- personal_registra_ticket TEXT

Tabla asignaciones:
- folio_ticket INTEGER
- colaborador_asignado TEXT
- departamento_asigando TEXT
- inicio_asignacion TEXT
- fin_asignacion TEXT
- estatus_asigancion TEXT
- servicio_asignacion TEXT
- tiempo_atencion_asignacion TEXT
- sla_asignacion REAL
- efectividad_asignacion REAL
- estatus_ticket TEXT
"""

ROUTER_SYSTEM_PROMPT = f"""
Eres un router de intención para un agente.

Tu tarea es analizar el mensaje del usuario y decidir cuál de estas intenciones usar:

1) "sql": cuando el usuario haga preguntas sobre datos que parecen estar
   en las tablas "tickets" o "asignaciones". Ejemplos:
   - estadísticas de tickets
   - promedios, conteos, por colaborador, departamentos, etc.

2) "web": cuando el usuario pida información actual o de internet, por ejemplo:
   - noticias, información reciente
   - datos que no están en la base local

3) "llm": cuando el usuario solo quiera una explicación, opinión, resumen,
   o algo que pueda responderse con tu conocimiento general sin usar la base
   de datos ni internet.

Además:
- Si la intención es "sql", debes generar un query SQL de SOLO LECTURA
  (solo SELECT) para la base de datos con este esquema:
{DB_SCHEMA_DESCRIPTION}

- Si la intención es "web", debes generar un texto corto de búsqueda en inglés
  o español que sirva como query para un motor de búsqueda web.

Responde SIEMPRE en JSON con esta estructura EXACTA:

{{
  "intent": "sql" | "web" | "llm",
  "sql_query": "<query o vacío>",
  "web_query": "<query o vacío>",
  "explanation": "<breve explicación de por qué elegiste esa intención>"
}}
"""

LLM_ANSWER_SYSTEM_PROMPT_SQL = f"""
Eres un asistente útil y claro. Responde en español, de forma concisa y didáctica.
Analiza la pregunta del usuario en conjunto con el contexto siguiente:

Se ejecutó este query SQL:
{{sql_query}}

Y este fue el resultado (JSON):
{{sql_result}}

Explica el resultado al usuario en español de forma clara.
"""

LLM_ANSWER_SYSTEM_PROMPT_WEB = f"""
Eres un asistente útil y claro. Responde en español, de forma concisa y didáctica.
Analiza la pregunta del usuario en conjunto con el contexto siguiente:

Se realizó esta búsqueda web:
{{web_query}}

Y este fueron los resultados de la búsqueda en internet:
{{web_result}}

Responde al usuario en español usando esta información.
"""
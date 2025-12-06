# Agente LLM para Ticketing

Un agente inteligente que combina **consultas SQL**, **búsqueda web** y
**razonamiento natural** usando un **modelo LLM local o remoto** con API
tipo OpenAI.

## Estructura del proyecto

    agent_project/
    │
    ├── backend/
    │   ├── main.py
    │   ├── router.py
    │   ├── llm_client.py
    │   ├── db_client.py
    │   ├── web_search.py
    │   ├── prompts.py
    │   └── config.py
    │
    ├── frontend/
    │   └── app.py
    │
    ├── tickets.db
    ├── requirements.txt
    └── README.md

## Instalación

### 1. Crear entorno virtual

``` bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate    # Windows
```

### 2. Instalar dependencias

``` bash
pip install -r requirements.txt
```

### 3. Configurar .env

    LLM_PROVIDER="local"  # "openai" | "gemini" | "local" | "lmstudio"

    LLM_API_BASE=http://localhost:8001/v1
    LLM_MODEL=model_name

    LLM_API_KEY=""
    OPENAI_API_KEY=""
    GEMINI_API_KEY=""

    TAVILY_API_KEY=""

    DB_PATH=./tickets.db

### 4. Levantar backend

``` bash
uvicorn backend.main:app --reload --port 8000
```

### 5. Levantar frontend

``` bash
streamlit run frontend/app.py
```

### 6. 🧠 Cómo funciona el agente internamente

1. User → mensaje textual
2. FastAPI → Router decide intención via LLM
3. Según la intención:
   - **sql** → genera SQL, ejecuta, resume resultados
   - **web** → busca info con Tavily, resume, devuelve fuentes
   - **llm** → respuesta directa del modelo
4. Devue lve JSON a Streamlit
5. Streamlit muestra la respuesta y renderiza tablas o fuentes


## Ejemplos de uso

### Consulta SQL

> "Muéstrame los tickets abiertos."

### Web search

> "¿Cuáles son los trending topics?"

### Respuesta LLM

> "Explica qué es un SLA."

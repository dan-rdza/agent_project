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

    LLM_API_URL=http://localhost:1234/v1/chat/completions
    LLM_MODEL=llama-3.2-8b-instruct
    TAVILY_API_KEY=TU_API_KEY
    DB_PATH=./tickets.db

### 4. Levantar backend

``` bash
uvicorn backend.main:app --reload --port 8000
```

### 5. Levantar frontend

``` bash
streamlit run frontend/app.py
```

## Ejemplos de uso

### Consulta SQL

> "Muéstrame los tickets abiertos."

### Web search

> "¿Cuáles son los trending topics?"

### Respuesta LLM

> "Explica qué es un SLA."

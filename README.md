# Agente LLM con Conexión a SQLite

Este proyecto consiste en un agente inteligente que combina **consultas SQL**, **búsqueda web** y
**razonamiento natural** usando un **modelo LLM local o remoto** con API tipo OpenAI.

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
    ├── database.db (SQLite)
    ├── requirements.txt
    └── README.md

## Instalación

### 1. Crear entorno virtual

Este proyecto se creo sobre un entorno virtual con python 3.10
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

    DB_PATH=./database.db

### 4. Levantar backend

Se levanta un servicio FastAPI
``` bash
uvicorn backend.main:app --reload --port 8000
```

### 5. Levantar frontend

Se levanta un frontend con el framework Streamlit
``` bash
streamlit run frontend/app.py
```

### 6. 🧠 Cómo funciona el agente

1. User → mensaje textual
2. FastAPI → Router decide intención via LLM
3. Según la intención:
   - **sql** → genera SQL, ejecuta, resume resultados
   - **web** → busca info con Tavily, resume, devuelve fuentes
   - **llm** → respuesta directa del modelo
4. Devue lve JSON a Streamlit
5. Streamlit muestra la respuesta y renderiza tablas o fuentes


### 7. Ejemplos de uso

#### Consulta SQL

> "Dame un top de los datos de la tabla <tabla> por fecha"
> "Cuáles son los detalles del campo <campo> de la tabla <tabla>"

#### Web search

> "¿Cuáles son los trending topics?"
> "¿Cuál es la noticia más reciente de la ciudad de méxico?"
> "Dime el pronostico del tiempo de Quintana Roo"

#### Respuesta LLM

> "Explica qué es un SLA."
> "¿Qué es la IA?"


### 8. Pasos Siguientes
> Integraciones con bases vectoriales
> Integración de memoria contextual para mantener un chat conversacional
> Integración con servicio de embeddings para busquedas en bases de conocimientos
> Integraciones con servicios de otras APIs, ejecución de tareas.



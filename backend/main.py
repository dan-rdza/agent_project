# backend/main.py
"""
API principal del agente usando FastAPI.
"""

from typing import List, Dict, Any, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .router import AgentRouter

app = FastAPI(title="Agente LLM")

# CORS para permitir que Streamlit (otro puerto) consuma esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # para educación; en producción ser más estricto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = AgentRouter()


class ChatRequest(BaseModel):
    message: str


class SQLResult(BaseModel):
    columns: list[str] = []
    rows: list[Any] = []
    error: Optional[str] = None


class ChatResponse(BaseModel):
    intent: str
    reply: str
    sql_query: Optional[str] = None
    sql_result: Optional[SQLResult] = None
    web_query: Optional[str] = None
    web_raw_result: Optional[List[Dict[str, str]]] = None


@app.post("/agent", response_model=ChatResponse)
def agent_endpoint(req: ChatRequest):
    """
    Endpoint principal: recibe un mensaje del usuario
    y devuelve la respuesta del agente.
    """
    result = router.route(req.message)

    # Normalizamos el sql_result para ajustarlo al modelo Pydantic
    sql_res = result.get("sql_result")
    if sql_res is not None and not isinstance(sql_res, dict):
        sql_res = None

    return ChatResponse(
        intent=result.get("intent", "llm"),
        reply=result.get("reply", ""),
        sql_query=result.get("sql_query"),
        sql_result=sql_res,  # Pydantic lo adaptará a SQLResult
        web_query=result.get("web_query"),
        web_raw_result=result.get("web_raw_result"),
    )

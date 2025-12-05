# backend/router.py
"""
Router de intención: decide si la pregunta del usuario
debe ir a SQL, búsqueda web o respuesta directa del LLM.
"""
import json
from typing import Dict, Any

from .llm_client import LLMClient
from .db_client import run_select_query
from .web_search import WebSearchClient
from .prompts import ROUTER_SYSTEM_PROMPT, LLM_ANSWER_SYSTEM_PROMPT


class AgentRouter:
    def __init__(self):
        self.llm = LLMClient()
        self.web_client = WebSearchClient()

    def route(self, user_message: str) -> Dict[str, Any]:
        """
        Devuelve un diccionario con:
        {
          "intent": "sql" | "web" | "llm",
          "reply": "texto para el usuario",
          "sql_query": str | None,
          "sql_result": {...} | None,
          "web_query": str | None,
          "web_raw_result": {...} | None
        }
        """
        # 1) Pedimos al LLM que clasifique la intención
        router_messages = [
            {"role": "system", "content": ROUTER_SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ]

        router_result = self.llm.chat_json(router_messages)
        
        print(f"Intención del usuario: {router_result.get('intent')}")
        print(f"Explicación: {router_result.get('explanation')}")

        intent = router_result.get("intent", "llm")
        sql_query = router_result.get("sql_query", "") or ""
        web_query = router_result.get("web_query", "") or ""

        # 2) Según la intención, actuamos:
        if intent == "sql" and sql_query:
            return self._handle_sql(user_message, sql_query)
        elif intent == "web" and web_query:
            return self._handle_web(user_message, web_query)
        else:
            # Intent llm o fallback
            return self._handle_llm(user_message)

    def _handle_sql(self, user_message: str, sql_query: str) -> Dict[str, Any]:
        sql_result = run_select_query(sql_query)

        # Construimos una respuesta amigable usando el LLM
        explanation_messages = [
            {"role": "system", "content": LLM_ANSWER_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    "El usuario hizo esta pregunta:\n"
                    f"{user_message}\n\n"
                    "Se ejecutó este query SQL:\n"
                    f"{sql_query}\n\n"
                    f"Y este fue el resultado (JSON):\n{sql_result}\n\n"
                    "Explica el resultado al usuario en español de forma clara."
                ),
            },
        ]

        reply_text = self.llm.chat(explanation_messages)

        return {
            "intent": "sql",
            "reply": reply_text,
            "sql_query": sql_query,
            "sql_result": sql_result,
            "web_query": None,
            "web_raw_result": None,
        }

    def _handle_web(self, user_message: str, web_query: str) -> Dict[str, Any]:
        web_result = self.web_client.search(web_query)

        # Llamamos al LLM para que sintetice

        messages = [
            {"role": "system", "content": LLM_ANSWER_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    "El usuario hizo esta pregunta:\n"
                    f"{user_message}\n\n"
                    "Se realizó esta búsqueda web:\n"
                    f"{web_query}\n\n"
                    f"Y este fueron los resultados de la búsqueda en internet:\n{web_result}\n\n"
                    "Responde al usuario en español usando esta información."
                ),
            },
        ]

        reply_text = self.llm.chat(messages)

        return {
            "intent": "web",
            "reply": reply_text,
            "sql_query": None,
            "sql_result": None,
            "web_query": web_query,
            "web_raw_result": web_result,
        }

    def _handle_llm(self, user_message: str) -> Dict[str, Any]:
        messages = [
            {"role": "system", "content": LLM_ANSWER_SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ]
        reply_text = self.llm.chat(messages)

        return {
            "intent": "llm",
            "reply": reply_text,
            "sql_query": None,
            "sql_result": None,
            "web_query": None,
            "web_raw_result": None,
        }

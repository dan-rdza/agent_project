# backend/llm_client.py
"""
Cliente simple para un servidor LLM con API compatible con OpenAI
(por ejemplo, LM Studio, llama.cpp server, etc).
"""

import json
from typing import List, Dict, Any, Optional

import requests

from .config import LLM_API_URL, LLM_API_KEY, LLM_MODEL_NAME


class LLMClient:
    def __init__(self):
        self.api_url = LLM_API_URL
        self.api_key = LLM_API_KEY
        self.model = LLM_MODEL_NAME

    def _build_headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
        }
        # Algunos servidores no requieren API key, pero dejamos el campo por compatibilidad
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.3) -> str:
        """
        Envía un chat simple y devuelve solo el texto de la respuesta.
        """
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature, # Define que tal creativo o determinista es el modelo
        }

        print(f"""🤖 Petición al LLM - Ejecución de tarea""")

        response = requests.post(
            self.api_url,
            headers=self._build_headers(),
            json=payload,
            timeout=60,
        )

        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    def chat_json(self, messages: List[Dict[str, str]], temperature: float = 0.0) -> Dict[str, Any]:
        """
        Envía un prompt al modelo y exige que responda SOLO con JSON válido.
        """

        # Forzamos al modelo a responder en JSON
        force_json_msg = {
            "role": "system",
            "content": (
                "Responde ÚNICAMENTE en JSON válido, sin texto adicional antes o después. "
                "No expliques nada, no agregues comentarios. "
                "Solo devuelve el objeto JSON."
            )
        }

        final_messages = [force_json_msg] + messages

        payload = {
            "model": self.model,
            "messages": final_messages,
            "temperature": temperature,
        }

        response = requests.post(
            self.api_url,
            headers=self._build_headers(),
            json=payload,
            timeout=60,
        )

        response.raise_for_status()
        data = response.json()

        # print(f"LLM Response: {data}")

        raw = data["choices"][0]["message"]["content"].strip()

        # A veces los modelos añaden ```json ... ```
        if raw.startswith("```"):
            raw = raw.strip("`")
            raw = raw.replace("json", "", 1).strip()

        try:
            return json.loads(raw)
        except Exception:
            # Fallback si el modelo no obedeció
            return {
                "intent": "llm",
                "explanation": "No pude interpretar JSON, devolviendo fallback.",
                "raw_response": raw,
            }

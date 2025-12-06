# backend/llm_client.py

import requests
from typing import List, Dict, Any
from .config import (
    LLM_PROVIDER,
    OPENAI_API_KEY,
    GEMINI_API_KEY,
    LLM_API_BASE,
    LLM_MODEL,
)

# IMPORTS SEGÚN PROVEEDOR
try:
    from openai import OpenAI
except:
    OpenAI = None

try:
    from google import genai
    from google.genai import types
except:
    genai = None


class LLMClient:
    """
    Cliente universal para múltiples proveedores LLM:
    - LM Studio / Ollama / llama.cpp (OpenAI-like)
    - OpenAI oficial
    - Gemini (Google)
    """

    def __init__(self):
        # OpenAI client
        if LLM_PROVIDER == "openai" and OpenAI:            

            self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
            self.openai_model = "gpt-5-mini"

        # Gemini client
        if LLM_PROVIDER == "gemini":
            self.gemini_client = genai.Client(api_key=GEMINI_API_KEY)
            self.gemini_model = "gemini-2.5-flash" 

    # ---------------------------
    # INTERFAZ PRINCIPAL
    # ---------------------------
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """
        Devuelve texto plano generado por el LLM.
        """
        if LLM_PROVIDER == "local":
            return self._lmstudio(messages)

        elif LLM_PROVIDER == "openai":
            return self._openai(messages)

        elif LLM_PROVIDER == "gemini":
            return self._gemini(messages)

        else:
            raise ValueError(f"Proveedor LLM desconocido: {LLM_PROVIDER}")

    # ---------------------------
    # PETICIÓN JSON UNIVERSAL
    # ---------------------------
    def chat_json(self, messages):
        """
        Envía un prompt para recibir un JSON válido.
        Si el modelo responde texto mixto, limpiamos y extraemos el JSON.
        """

        # Añadir instrucción estricta
        json_instruction = {
            "role": "system",
            "content": (
                "Responde únicamente con un JSON válido. No incluyas explicación, "
                "texto adicional, ni comentarios. Solo devuelve un objeto JSON."
            )
        }

        full_messages = [json_instruction] + messages

        raw_output = self.chat(full_messages)

        # Intentar extraer JSON
        cleaned = self._extract_json(raw_output)

        return cleaned

    # ---------------------------
    # UTILIDAD: EXTRACCIÓN DE JSON
    # ---------------------------
    def _extract_json(self, text):
        """
        Extrae JSON válido incluso si viene envuelto en bloques Markdown
        como ```json ... ``` o ``` ... ```.
        """

        import json
        import re

        # 1. Intento directo
        try:
            return json.loads(text)
        except:
            pass

        # 2. Eliminar fences tipo ```json ... ``` o ```
        cleaned = re.sub(r"```json|```", "", text, flags=re.IGNORECASE).strip()

        # Intento parsear después de limpiar
        try:
            return json.loads(cleaned)
        except:
            pass

        # 3. Extraer todo lo que esté entre llaves {...}
        try:
            match = re.search(r"\{[\s\S]*\}", cleaned)
            if match:
                return json.loads(match.group(0))
        except:
            pass

        # 4. Si todo falla → error visible
        raise ValueError(f"El modelo no devolvió JSON válido: {text}")

    # ---------------------------
    # IMPLEMENTACIONES
    # ---------------------------

    def _lmstudio(self, messages: List[Dict[str, str]]) -> str:
        """
        Para LM Studio / Ollama / llama.cpp / servidores OpenAI-like.
        """
        url = f"{LLM_API_BASE}/chat/completions"

        print(f"URL API LOCAL: {url}")

        payload = {
            "model": LLM_MODEL,
            "messages": messages,
            "temperature": 0.2,
        }
        #print(f"Payload: {payload}")
        response = requests.post(url, json=payload, timeout=60)
        #print(f"Response: {response}")
        if not response.ok:
            raise RuntimeError(
                f"Error LLM local: {response.status_code} -> {response.text}"
            )

        data = response.json()
        return data["choices"][0]["message"]["content"]

    def _openai(self, messages):
        """
        Cliente actualizado para la API Responses de OpenAI (2025+)
        """

        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY no está configurado")

        # Convertimos los mensajes tipo ChatGPT a texto lineal, como lo requiere Responses
        input_text = ""
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            input_text += f"{role.upper()}: {content}\n"

        # Llamada al endpoint moderno
        response = self.openai_client.responses.create(
            model=self.openai_model,  
            input=input_text,
        )

        return response.output_text

    def _gemini(self, messages):
        """
        Implementación que convierte mensajes estilo OpenAI
        a contenido compatible con Google GenAI (nuevo SDK).
        """

        # Convertir messages (role, content) a estructura de Google
        contents = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=msg["content"])]
                )
            )

        response = self.gemini_client.models.generate_content(
            model=self.gemini_model,
            contents=contents,
        )

        return response.text

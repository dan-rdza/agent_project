# backend/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Selecciona el proveedor de LLM:
# "local", "openai", "gemini"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "local")

# Para proveedores que usen API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Para proveedores OpenAI-like (LM Studio, Ollama, etc.)
LLM_API_BASE = os.getenv("LLM_API_BASE", "http://localhost:8001/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.2-8b-instruct")

# Tavily
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
DB_PATH = os.getenv("DB_PATH", "./tickets.db")

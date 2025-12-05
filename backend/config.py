# backend/config.py
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

LLM_API_URL = os.getenv("LLM_API_URL", "http://localhost:8001/v1/chat/completions")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "llama-3.2-8b-instruct")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

DB_PATH = os.getenv("DB_PATH", "./tickets.db")

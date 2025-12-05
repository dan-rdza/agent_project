# backend/web_search.py
"""
Módulo para búsquedas web usando Tavily.
Devuelve una lista de resultados simples: [{"title": "...", "content": "...", "url": "..."}].
"""

from typing import Dict, Any, List
from tavily import TavilyClient

from .config import TAVILY_API_KEY


class WebSearchClient:
    def __init__(self):
        if not TAVILY_API_KEY:
            raise ValueError("TAVILY_API_KEY no está configurado en el .env")
        self.client = TavilyClient(api_key=TAVILY_API_KEY)

    def search(self, query: str, score_threshold: float = 0.30) -> List[Dict[str, str]]:
        """
        Realiza una búsqueda web y devuelve una lista de resultados simplificados:
        [{
            "title": "...",
            "content": "...",
            "url": "..."
        }]
        """

        result = self.client.search(
            query=query,
            include_answer="basic",
            include_raw_content="text",
            max_results=3
        )

        raw_results = result.get("results", [])
        filtered = [r for r in raw_results if r.get("score", 0) >= score_threshold]

        simplified = []

        for item in filtered:
            title = item.get("title", "Sin título")
            content = (item.get("content") or "").strip()
            url = item.get("url", "")

            # Recortar contenido largo
            if len(content) > 500:
                content = content[:500] + "..."

            simplified.append({
                "title": title,
                "content": content,
                "url": url,
            })

        return simplified

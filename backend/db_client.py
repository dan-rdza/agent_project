# backend/db_client.py
"""
Módulo para manejar la conexión a la base de datos SQLite
y ejecutar consultas de solo lectura de forma segura.
"""

import sqlite3
from typing import Any, Dict

from .config import DB_PATH


FORBIDDEN_SQL_KEYWORDS = [
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "create",
    "truncate",
    "attach",
    "detach",
    "pragma",
]


def is_safe_select_query(query: str) -> bool:
    """
    Valida que el query sea un SELECT y que no intente modificar la BD.
    Es un validador simple para fines educativos.
    """
    q_lower = query.strip().lower()

    # Debe comenzar con "select"
    if not q_lower.startswith("select"):
        return False

    # No debe contener palabras peligrosas
    for kw in FORBIDDEN_SQL_KEYWORDS:
        if kw in q_lower:
            return False

    # Puedes agregar más restricciones si quieres (ej. un solo statement, sin ';')
    if ";" in q_lower:
        # Permitimos un ';' al final, pero no múltiples statements
        if q_lower.count(";") > 1:
            return False

    return True


def run_select_query(query: str) -> Dict[str, Any]:
    """
    Ejecuta un SELECT seguro y devuelve:
    {
        "columns": [...],
        "rows": [...]
    }
    """
    if not is_safe_select_query(query):
        return {
            "error": "El query no es seguro o no es un SELECT.",
            "columns": [],
            "rows": [],
        }

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        conn.close()

        return {
            "columns": column_names,
            "rows": rows,
        }
    except Exception as e:
        return {
            "error": str(e),
            "columns": [],
            "rows": [],
        }

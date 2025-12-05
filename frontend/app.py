# frontend/app.py
"""
Interfaz sencilla de chat usando Streamlit.
Se comunica con el backend FastAPI en http://localhost:8000/agent
"""

import requests
import streamlit as st

BACKEND_URL = "http://localhost:8000/agent"


def send_message_to_backend(message: str):
    payload = {"message": message}
    resp = requests.post(BACKEND_URL, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()


def main():
    st.set_page_config(page_title="Agente LLM", page_icon="🤖")
    st.title("🤖 Agente LLM")

    # Estado de la conversación
    if "chat_history" not in st.session_state:
        # Cada elemento: {"role": "user"/"assistant", "content": str, "meta": dict}
        st.session_state.chat_history = []

    # Creamos contenedores para controlar el orden visual:
    # - Primero se muestra el historial (arriba)
    # - Luego el input del usuario (abajo)
    history_container = st.container()
    input_container = st.container()

    # --- INPUT DEL USUARIO (lógicamente primero, visualmente abajo) ---
    with input_container:
        user_input = st.chat_input("Escribe tu mensaje...")

        if user_input:
            # Guardamos mensaje de usuario en el historial
            st.session_state.chat_history.append(
                {"role": "user", "content": user_input, "meta": {}}
            )

            # Llamamos al backend y guardamos la respuesta del asistente
            try:
                with st.spinner("Pensando..."):
                    response = send_message_to_backend(user_input)

                reply = response.get("reply", "")

                st.session_state.chat_history.append(
                    {
                        "role": "assistant",
                        "content": reply,
                        "meta": {
                            "intent": response.get("intent"),
                            "sql_query": response.get("sql_query"),
                            "sql_result": response.get("sql_result"),
                            "web_raw_result": response.get("web_raw_result"),
                        },
                    }
                )

            except Exception as e:
                # En caso de error, agregamos un mensaje de asistente con el error
                error_msg = f"Error al comunicar con el backend: {e}"
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": error_msg, "meta": {}}
                )

    # --- MOSTRAR HISTORIAL COMPLETO (incluye el último turno) ---
    with history_container:
        for msg in st.session_state.chat_history:
            role = msg["role"]
            content = msg["content"]
            meta = msg.get("meta", {}) or {}

            if role == "user":
                with st.chat_message("user"):
                    st.markdown(content)
            else:
                with st.chat_message("assistant"):
                    st.markdown(content)

                    # Si hay meta de SQL, mostramos tabla
                    if meta.get("intent") == "sql" and meta.get("sql_result"):
                        st.caption("🚀 Fuente: Base de datos de tickets") 
                        st.code(f"{meta.get('sql_query')}",language="sql")
                        sql_res = meta["sql_result"]

                        # Por si el backend manda algún error encapsulado ahí
                        if isinstance(sql_res, dict) and sql_res.get("error"):
                            st.error(f"Error SQL: {sql_res['error']}")
                        elif isinstance(sql_res, dict):
                            cols = sql_res.get("columns", [])
                            rows = sql_res.get("rows", [])
                            if cols and rows:
                                st.caption("Resultados de la consulta SQL:")
                                st.dataframe(
                                    [dict(zip(cols, row)) for row in rows],
                                    width=True,
                                )

                    # Opcional: mostrar fuentes web si la intención fue "web"
                    if meta.get("intent") == "web" and meta.get("web_raw_result"):
                        st.caption("🌍 Fuentes utilizadas (búsqueda web)")
                        sources = meta["web_raw_result"]
                        # Esperamos una lista de dicts con 'title' y 'url'
                        if isinstance(sources, list):
                            for i, source in enumerate(sources, start=1):
                                title = source.get("title", "Sin título")
                                url = source.get("url")
                                if url:
                                    st.markdown(f"- {i}. [{title}]({url})")
                                else:
                                    st.markdown(f"- {i}. {title}")

                    if meta.get("intent") == "llm":
                        st.caption("🧠 Se ha utilizado el conocimiento del LLM")


if __name__ == "__main__":
    main()

# frontend/app.py
"""
Interfaz tipo chat usando Streamlit.
"""

import requests
import streamlit as st

BACKEND_URL = "http://localhost:8000/agent"
CHAT_NAME = "BEDUito"

def send_message_to_backend(message: str):
    payload = {"message": message}
    resp = requests.post(BACKEND_URL, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()


def main():
    st.set_page_config(page_title=CHAT_NAME, page_icon="🤖")
    st.title("🧠 BEDUito Chat")

    # Estado de la conversación
    if "chat_history" not in st.session_state:
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
                with st.spinner("Procesando..."):
                    response = send_message_to_backend(user_input)
                
                # print(f"All response from LLm: {response}")            
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
                source_caption = ""
                with st.chat_message("assistant"):
                    st.markdown(content)

                    # Si hay meta de SQL, mostramos tabla
                    if meta.get("intent") == "sql" and meta.get("sql_result"):                                                
                        sql_res = meta["sql_result"]
                        source_caption = "**🚀 Fuente:** Base de datos de tickets"
                        # Por si el backend manda algún error encapsulado ahí
                        if isinstance(sql_res, dict) and sql_res.get("error"):
                            st.error(f"Error SQL: {sql_res['error']}")
                        elif isinstance(sql_res, dict):
                            cols = sql_res.get("columns", [])
                            rows = sql_res.get("rows", [])
                            if cols and rows:
                                st.caption("Resultados de la consulta SQL:")
                                st.code(f"{meta.get('sql_query')}",language="sql")
                                st.dataframe(
                                    [dict(zip(cols, row)) for row in rows],                                    
                                )

                    # Opcional: mostrar fuentes web si la intención fue "web"
                    if meta.get("intent") == "web" and meta.get("web_raw_result"):
                        source_caption ="**🌍 Fuente:** Búsqueda en la web"
                        sources = meta["web_raw_result"]
                        # Esperamos una lista de dicts con 'title' y 'url'
                        if isinstance(sources, list):
                            for i, source in enumerate(sources, start=1):
                                title = source.get("title", "Sin título")
                                url = source.get("url")
                                if url:
                                    st.badge(f"{i}. [{title}] ({url})", color="violet")
                                else:
                                    st.badge(f"{i}. {title}", color="violet")

                    if meta.get("intent") == "llm":
                        source_caption = "**🧠 Fuente:** Conocimiento del LLM"
                    
                    st.caption(source_caption) 

if __name__ == "__main__":
    main()

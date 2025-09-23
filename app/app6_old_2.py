import streamlit as st

# ----------------------------------------
# EJECUCIÓN PRINCIPAL
# ----------------------------------------
def main():

    import streamlit as st
    import PyPDF2
    import ollama
    import pandas as pd
    import time

    # CONFIGURACIÓN
    st.set_page_config(page_title="📑 Analizador de Contratos IA", layout="wide")
    MODEL = "gpt-oss:20b" #  llama3:instruct | jobautomation/OpenEuroLLM-Spanish | gpt-oss:20b

    # ---------------------------
    # FUNCIONES
    # ---------------------------

    def cargar_pdf(uploaded_file, max_paginas=50):
        reader = PyPDF2.PdfReader(uploaded_file)
        contenido_paginas = []

        for i, page in enumerate(reader.pages[:max_paginas]):
            text = page.extract_text()
            if text:
                contenido_paginas.append((i + 1, text))

        return contenido_paginas

    def dividir_en_bloques(paginas, tamaño_bloque=10):
        bloques = []
        for i in range(0, len(paginas), tamaño_bloque):
            bloque = paginas[i:i + tamaño_bloque]
            texto_bloque = "\n\n".join([f"[Página {p}] {t}" for p, t in bloque])
            bloques.append((bloque[0][0], bloque[-1][0], texto_bloque))
        return bloques

    def preguntar_al_modelo_streaming(prompt):
        respuesta = ""
        try:
            response = ollama.chat(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                stream=True
            )
            for chunk in response:
                chunk_text = chunk.get('message', {}).get('content', '')
                respuesta += chunk_text
                yield chunk_text
        except Exception as e:
            yield f"❌ Error al generar respuesta: {str(e)}"

    # ---------------------------
    # SESIONES
    # ---------------------------

    if "analisis_bloques" not in st.session_state:
        st.session_state.analisis_bloques = []

    if "contenido_pdf" not in st.session_state:
        st.session_state.contenido_pdf = []

    if "chat" not in st.session_state:
        st.session_state.chat = []

    # ---------------------------
    # INTERFAZ
    # ---------------------------

    st.title("📄 Analizador de Contratos con IA")
    st.caption("Sube un contrato en PDF (máximo 50 páginas). IA buscará artículos sobre fideicomisos y fórmulas.")

    uploaded_file = st.file_uploader("🔽 Sube un archivo PDF", type=["pdf"])

    if uploaded_file:
        with st.spinner("📖 Leyendo y dividiendo el contrato en bloques..."):
            contenido = cargar_pdf(uploaded_file, max_paginas=50)
            bloques = dividir_en_bloques(contenido, tamaño_bloque=10)
            st.session_state.contenido_pdf = contenido
            st.session_state.analisis_bloques = []

        st.success("✅ Archivo cargado correctamente. Comienza el análisis...")

        for idx, (inicio, fin, bloque) in enumerate(bloques):
            with st.expander(f"🧾 Bloque {idx + 1} (Páginas {inicio}-{fin})", expanded=False):
                consulta = f"""
    Tengo un contrato legal. Quiero que busques en el siguiente texto todos los artículos o secciones que hagan referencia a cualquier tipo de "reserva de fideicomisos".

    Para cada artículo encontrado, devuélveme:
    1. El número o nombre del artículo
    2. La página (si la menciono en el texto que te doy)
    3. Un resumen en 1 sola frase de qué trata ese artículo

    Además, si el artículo contiene una fórmula o ecuación:
    - Extrae la fórmula exacta
    - Explica el significado de cada variable o constante
    - Devuélvelo en una tabla con columnas: Artículo, Fórmula, Variable, Definición

    Respode siempre en ESPAÑOL.

    Texto del contrato (páginas {inicio}-{fin}):

    {bloque}
    """

                output_placeholder = st.empty()
                full_output = ""

                with st.status("🤖 Analizando bloque con IA..."):
                    for chunk in preguntar_al_modelo_streaming(consulta):
                        full_output += chunk
                        output_placeholder.markdown(full_output)

                st.session_state.analisis_bloques.append(full_output)

        st.markdown("---")

    # ---------------------------
    # MODO CHAT IA
    # ---------------------------

    if st.session_state.contenido_pdf:
        st.subheader("💬 Haz preguntas sobre el contrato")

        for msg in st.session_state.chat:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        pregunta = st.chat_input("¿Qué quieres preguntar sobre el contrato?")

        if pregunta:
            with st.chat_message("user"):
                st.markdown(pregunta)
            st.session_state.chat.append({"role": "user", "content": pregunta})

            # Unimos el contenido de las páginas cargadas (limitado a 50)
            contexto = "\n\n".join([f"[Página {p}] {t}" for p, t in st.session_state.contenido_pdf])

            prompt_chat = f"""Este es el contenido parcial de un contrato legal en español:

    {contexto}

    Pregunta del usuario: {pregunta}
    """

            with st.chat_message("assistant"):
                placeholder = st.empty()
                full_response = ""
                with st.status("🧠 Pensando..."):
                    for chunk in preguntar_al_modelo_streaming(prompt_chat):
                        full_response += chunk
                        placeholder.markdown(full_response)

            st.session_state.chat.append({"role": "assistant", "content": full_response})


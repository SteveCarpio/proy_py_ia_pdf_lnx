import streamlit as st
#from datetime import datetime

# ----------------------------------------
# EJECUCIÓN PRINCIPAL
# ----------------------------------------
def main():
    import PyPDF2
    import ollama
    import time
    from datetime import datetime

    # CONFIG
    #st.set_page_config(page_title="📄 Contratos por bloques con IA", layout="wide")
    MODEL = "gpt-oss:20b"  #  jobautomation/OpenEuroLLM-Spanish | gpt-oss:20b

    # ---------------------------
    # FUNCIONES
    # ---------------------------

    def cargar_pdf_por_rango(uploaded_file, pag_inicio, pag_fin):
        reader = PyPDF2.PdfReader(uploaded_file)
        contenido_paginas = []

        total_paginas = len(reader.pages)
        pag_inicio = max(1, pag_inicio)
        pag_fin = min(total_paginas, pag_fin)

        for i in range(pag_inicio - 1, pag_fin):
            texto = reader.pages[i].extract_text()
            if texto:
                contenido_paginas.append((i + 1, texto))

        return contenido_paginas

    def dividir_en_bloques(paginas, tamaño_bloque=10):
        bloques = []
        for i in range(0, len(paginas), tamaño_bloque):
            bloque = paginas[i:i + tamaño_bloque]
            texto_bloque = "\n\n".join([f"[Página {p}] {t}" for p, t in bloque])
            bloques.append((bloque[0][0], bloque[-1][0], texto_bloque))
        return bloques

    def preguntar_a_bloque(texto_bloque, pregunta):
        prompt = f"""
    Estás leyendo un contrato legal. A continuación tienes un bloque de texto (extraído del contrato). 

    Texto:
    {texto_bloque}

    Pregunta:
    {pregunta}

    Devuelve solo la respuesta relevante al bloque, indicando la página/artículo si aplica.
    """
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
            return respuesta
        except Exception as e:
            return f"❌ Error: {str(e)}"

    # ---------------------------
    # SESIONES
    # ---------------------------

    if "contenido_pdf" not in st.session_state:
        st.session_state.contenido_pdf = []

    if "bloques" not in st.session_state:
        st.session_state.bloques = []

    if "chat_hist" not in st.session_state:
        st.session_state.chat_hist = []

    # ---------------------------
    # SIDEBAR CONFIGURACIÓN
    # ---------------------------

    st.sidebar.title("🤖 : Contratos PDF")

    uploaded_file = st.sidebar.file_uploader("📎 Sube el PDF del contrato", type=["pdf"])

    pag_inicio = st.sidebar.number_input("📄 Página de inicio", min_value=1, value=1, step=1)
    pag_fin = st.sidebar.number_input("📄 Página final", min_value=1, value=10, step=1)
    tam_bloque = st.sidebar.number_input("📦 Tamaño del bloque", min_value=1, value=2, step=1)

    cargar_btn = st.sidebar.button("📥 Cargar PDF y dividir en bloques")

    if st.sidebar.button("🔄 Nuevo análisis"):
        st.session_state.contenido_pdf = []
        st.session_state.bloques = []
        st.session_state.chat_hist = []
        st.rerun()


    # ---------------------------
    # PROCESAMIENTO DEL PDF
    # ---------------------------

    st.title("🤖 Visor de Contratos Dividido por Bloques 📚")
    st.caption("Carga por rango, analiza por bloques, y pregunta por IA sin superar el límite de contexto.")

    access_inicio = datetime.now().strftime("%H:%M:%S")

    if uploaded_file and cargar_btn:
        with st.spinner("🔄 Procesando archivo..."):
            contenido = cargar_pdf_por_rango(uploaded_file, pag_inicio, pag_fin)
            bloques = dividir_en_bloques(contenido, tamaño_bloque=tam_bloque)

            st.session_state.contenido_pdf = contenido
            st.session_state.bloques = bloques
            st.session_state.chat_hist = []
        
        # Obtener IP del cliente si está disponible
            client_ip = st.context.ip_address  # solo disponible en v1.45.0+
            if client_ip:
                access_time = datetime.now().strftime(f"%Y-%m-%d > {access_inicio} > %H:%M:%S")
                with open("/home/robot/Python/x_log/streamlit_ip.log", "a") as f:
                    f.write(f"{access_time} > {client_ip} > APPS_IA > Contratos_PDF > {uploaded_file.name} > {pag_inicio}|{pag_fin}|{tam_bloque} \n")

        st.success(f"✅ {len(bloques)} bloques creados (Páginas {pag_inicio}-{pag_fin})")

    # ---------------------------
    # MOSTRAR BLOQUES
    # ---------------------------

    if st.session_state.bloques:
        st.subheader("📦 Bloques del contrato")
        for idx, (inicio, fin, bloque_texto) in enumerate(st.session_state.bloques):
            with st.expander(f"📚 Bloque {idx + 1} (Páginas {inicio}-{fin})", expanded=False):
                st.markdown(bloque_texto)

    # ---------------------------
    # MODO CHAT POR BLOQUES
    # ---------------------------

    if st.session_state.bloques:
        st.markdown("---")
        st.subheader("💬 Pregunta al contrato (procesando bloque por bloque)")

        # Mostrar historial
        for msg in st.session_state.chat_hist:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        pregunta = st.chat_input("¿Qué quieres preguntar sobre el contrato?")

        if pregunta:
            with st.chat_message("user"):
                st.markdown(pregunta)
            st.session_state.chat_hist.append({"role": "user", "content": pregunta})

            resumen_respuestas = ""

            with st.chat_message("assistant"):
                status = st.status("🤖 Analizando bloques...", expanded=False)
                for idx, (pag_ini, pag_fin, texto_bloque) in enumerate(st.session_state.bloques):
                    st.markdown(f"🔎 **Bloque {idx+1}** (Páginas {pag_ini}-{pag_fin})")
                    with st.spinner(f"Consultando bloque {idx + 1}..."):
                        respuesta = preguntar_a_bloque(texto_bloque, pregunta)
                        st.markdown(respuesta)
                        resumen_respuestas += f"🧩 Bloque {idx+1} (Pág. {pag_ini}-{pag_fin}):\n{respuesta}\n\n"
                status.update(label="✅ Consulta completada", state="complete")

            st.session_state.chat_hist.append({"role": "assistant", "content": resumen_respuestas})

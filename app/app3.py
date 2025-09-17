import streamlit as st
import time
import ollama
import pandas as pd
import PyPDF2
from pathlib import Path
from datetime import datetime

# ----------------------------------------
# FUNCIONES PARA LEER ARCHIVOS
# ----------------------------------------

def leer_archivo(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1].lower()

    if file_type == 'txt':
        return uploaded_file.read().decode('utf-8')

    elif file_type == 'pdf':
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text

    elif file_type in ['xls', 'xlsx']:
        df = pd.read_excel(uploaded_file)
        return df.to_string(index=False)

    elif file_type == 'csv':
        df = pd.read_csv(uploaded_file)
        return df.to_string(index=False)

    else:
        return "❌ Tipo de archivo no soportado todavía."

# ----------------------------------------
# APP PRINCIPAL
# ----------------------------------------

def main():
    # Inicializar historial de chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Inicializar contador de chats
    if "chat_counter" not in st.session_state:
        st.session_state.chat_counter = 1

    # SIDEBAR
    with st.sidebar:
        st.markdown("---")

        # Botón para nuevo chat
        if st.button("🗑️ Nuevo chat"):   # 🗑️   🆕
            st.session_state.messages = []
            st.session_state.chat_counter += 1
            st.rerun()

        # Selector de modelo
        model_choice = st.selectbox(
            "🧠 Selecciona el modelo:",
            ["llama3:instruct", "mistral:latest", "jobautomation/OpenEuroLLM-Spanish"],
            index=0,
            help="Modelos disponibles localmente (en continuo desarrollo)."
        )

        st.markdown("""
        **📝 Instrucciones:**
        1. Sube un archivo (opcional)
        2. Selecciona un modelo (opcional)
        2. Escribe tu pregunta
        3. Presiona 'Enviar'
        """)

        st.markdown(f"**Modelo activo:** `{model_choice}`")
        st.markdown(f"**Chat actual:** #{st.session_state.chat_counter}")

    # TÍTULO
    st.title(f"🤖 ChatTDA (Chat #{st.session_state.chat_counter})")
    st.caption(f"Puedes conversar con el modelo local '{model_choice}' y subir archivos para analizarlos. No se guarda ningún dato en servidores externos.")

    # SUBIR ARCHIVO
    st.markdown("### 📄 Subir archivo para análisis")
    uploaded_file = st.file_uploader("Sube un archivo (.txt, .pdf, .xlsx, .csv)", type=["txt", "pdf", "xlsx", "csv"])

    file_content = None
    if uploaded_file is not None:
        try:
            file_content = leer_archivo(uploaded_file)
            st.success(f"Archivo '{uploaded_file.name}' cargado correctamente.")
            with st.expander("📃 Ver contenido del archivo"):
                st.text(file_content[:2000] + "..." if len(file_content) > 2000 else file_content)

            # Agregar contenido como contexto del sistema
            st.session_state.messages.append({
                "role": "system",
                "content": f"El usuario ha subido un archivo con el siguiente contenido:\n\n{file_content}"
            })

        except Exception as e:
            st.error(f"❌ Error al procesar el archivo: {str(e)}")

    # MOSTRAR HISTORIAL
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ENTRADA DEL USUARIO
    if prompt := st.chat_input("Escribe tu pregunta aquí..."):
        # Mostrar pregunta del usuario
        with st.chat_message("user"):
            st.markdown(prompt)

        # Añadir al historial
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Mostrar respuesta del asistente
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            start_time = time.time()

            try:
                # Enviar todo el historial al modelo
                response = ollama.chat(
                    model=model_choice,
                    messages=st.session_state.messages,
                    stream=True
                )

                # Mostrar respuesta en tiempo real
                for chunk in response:
                    chunk_content = chunk.get('message', {}).get('content', '')
                    full_response += chunk_content
                    message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)
                end_time = time.time()

                st.caption(f"⏱ Tiempo de respuesta: {end_time - start_time:.2f} segundos")

                # Añadir respuesta al historial
                st.session_state.messages.append({"role": "assistant", "content": full_response})

                # Guardar IP si es posible (opcional, versión Streamlit 1.45+)
                client_ip = getattr(st.context, "ip_address", None)
                if client_ip:
                    access_time = datetime.now().strftime("%Y-%m-%d > %H:%M:%S")
                    log_path = "/home/robot/Python/x_log/streamlit_ip.log"
                    with open(log_path, "a") as f:
                        f.write(f"{access_time} > {client_ip} > Pag3 > IA_ChatTDA({model_choice}) >> {prompt}\n")

            except Exception as e:
                st.error(f"❌ Error al generar respuesta: {str(e)}")
                st.session_state.messages.append({"role": "assistant", "content": f"Error: {str(e)}"})


# ----------------------------------------
# EJECUCIÓN PRINCIPAL
# ----------------------------------------

if __name__ == "__main__":
    main()

import streamlit as st
import time
import ollama
import pandas as pd
import PyPDF2
from pathlib import Path
from datetime import datetime

# ----------------------------------------
# FUNCIONES
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

def resumir_contenido(texto):
    resumen = texto.strip().split('\n')
    resumen = [line for line in resumen if len(line.strip()) > 30]
    return '\n'.join(resumen[:5]) + ("\n..." if len(resumen) > 5 else '')

# ----------------------------------------
# APP PRINCIPAL
# ----------------------------------------

def main():

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chat_counter" not in st.session_state:
        st.session_state.chat_counter = 1

    if "file_content" not in st.session_state:
        st.session_state.file_content = None

    if "file_name" not in st.session_state:
        st.session_state.file_name = None

    # SIDEBAR
    with st.sidebar:
        st.subheader("🤖 : ChatTdA")
        
        if st.button("🆕 Nuevo chat"):
            st.session_state.messages = []
            st.session_state.chat_counter += 1
            st.session_state.file_content = None
            st.session_state.file_name = None
            st.rerun()

        if st.session_state.file_name:
            st.markdown(f"**📁 Archivo cargado:** `{st.session_state.file_name}`")
            if st.button("❌ Quitar archivo"):
                st.session_state.file_content = None
                st.session_state.file_name = None
                st.rerun()
        
        # ["llama3:instruct", "mistral:latest", "jobautomation/OpenEuroLLM-Spanish", "gpt-oss:20b"]
        model_choice = st.selectbox(
            "🧠 Modelo:",
            ["tda-llama3", "tda-gpt20b", "codellama", "deepseek-coder"],
            index=0
        )

        st.markdown("""
        **💡 Tips de uso:**
        - Sube un archivo (PDF, TXT, Excel, CSV)
        - Escribe tu pregunta
        - El modelo considerará el archivo cargado como contexto
        """)

    # CONTENIDO PRINCIPAL
    st.title(f"🤖 Chat #{st.session_state.chat_counter}")
    st.caption("Interfaz de chat IA con soporte para archivos y modelo local.")

    # SUBIDA DE ARCHIVO
    uploaded_file = st.file_uploader("📎 Sube un archivo", type=["txt", "pdf", "xlsx", "csv"])
    if uploaded_file is not None:
        try:
            file_ext = uploaded_file.name.split('.')[-1].lower()
            st.session_state.file_name = uploaded_file.name

            if file_ext == 'txt':
                contenido = uploaded_file.read().decode('utf-8')
                st.session_state.file_content = contenido
                st.session_state.file_df = None  # No hay DataFrame

            elif file_ext == 'pdf':
                reader = PyPDF2.PdfReader(uploaded_file)
                text = ''
                for page in reader.pages:
                    text += page.extract_text()
                st.session_state.file_content = text
                st.session_state.file_df = None

            elif file_ext == 'xlsx':
                df = pd.read_excel(uploaded_file)
                st.session_state.file_df = df
                st.session_state.file_content = df.to_string(index=False)

            elif file_ext == 'csv':
                df = pd.read_csv(uploaded_file)
                st.session_state.file_df = df
                st.session_state.file_content = df.to_string(index=False)

            else:
                st.session_state.file_content = "❌ Tipo de archivo no soportado."
                st.session_state.file_df = None

        except Exception as e:
            st.error(f"❌ Error al procesar archivo: {str(e)}")


    # Mostrar contenido del archivo cargado
    if st.session_state.file_content and st.session_state.file_name:
        file_name = st.session_state.file_name
        file_ext = file_name.split('.')[-1].lower()

        with st.expander("📃 Vista previa del archivo cargado", expanded=False):
            if file_ext in ['xlsx', 'csv'] and st.session_state.get("file_df") is not None:
                st.dataframe(st.session_state.file_df.head(50).reset_index(drop=True).rename_axis('').set_index(pd.RangeIndex(1, 1 + len(st.session_state.file_df.head(50)))))
            else:
                resumen = resumir_contenido(st.session_state.file_content)
                st.text_area("Resumen:", resumen, height=200)

    # HISTORIAL DEL CHAT
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and "Última respuesta" in message:
                st.code(message["content"], language="markdown")

    # INPUT DEL USUARIO

    access_inicio = datetime.now().strftime("%H:%M:%S")

    if prompt := st.chat_input("Escribe tu pregunta..."):
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            status = st.status("Pensando... 🤔", expanded=False)

            start_time = time.time()

            try:
                # Crear historial + contexto si hay archivo
                mensajes_para_modelo = st.session_state.messages.copy()

                if st.session_state.file_content:
                    contexto = f"El usuario ha subido un archivo con el siguiente contenido:\n\n{st.session_state.file_content}"
                    mensajes_para_modelo = [{"role": "system", "content": contexto}] + mensajes_para_modelo

                # Llamar al modelo
                response = ollama.chat(
                    model=model_choice,
                    messages=mensajes_para_modelo,
                    stream=True
                )

                for chunk in response:
                    chunk_content = chunk.get('message', {}).get('content', '')
                    full_response += chunk_content
                    message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})

                # Copiar al portapapeles (si Streamlit soporta clipboard en frontend)
                #st.code(full_response, language="markdown")
                #st.button("📋 Copiar última respuesta", help="(Haz clic derecho > copiar)")

                end_time = time.time()
                status.update(label=f"✅ Respuesta generada en {end_time - start_time:.2f} segundos", state="complete")


                # Obtener IP del cliente si está disponible
                client_ip = st.context.ip_address  # solo disponible en v1.45.0+
                if client_ip:
                    access_time = datetime.now().strftime(f"%Y-%m-%d > {access_inicio} > %H:%M:%S")
                    #st.write(f"Acceso desde IP local: {client_ip} a las {access_time}")
                    with open("/home/robot/Python/x_log/streamlit_ip.log", "a") as f:
                        f.write(f"{access_time} > {client_ip} > APPS_IA > ChatTdA > {model_choice} > {prompt}\n")


            except Exception as e:
                st.error(f"❌ Error al generar respuesta: {str(e)}")
                st.session_state.messages.append({"role": "assistant", "content": f"Error: {str(e)}"})


# ----------------------------------------
# EJECUCIÓN PRINCIPAL
# ----------------------------------------

if __name__ == "__main__":
    main()

import streamlit as st

def main():
    import streamlit as st
    import os
    import re
    import json
    import shutil
    from io import BytesIO
    import tempfile
    from datetime import datetime
    import pandas as pd
    import pdfplumber
    from pdf2image import convert_from_bytes
    import pytesseract
    import ollama

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Configuración inicial de la app
    #st.set_page_config("(TDA) Lector de Facturas IA", layout="wide")
    st.title("🤖 Transcrición de Audio")  # 🗂️ 📄  🤖
    st.caption("Combina ASR (Reconocimiento Automático de Voz) con modelos LLM para transformar audio en texto estructurado y resúmenes contextuales.")

    # Crear directorio temporal para subidas
    UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), "transcripcion_audio")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    st.sidebar.markdown("---")  # Separador

    # Opción 2: Subida de archivos desde el cliente
    uploaded_files = st.sidebar.file_uploader(
        label="📁 Seleccione Archivo AUDIO  ",  
        type=["mp3", "wav", "ogg"],
        accept_multiple_files=False,
        label_visibility="visible" 
    )


    # Si se sube el archivo a la carpeta temporal de Linux
    if uploaded_files is not None:
        extension = os.path.splitext(uploaded_files.name)[1]
        file_path = os.path.join("/tmp/transcripcion_audio/", uploaded_files.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_files.getbuffer())
        st.audio(uploaded_files, format=uploaded_files.type.split("/")[-1])
        os.rename(file_path, file_path.replace(uploaded_files.name, f'REUNION_1_audio_{timestamp}{extension}'))

    folder = "/home/robot/Python/x_audios"

    # Procesar archivos subidos
    if uploaded_files:      
        st.sidebar.success(f"✅ Se subio correctamente")
        folder = UPLOAD_FOLDER  # Usar la carpeta de subidas para procesamiento

    # BOTÓN: para procesar AUDIO
    if st.sidebar.button("Procesar AUDIO"):
        
        if uploaded_files is None:
            st.write("")
            st.write(" ℹ️ Debe seleccionar un fichero de audio y luego darle a 'Procesar AUDIO'")

        else:
            st.write("Procesando audio...")      

            # Obtener IP del cliente si está disponible
            client_ip = st.context.ip_address  # solo disponible en v1.45.0+
            if client_ip:
                access_time = datetime.now().strftime("%Y-%m-%d > %H:%M:%S")
                #st.write(f"Acceso desde IP local: {client_ip} a las {access_time}")
                with open("/home/robot/Python/x_log/streamlit_ip.log", "a") as f:
                    f.write(f"{access_time} > {client_ip} > Pag2 > IA_Transcripcion_Audio (new) >> REUNION_1_audio_{timestamp}{extension} \n")

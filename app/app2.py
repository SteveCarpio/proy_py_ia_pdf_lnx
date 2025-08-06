import streamlit as st

def main():
    import streamlit as st
    from io import BytesIO # Importación de BytesIO para manejar archivos en memoria
    import tempfile # Importación de la librería temporal para crear directorios temporales
    import os  # Importación de la librería para operaciones de sistema (manejo de archivos y directorios)
    import json  # Importación de la librería para trabajar con datos en formato JSON
    from vosk import Model, KaldiRecognizer  # Importación de las clases necesarias para el reconocimiento de voz
    import wave  # Librería para trabajar con archivos WAV
    from pydub import AudioSegment  # Librería para convertir y manipular audios
    import requests  # Librería para realizar solicitudes HTTP
    import re  # Importación de la librería para expresiones regulares
    import ollama # Importación de la librería Ollama para interactuar con modelos de IA
    import shutil # Importación de la librería para copiar archivos y directorios
    from datetime import datetime # Importación de la clase datetime para manejar fechas y horas

    # Configuración de la librería pydub para usar ffmpeg
    AudioSegment.converter = "/usr/bin/ffmpeg"
    AudioSegment.ffprobe = "/usr/bin/ffprobe"

    ######################################################################################################################
    ### FUNCIONES VARIAS
    ######################################################################################################################

    ### Función: convert_to_wav ##########################################################################
    # Objetivo: Convertir cualquier archivo de audio a formato WAV con un solo canal y frecuencia de 16000
    def convert_to_wav(audio_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Cargar el archivo de audio y convertirlo a formato WAV con las configuraciones especificadas
        sound = AudioSegment.from_file(audio_path)
        sound = sound.set_channels(1).set_frame_rate(16000) # Configura el canal mono y la frecuencia de muestreo
        wav_path = f"temp_{timestamp}.wav"
        sound.export(wav_path, format="wav") # Exportar el audio convertido
        return wav_path

    ### Función: save_txt ###############################################
    # Objetivo: Guardar el texto transcrito en un archivo de texto (.txt)
    def save_txt(text, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(text) # Escribir el texto en el archivo especificado

    ### Función: transcribe ##############################################################
    # Objetivo: Transcribir el audio (en formato WAV) a texto utilizando el modelo de Vosk
    def transcribe(audio_path, model_path, timestamp):
        # Convertir el audio de entrada a formato WAV
        wav_path = convert_to_wav(audio_path)
        # Cargar el modelo preentrenado de Vosk

        model = Model(model_path)
        results = [] # Lista para almacenar las transcripciones

        # Abrir el archivo WAV y preparar el reconocimiento de voz
        with wave.open(wav_path, "rb") as wf:
            rec = KaldiRecognizer(model, wf.getframerate())
            while True:
                # Leer datos del archivo WAV en bloques de 4000 frames
                data = wf.readframes(4000)
                if len(data) == 0: # Si no hay más datos, salir del bucle
                    break
                if rec.AcceptWaveform(data): # Si el bloque de audio es aceptado por el reconocedor
                    # Solo texto puro
                    result_json = json.loads(rec.Result()) # Parsear la transcripción en formato JSON
                    results.append(result_json.get("text", "")) # Guardar el texto transcrito
            # Obtener el resultado final de la transcripción
            final_json = json.loads(rec.FinalResult())
            results.append(final_json.get("text", "")) # Guardar el texto final

        # Copiar y Eliminar el archivo temporal
        shutil.copy(wav_path, f'{ruta_salida}/REUNION_audio2_{timestamp}.wav')  # Copiar el archivo WAV a la ruta de salida
        os.remove(wav_path)
        
        # Unir todas las transcripciones y devolverlas como un único texto
        return "\n".join(results).strip() 

    ### Función: procesar_audio ################################################
    # Objetivo: Transcribir el audio y luego generar un resumen utilizando la IA
    def procesar_audio(audio_file, modelo_dir, base, timestamp):
        # Llamar a la función de transcripción para obtener el texto del audio
        texto = transcribe(audio_file, modelo_dir, timestamp)
        # Guardar el texto transcrito en un archivo .txt
        txt_path = f"{base}/REUNION_completo_{timestamp}.txt"
        save_txt(texto, txt_path)
        return texto, txt_path


    ### Función: resumir_ollama #########################################################################
    # Objetivo: Generar un resumen profesional de la reunión usando un modelo de IA (por ejemplo, Ollama)
    def resumir_ollama(texto, modelo_ollama, base, timestamp):
        prompt = (
            "A continuación tienes la transcripción de una reunión en español, posiblemente sin puntuación ni formato. "
            "Tu tarea es redactar un acta profesional de la reunión, respetando el idioma español.\n\n"
            "Por favor, sigue estas instrucciones:\n"
            "- Indica la fecha, hora y lugar de la reunión (si esos datos aparecen en el texto; si no, deja un espacio para completarlos).\n"
            "- Presenta una breve descripción de los participantes, indicando nombre completo y, si es posible, su empresa o rol.\n"
            "- Haz un listado breve y claro de los puntos tratados en la reunión.\n"
            "- Si quedan temas pendientes o para la próxima reunión, indícalos como 'Puntos pendientes'.\n"
            "- Mantén una redacción clara, profesional y estructurada.\n\n"
            f"Transcripción de la reunión:\n\n{texto}\n\n"
        )

        try:
            respuesta = ollama.chat(
                model=modelo_ollama,
                messages=[{"role": "user", "content": prompt}]
            )
            resumen = respuesta['message']['content'].strip()
        except Exception as e:
            raise RuntimeError(f"Error al generar el resumen con el modelo '{modelo_ollama}': {e}")

        resumen_filename = f"REUNION_resumen_{timestamp}.txt"  #  f"resumen_{timestamp}.txt"
        resumen_path = os.path.join(base, resumen_filename)

        try:
            os.makedirs(base, exist_ok=True)  # Asegura que el directorio exista
            with open(resumen_path, 'w', encoding='utf-8') as f:
                f.write(resumen)
        except Exception as e:
            raise IOError(f"No se pudo guardar el archivo de resumen en {resumen_path}: {e}")

        return resumen, resumen_path

    # Leer el archivo .txt para mostrarlo en la WEB
    @st.cache_data
    def load_markdown_file(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    ######################################################################################################################
    ### INICIO DEL PROGRAMA
    ######################################################################################################################

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

    # Procesar archivos subidos
    folder = "/home/robot/Python/x_audios"
    if uploaded_files:      
        st.sidebar.success(f"✅ Se subio correctamente")
        folder = UPLOAD_FOLDER  # Usar la carpeta de subidas para procesamiento
        # Visualizar el reproductor del audio para escuchar el audio 
        file_path = os.path.join("/tmp/transcripcion_audio/", uploaded_files.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_files.getbuffer())
        st.audio(uploaded_files, format=uploaded_files.type.split("/")[-1])
        

    ############## BOTÓN: para procesar AUDIO ##############
    if st.sidebar.button("Procesar AUDIO"):
        
        if uploaded_files is None:
            st.write("")
            st.write(" ℹ️ Debe seleccionar un fichero de audio y luego darle a 'Procesar AUDIO'")

        else:
            ############## INICIO DEL PROCESAMIENTO ##############

            # Si se sube el archivo a la carpeta temporal de Linux
            if uploaded_files is not None:
                extension = os.path.splitext(uploaded_files.name)[1]
                os.rename(file_path, file_path.replace(uploaded_files.name, f'REUNION_audio1_{timestamp}{extension}'))

            # Obtener IP del cliente si está disponible
            client_ip = st.context.ip_address  # solo disponible en v1.45.0+
            if client_ip:
                access_time = datetime.now().strftime("%Y-%m-%d > %H:%M:%S")
                with open("/home/robot/Python/x_log/streamlit_ip.log", "a") as f:
                    f.write(f"{access_time} > {client_ip} > Pag2 > IA_Transcripcion_Audio (new) >> REUNION_audio1_{timestamp}{extension} \n")

            audio_file = f"/tmp/transcripcion_audio/REUNION_audio1_{timestamp}{extension}"
            modelo_dir  = "/opt/models/vosk/vosk-model-es-0.42"    
            modelo_ollama = "llama3:instruct"                                        #  [ llama3:instruct | mistral ]
            ruta_salida = "/tmp/transcripcion_audio"
            base = ruta_salida
            
            # Función Procesar Audio
            texto, txt_path = procesar_audio(audio_file, modelo_dir, base, timestamp)  
            
            # Función Crea Resumen Modelo IA
            resumen, resumen_path = resumir_ollama(texto, modelo_ollama, base, timestamp)
            
            st.caption("📝 Resumen de la transcripción revisada por ChatTdA:")

            # Mostrar el texto2 transcrito en la WEB
            file_path2 = f"/tmp/transcripcion_audio/REUNION_resumen_{timestamp}.txt"  
            markdown_content = load_markdown_file(file_path2)
            st.markdown(markdown_content, unsafe_allow_html=False)

            st.markdown("---")

            st.caption("📝 Transcripción completa del audio:")

            # Mostrar el texto1 transcrito en la WEB
            file_path1 = f"/tmp/transcripcion_audio/REUNION_completo_{timestamp}.txt"  
            markdown_content = load_markdown_file(file_path1)
            st.markdown(markdown_content, unsafe_allow_html=False)

            st.markdown("---")

            st.write("Audio procesado y transcrito correctamente.")

    
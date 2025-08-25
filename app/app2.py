import gc
import os  # Importación de la librería para operaciones de sistema (manejo de archivos y directorios)
import re  # Importación de la librería para expresiones regulares
import json  # Importación de la librería para trabajar con datos en formato JSON
import wave  # Librería para trabajar con archivos WAV
import time  # Importación de la librería para manejar el tiempo
import torch
import ollama # Importación de la librería Ollama para interactuar con modelos de IA
import shutil # Importación de la librería para copiar archivos y directorios
import whisper # Importación del modelo Whisper de OpenIA
import tempfile # Importación de la librería temporal para crear directorios temporales
import requests  # Librería para realizar solicitudes HTTP
import streamlit as st
from io import BytesIO # Importación de BytesIO para manejar archivos en memoria
from datetime import datetime # Importación de la clase datetime para manejar fechas y horas
from pydub import AudioSegment  # Librería para convertir y manipular audios
from vosk import Model, KaldiRecognizer  # Importación de las clases necesarias para el reconocimiento de voz


@st.cache_resource
def cargar_modelo_whisper(nombre_modelo="medium"):
    return whisper.load_model(nombre_modelo, device="cuda")

def liberar_memoria():
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()

def main():

    ######################################################################################################################
    ### FUNCIONES VARIAS
    ######################################################################################################################

    ### Función: convert_to_wav ##########################################################################
    # Objetivo: Convertir cualquier archivo de audio a formato WAV con un solo canal y frecuencia de 16000      <-----:::  STV NO SE USA
    def convert_to_wav(audio_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Cargar el archivo de audio y convertirlo a formato WAV con las configuraciones especificadas
        sound = AudioSegment.from_file(audio_path)
        sound = sound.set_channels(1).set_frame_rate(16000) # Configura el canal mono y la frecuencia de muestreo
        wav_path = f"temp_{timestamp}.wav"
        sound.export(wav_path, format="wav") # Exportar el audio convertido
        return wav_path

    ### Función: transcribe ##############################################################
    # Objetivo: Transcribir el audio (en formato WAV) a texto utilizando el modelo de Vosk                      <-----:::  STV NO SE USA
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
        shutil.copy(wav_path, f'{ruta_salida}/Audio_{timestamp}_convertido.wav')  # Copiar el archivo WAV a la ruta de salida
        os.remove(wav_path)
        
        # Unir todas las transcripciones y devolverlas como un único texto
        return "\n".join(results).strip() 

    ### Función: procesar_audio VOSK ################################################
    # Objetivo: Transcribir el audio y luego generar un resumen utilizando la IA                         <-----:::  STV NO SE USA
    def procesar_audio1(audio_file, modelo_dir, base, timestamp):
        # Llamar a la función de transcripción para obtener el texto del audio
        texto = transcribe(audio_file, modelo_dir, timestamp)
        # Guardar el texto transcrito en un archivo .txt
        txt_path = f"{base}/Audio_{timestamp}_texto_completo.txt"
        save_txt(texto, txt_path)
        return texto, txt_path

    ### Función: procesar_audio WHISPER ################################################
    # Objetivo: Transcribir el audio y luego generar un resumen utilizando la IA
    def procesar_audio2(audio_file, modelo_dir, base, timestamp):
        model = cargar_modelo_whisper(modelo_dir)
        # Transcribir Audio con Whisper
        result = model.transcribe(audio_file)
        texto = result["text"]
        # Guardar el texto transcrito en un archivo .txt
        txt_path = f"{base}/Audio_{timestamp}_texto_completo.txt"
        save_txt(texto, txt_path)
        return texto, txt_path

    ### Función: save_txt ###############################################
    # Objetivo: Guardar el texto transcrito en un archivo de texto (.txt)
    def save_txt(text, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(text) # Escribir el texto en el archivo especificado

    ### Función: resumir_ollama #########################################################################
    # Objetivo: Generar un resumen profesional de la reunión usando un modelo de IA (por ejemplo, Ollama)
    def resumir_ollama(texto, modelo_ollama, base, timestamp, seleccion):

        if seleccion == "Reunión":
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

        if seleccion == "Conversación":
            prompt = (
                "A continuación tienes la transcripción de una conversación, posiblemente sin puntuación ni formato adecuado.\n\n"
                "Tu tarea es:\n"
                "1. Redactar un resumen claro y profesional del contenido de la conversación.\n"
                "2. Si la conversación no está en español, debes traducirla al español antes de hacer el resumen.\n"
                "3. Al final, incluye la transcripción completa de la conversación, aplicando saltos de línea adecuados y puntuación básica para mejorar la legibilidad.\n\n"
                "Toda la respuesta debe tener una estructura clara, profesional y bien organizada.\n\n"
                f"Transcripción de la conversación:\n\n{texto}\n"
            )

        if seleccion == "Poema":
            prompt = (
                "A continuación tienes la transcripción de un poema, posiblemente sin puntuación, sin formato adecuado y en un idioma distinto al español.\n\n"
                "Tu tarea es:\n"
                "1. Detectar el idioma original del poema.\n"
                "2. Intentar identificar al autor del poema y nombre del poema, etc en modo tabla (si es posible).\n"
                "3. Redactar un breve resumen o interpretación del poema.\n"
                "4. Reconstruir el poema en español aplicando saltos de línea los puntos y aparte y corregir los errores gramaticales.\n"
                "Toda la respuesta debe tener una estructura clara, profesional y bien organizada.\n\n"
                f"Transcripción del poema:\n\n{texto}\n"
            )

        if seleccion == "Canción":
            prompt = (
                "A continuación tienes la transcripción de una canción, posiblemente sin puntuación, sin formato adecuado y en un idioma distinto al español.\n\n"
                "Tu tarea es:\n"
                "1. Detectar el idioma original de la canción.\n"
                "2. Intentar dar detalles del autor, nombre del disco, nombre de la canción, fecha de lanzamiento, etc en modo tabla (si es posible).\n"
                "3. Redactar un breve resumen o interpretación de la letra de la canción.\n"
                "4. Reconstruir la canción en español aplicando saltos de línea los puntos y aparte y corregir posibles errores gramaticales.\n"
                "Toda la respuesta debe tener una estructura clara, profesional y bien organizada.\n\n"
                f"Transcripción del poema:\n\n{texto}\n"
            )


        try:
            respuesta = ollama.chat(
                model=modelo_ollama,
                messages=[{"role": "user", "content": prompt}]
            )
            resumen = respuesta['message']['content'].strip()
        except Exception as e:
            raise RuntimeError(f"Error al generar el resumen con el modelo '{modelo_ollama}': {e}")

        resumen_filename = f"Audio_{timestamp}_texto_resumen.txt"  #  f"resumen_{timestamp}.txt"
        resumen_path = os.path.join(base, resumen_filename)

        try:
            os.makedirs(base, exist_ok=True)  # Asegura que el directorio exista
            with open(resumen_path, 'w', encoding='utf-8') as f:
                f.write(resumen)
        except Exception as e:
            raise IOError(f"No se pudo guardar el archivo de resumen en {resumen_path}: {e}")
        
        respuesta = None

        return resumen, resumen_path

    # Leer el archivo .txt para mostrarlo en la WEB
    @st.cache_data
    def load_markdown_file(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    ######################################################################################################################
    ### INICIO DEL PROGRAMA
    ######################################################################################################################

    # Configuración de la librería pydub para usar ffmpeg
    AudioSegment.converter = "/usr/bin/ffmpeg"
    AudioSegment.ffprobe = "/usr/bin/ffprobe"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Configuración inicial de la app
    #st.set_page_config("(TDA) Lector de Facturas IA", layout="wide")
    st.title("🤖 Transcripción de Audio")  # 🗂️ 📄  🤖
    st.caption("Combina ASR (Reconocimiento Automático de Voz) con modelos LLM para transformar audio en texto estructurado y resúmenes contextuales.")

    # Mostrar markdown previamente cargado
    if "markdown1_app2" in st.session_state:
        st.success("Mostrando resumen con IA previamente generado:")
        st.markdown(st.session_state["markdown1_app2"], unsafe_allow_html=False)
    if "markdown2_app2" in st.session_state:
        st.success("Mostrando resumen Original previamente generado:")
        st.markdown(st.session_state["markdown2_app2"], unsafe_allow_html=False)
        st.markdown("---")

    # Crear directorio temporal para subidas
    UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), "transcripcion_audio")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    st.sidebar.markdown("---")  # Separador

    # ---[ BOTON: Browse Files ]--- #
    uploaded_files = st.sidebar.file_uploader(
        label="📁 Seleccione Archivo AUDIO  ",  
        type=["mp3", "wav", "ogg"],
        accept_multiple_files=False,
        label_visibility="visible" 
    )

    # Carpeta por defecto
    folder = "/home/robot/Python/x_audios"

    if uploaded_files:      
        st.sidebar.success(f"✅ Se subio correctamente")
        folder = UPLOAD_FOLDER  # Usar la carpeta de subidas para procesamiento

        # Visualizar el reproductor del audio en la web para escuchar el audio 
        file_path = os.path.join("/tmp/transcripcion_audio/", uploaded_files.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_files.getbuffer())
        st.audio(uploaded_files, format=uploaded_files.type.split("/")[-1])
        
    # ---[SELECTBOX: Tipo de Audio ]--- #
    opciones = ["Reunión", "Conversación", "Canción", "Poema", "Otros"]  # lista de opciones
    seleccion = st.sidebar.selectbox(
        "Indique el tipo del audio:",
        opciones,
        index=0,               # índice por defecto (0 = primera opción)
        key="opcion_elegida"   # clave opcional para mantener estado
    )

 
    

    # ---[ BOTÓN: Procesar AUDIO ]--- #
    if st.sidebar.button("Procesar AUDIO"):

        if uploaded_files is None:
            st.write("")
            st.write(" ℹ️ Debe seleccionar un fichero de audio y luego darle a 'Procesar AUDIO'")

        else:
            ############## INICIO DEL PROCESAMIENTO ##############

            access_inicio = datetime.now().strftime("%H:%M:%S")

            with st.spinner(f'Analizando Audio de Tipo ({seleccion}): Por favor espere...'):

                nombre_audio = f'Audio_{timestamp}'

                # Si se sube el archivo a la carpeta temporal de Linux
                if uploaded_files is not None:
                    extension = os.path.splitext(uploaded_files.name)[1]
                    os.rename(file_path, file_path.replace(uploaded_files.name, f'{nombre_audio}_original{extension}'))

                audio_file      = f"/tmp/transcripcion_audio/{nombre_audio}_original{extension}"
                modelo_vosk     = "/opt/models/vosk/vosk-model-es-0.42"    #  [ vosk-model-es-0.42  |  ]
                modelo_whisper  = "medium"                                 #  [ medium  |  large ]
                modelo_ollama   = "llama3:instruct"                        #  [ llama3:instruct  |  mistral:latest  |  gpt-oss:20b  |  deepseek-r1:32b | mixtral:latest ]
                ruta_salida     = "/tmp/transcripcion_audio"
                base            = ruta_salida
                
                # Función Procesar Audio (usa el modelo VOSK)
                #texto, txt_path = procesar_audio1(audio_file, modelo_vosk, base, timestamp)  

                # Función Procesar Audio (usa el modelo WHISPER)
                texto, txt_path = procesar_audio2(audio_file, modelo_whisper, base, timestamp)  

                # Función Crea Resumen Modelo IA
                resumen, resumen_path = resumir_ollama(texto, modelo_ollama, base, timestamp, seleccion)
                
                st.caption("📝 Resumen de la transcripción revisada por ChatTdA:")

                # Mostrar el texto2 transcrito en la WEB
                file_path2 = f"/tmp/transcripcion_audio/Audio_{timestamp}_texto_resumen.txt"  
                markdown_content = load_markdown_file(file_path2)
                # Guardar contenido en session_state para persistencia
                st.session_state["markdown1_app2"] = markdown_content
                st.markdown(markdown_content, unsafe_allow_html=False)

                st.markdown("---")

                st.caption("📝 Transcripción original del audio sin IA:")

                # Mostrar el texto1 transcrito en la WEB
                file_path1 = f"/tmp/transcripcion_audio/Audio_{timestamp}_texto_completo.txt"  
                markdown_content = load_markdown_file(file_path1)
                # Guardar contenido en session_state para persistencia
                st.session_state["markdown2_app2"] = markdown_content
                #st.markdown(markdown_content, unsafe_allow_html=False)
                st.caption(markdown_content, unsafe_allow_html=False)

                st.markdown("---")

                # Obtener IP del cliente si está disponible
                client_ip = st.context.ip_address  # solo disponible en v1.45.0+
                if client_ip:
                    access_time = datetime.now().strftime(f"%Y-%m-%d > {access_inicio} > %H:%M:%S")
                    with open("/home/robot/Python/x_log/streamlit_ip.log", "a") as f:
                        f.write(f"{access_time} > {client_ip} > Pag2 > IA_Transcripcion_Audio({seleccion}) >> /tmp/transcripcion_audio/{nombre_audio}_* \n")


            st.success(f"¡ Audio procesado y transcrito correctamente ! : {access_time}")

            # Limpiar archivos subidos después del procesamiento
            del texto, resumen
            liberar_memoria()
            st.info("🧹 Memoria liberada después del procesamiento.")

    

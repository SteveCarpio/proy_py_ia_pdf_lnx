######################################################################################################################
# source .\venv\Scripts\activate
# sudo apt update && sudo apt install ffmpeg -y   
# pip install pydub
# pip install vosk 
# pip install ffmpeg-python
# pip install requests
# pip freeze > requirements.txt
# https://alphacephei.com/vosk/models   # -- descargar el modelos  (por ejemplo “vosk-model-small-es-0.42”).
# Descomprime el archivo ZIP y copiar la carpeta en una ruta y ponerlo en el programa
######################################################################################################################

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

######################################################################################################################
# Funciones Varias
######################################################################################################################

### Función: convert_to_wav ##########################################################################################
# Objetivo: Convertir cualquier archivo de audio a formato WAV con un solo canal y frecuencia de 16000
def convert_to_wav(audio_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Cargar el archivo de audio y convertirlo a formato WAV con las configuraciones especificadas
    sound = AudioSegment.from_file(audio_path)
    sound = sound.set_channels(1).set_frame_rate(16000) # Configura el canal mono y la frecuencia de muestreo
    wav_path = f"temp_{timestamp}.wav"
    sound.export(wav_path, format="wav") # Exportar el audio convertido
    return wav_path

### Función: save_txt ################################################################################################
# Objetivo: Guardar el texto transcrito en un archivo de texto (.txt)
def save_txt(text, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text) # Escribir el texto en el archivo especificado

### Función: transcribe ############################################################################################## 
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

    # Eliminar el archivo WAV temporal
    shutil.copy(wav_path, f'{ruta_salida}/REUNION_audio_{timestamp}.wav')  # Copiar el archivo WAV a la ruta de salida
    os.remove(wav_path)
    
    # Unir todas las transcripciones y devolverlas como un único texto
    return "\n".join(results).strip() 

### Función: procesar_audio ##########################################################################################
# Objetivo: Transcribir el audio y luego generar un resumen utilizando la IA
def procesar_audio(audio_file, modelo_dir, base, timestamp):
    # Llamar a la función de transcripción para obtener el texto del audio
    texto = transcribe(audio_file, modelo_dir, timestamp)
    # Guardar el texto transcrito en un archivo .txt
    txt_path = f"{base}/REUNION_completo_{timestamp}.txt"
    save_txt(texto, txt_path)
    return texto, txt_path


### Función: resumir_ollama ##########################################################################################
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

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    resumen_filename = f"REUNION_resumen_{timestamp}.txt"  #  f"resumen_{timestamp}.txt"
    resumen_path = os.path.join(base, resumen_filename)

    try:
        os.makedirs(base, exist_ok=True)  # Asegura que el directorio exista
        with open(resumen_path, 'w', encoding='utf-8') as f:
            f.write(resumen)
    except Exception as e:
        raise IOError(f"No se pudo guardar el archivo de resumen en {resumen_path}: {e}")

    return resumen, resumen_path


######################################################################################################################
#                                              Inicio del Programa                                                   #
######################################################################################################################

if __name__ == "__main__":

    audio_file = "/home/robot/Python/x_audios/REUNION.mp3"
    modelo_dir  = "/opt/models/vosk/vosk-model-es-0.42"    
    modelo_ollama = "llama3:instruct"                                        #  [ llama3:instruct | mistral ]
    ruta_salida = "/tmp/transcripcion_audio"
    base = ruta_salida
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Función Procesar Audio
    texto, txt_path = procesar_audio(audio_file, modelo_dir, base, timestamp)  
    print(f"\n - Transcripción guardada en: {txt_path}")
    print(f"\n{texto}")

    # Función Crea Resumen Modelo IA
    resumen, resumen_path = resumir_ollama(texto, modelo_ollama, base, timestamp)
    print(f"\n\n - Resumen guardado en: {resumen_path}")
    print(f"\n{resumen}\n")
    
 
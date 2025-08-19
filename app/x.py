import whisper

# Cargar el modelo ( medium - large (este no va muy bien))
model = whisper.load_model("medium")
# Ruta al archivo de audio a transcribir
audio_path = "/tmp/transcripcion_audio/Audio_20250819_141504_original.mp3"
# Transcribir Audio con Whisper
result = model.transcribe(audio_path)
# print(f"Idioma detectado: {result['language']}")
# print("\nTexto transcrito:")
#print(result["text"])
    
 
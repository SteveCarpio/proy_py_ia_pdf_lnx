import streamlit as st
import time
import ollama
from pathlib import Path

def main():
    # Configuración de la página
    #st.set_page_config(
    #    page_title="Chat con Modelos Locales",
    #    page_icon="🤖",
    #    layout="wide"
    #)

    # Inicializar historial de chat si no existe
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Inicializar contador de chats si no existe
    if "chat_counter" not in st.session_state:
        st.session_state.chat_counter = 1
    
    # Sidebar para configuración
    with st.sidebar:
        st.markdown("---")
        
        # Botón para nuevo chat
        if st.button("Transcribir"):
            st.session_state.messages = []
            st.session_state.chat_counter += 1
            st.rerun()
        
        #st.markdown("---")
        
        # Formato de Salida
        model_choice = st.selectbox(
            "Selecciona el formato de salida:",
            ["PDF", "DOC", "TXT"],
            index=0,
            help="Formatos disponibles (en continuo desarrollo)."
        )
        
        #st.markdown("---")
        st.markdown("""
        **📝 Instrucciones:**
        1. Selecciona el formato de salida
        2. Presiona 'Transcribir'
        """)
        
        # Mostrar información del modelo seleccionado
        st.markdown(f"**Formato Seleccionado:** `{model_choice}`")
    

    # Área principal del chat
    st.title(f"🤖 Transcrición de Audio a ({model_choice})")
    st.caption("Combina ASR (Reconocimiento Automático de Voz) con modelos LLM para transformar audio en texto estructurado y resúmenes contextuales.")
    st.text("🚧 .... En Construcción .... 🚧 ")


if __name__ == "__main__":
    main()

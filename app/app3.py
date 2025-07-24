import streamlit as st
import time
import ollama
from pathlib import Path

def main():
    # Configuración de la página
    # st.set_page_config(
    #    page_title="Chat con Modelos Locales",
    #    page_icon="🤖",
    #    layout="wide"
    # )

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
        if st.button("🆕 Nuevo chat"):
            st.session_state.messages = []
            st.session_state.chat_counter += 1
            st.rerun()
        
        #st.markdown("---")
        
        # Selector de modelo
        model_choice = st.selectbox(
            "🧠 Selecciona el modelo:",
            ["llama3:instruct", "mistral:latest"],   # "mixtral:lastest"
            index=0,
            help="Modelos disponibles localmente (en continuo desarrollo)."
        )
        
        #st.markdown("---")
        st.markdown("""
        **📝 Instrucciones:**
        1. Selecciona el modelo
        2. Escribe tu pregunta/prompt
        3. Presiona 'Enviar'
        """)
        
        # Mostrar información del modelo seleccionado
        st.markdown(f"**Modelo activo:** `{model_choice}`")
        st.markdown(f"**Chat actual:** #{st.session_state.chat_counter}")

    # Área principal del chat
    st.title(f"🤖 ChatTDA (Chat #{st.session_state.chat_counter})")
    st.caption("Nota: Se ejecutará usando un modelo pre-entrenado (en construcción), los datos no se almacenan en ningún servidor exterior/local.")

    # Mostrar historial de chat existente
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada de usuario
    if prompt := st.chat_input("Escribe tu pregunta aquí..."):
        # Mostrar mensaje del usuario
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Añadir al historial
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Mostrar respuesta del asistente
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Generar respuesta
            start_time = time.time()
            
            try:
                # Stream de respuesta desde Ollama usando TODO el historial
                response = ollama.chat(
                    model=model_choice,
                    messages=st.session_state.messages,  # Envía todo el historial
                    stream=True
                )
                
                # Mostrar respuesta en tiempo real
                for chunk in response:
                    chunk_content = chunk.get('message', {}).get('content', '')
                    full_response += chunk_content
                    message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                
                # Mostrar estadísticas
                end_time = time.time()
                st.caption(f"Tiempo de respuesta: {end_time - start_time:.2f} segundos")
                
                # Añadir al historial
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"Error al generar respuesta: {str(e)}")
                st.session_state.messages.append({"role": "assistant", "content": f"Error: {str(e)}"})

if __name__ == "__main__":
    main()

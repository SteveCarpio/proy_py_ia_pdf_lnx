import streamlit as st
import time
import ollama
from pathlib import Path

def main():
    # Configuración de la página (debe ser lo primero en Streamlit)
    #st.set_page_config(
    #    page_title="Chat con Modelos Locales",
    #    page_icon="🤖",
    #    layout="wide"
    #)

    # Sidebar para configuración
    with st.sidebar:
        st.markdown("---")  # Separador

        #st.title("Configuración del Modelo") #  ⚙️
        
        # Selector de modelo
        model_choice = st.selectbox(
            "🧠 Selecciona el modelo:",
            ["llama3:instruct", "mistral:latest", "mixtral:latest"],
            index=0,
            help="Modelos disponibles localmente (en continuo desarrollo)."
        )
        
        st.markdown("---")
        st.markdown("""
        **📝 Instrucciones:**
        1. Selecciona el modelo
        2. Escribe tu pregunta/prompt
        3. Presiona 'Enviar'
        """)
        
        # Mostrar información del modelo seleccionado
        st.markdown(f"**Modelo activo:** `{model_choice}`")

    # Área principal del chat
    st.title("🤖 ChatTDA Local rev. 2023")
    st.caption("Nota: Se ejecutará usando un modelo pre-entrenado (en construcción), los datos no se almacenan en ningún servidor exterior/local.")

    # Inicializar historial de chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

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
                # Stream de respuesta desde Ollama
                response = ollama.chat(
                    model=model_choice,
                    messages=[{"role": "user", "content": prompt}],
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

#if __name__ == "__main__":
#    main()
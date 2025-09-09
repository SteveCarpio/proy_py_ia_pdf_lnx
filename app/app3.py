import streamlit as st
import time
import ollama
from pathlib import Path
from datetime import datetime

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
            ["llama3:instruct", "mistral:latest" ],     #   "gpt-oss:20b", "mixtral:latest" , "deepseek-r1:32b"
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
    st.caption(f"La ejecución se realizará utilizando el modelo previamente entrenado {model_choice}. Cualquier dato ingresado durante el proceso no será almacenado en ningún servidor o base de datos.")

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

                # Obtener IP del cliente si está disponible
                client_ip = st.context.ip_address  # solo disponible en v1.45.0+
                if client_ip:
                    access_time = datetime.now().strftime("%Y-%m-%d > %H:%M:%S")
                    #st.write(f"Acceso desde IP local: {client_ip} a las {access_time}")
                    with open("/home/robot/Python/x_log/streamlit_ip.log", "a") as f:
                        f.write(f"{access_time} > {client_ip} > Pag3 > IA_ChatTDA({model_choice}) >> {prompt}\n")

            except Exception as e:
                st.error(f"Error al generar respuesta: {str(e)}")
                st.session_state.messages.append({"role": "assistant", "content": f"Error: {str(e)}"})

    

if __name__ == "__main__":
    main()

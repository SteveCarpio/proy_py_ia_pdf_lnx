import streamlit as st
from llama_cpp import Llama
import os
import time

def main():
    # Configuración del sidebar específico de esta app
    with st.sidebar:
        st.title("Configuración de App 2")
        param1 = st.slider("Parámetro 1", 0, 100, 50)
        param2 = st.selectbox("Parámetro 2", ["Opción A", "Opción B", "Opción C"])
    
    # Contenido principal de la app
    st.title("Aplicación 2")
    st.write(f"""
    Esta es la aplicación 2 con los siguientes parámetros:
    - Parámetro 1: {param1}
    - Parámetro 2: {param2}
    """)
    
    # Más contenido de tu app aquí...

def main2():
    # Configuración del sidebar específico de esta app
    with st.sidebar:
        st.title("Configuración de App 2")
        
    # Contenido principal de la app
    st.title("Aplicación 2")
    st.write(f"""
    Esta es la aplicación 2 con los siguientes parámetros:
    - Parámetro 1: 
    - Parámetro 2: 
    """)
    
    # Más contenido de tu app aquí...

    

    # Configuración de la página
    st.set_page_config(page_title="Modelos Locales", layout="wide")

    # Título de la aplicación
    st.title("🤖 Chat con Modelos Locales")

    # Sidebar para configuración
    with st.sidebar:
        st.header("⚙️ Configuración")
        model_choice = st.selectbox("Selecciona el modelo:", ["Llama3", "Mistral"])
        
        st.markdown("---")
        st.markdown("""
        **📝 Instrucciones:**
        1. Selecciona el modelo
        2. Escribe tu pregunta/prompt
        3. Presiona 'Enviar'
        """)

    # Cargar el modelo seleccionado
    @st.cache_resource
    def load_model(model_name):
        model_path = ""
        if model_name == "Llama3":
            model_path = "/ruta/a/tu/modelo/llama3.gguf"  # Cambiar por tu ruta real
        elif model_name == "Mistral":
            model_path = "/ruta/a/tu/modelo/mistral.gguf"  # Cambiar por tu ruta real
        
        if not os.path.exists(model_path):
            st.error(f"Modelo no encontrado en: {model_path}")
            return None
        
        return Llama(
            model_path=model_path,
            n_ctx=2048,  # Ajustar según tu hardware
            n_threads=4,  # Ajustar según tus núcleos de CPU
        )

    # Inicializar el modelo
    llm = load_model(model_choice)

    # Historial de chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar historial de chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if "content" in message:
                st.markdown(message["content"])

    # Entrada de usuario
    if prompt := st.chat_input("Escribe tu pregunta aquí..."):
        # Mostrar mensaje del usuario
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Añadir al historial
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        if llm is not None:
            # Mostrar respuesta del modelo
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                # Generar respuesta
                start_time = time.time()
                response = llm.create_chat_completion(
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1024,
                    temperature=0.7,
                    stream=True
                )
                
                # Mostrar respuesta en tiempo real
                for chunk in response:
                    chunk_content = chunk['choices'][0]['delta'].get('content', '')
                    full_response += chunk_content
                    message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                
                # Mostrar estadísticas
                end_time = time.time()
                st.caption(f"Tiempo de respuesta: {end_time - start_time:.2f} segundos")
            
            # Añadir al historial
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        else:
            st.error("Modelo no cargado correctamente. Verifica las rutas en la configuración.")

    # Notas al pie
    st.markdown("---")
    st.caption("Nota: Los modelos se ejecutan localmente en tu servidor Ubuntu.")
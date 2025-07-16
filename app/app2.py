import streamlit as st

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
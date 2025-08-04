import streamlit as st
from datetime import datetime
from app import app1, app2, app3  # Importa tus apps aquí

# Configuración de la página
st.set_page_config(
    page_title="Portal IA (TdA)",
    page_icon="💼",  # 💼  🏛️
    layout="wide"
)

# Diccionario de aplicaciones disponibles
APPS = {
    "Inicio": None,
    "IA: Facturas PDF": app1,
    "IA: Transcripción de Audio": app2,
    "IA: ChatTDA": app3
}

def main():
    # Sidebar para selección de aplicación
    st.sidebar.title("Selecciona una App")
    app_selection = st.sidebar.radio("Ir a:", list(APPS.keys()))
    
    # Página de inicio
    if app_selection == "Inicio":
        st.title("Listado de Aplicaciones")
        st.write("""
        Selecciona una aplicación desde el menú lateral para comenzar.
        """)
        
        # Mostrar miniaturas de las apps disponibles
        cols = st.columns(3)
        with cols[0]:
            st.subheader("Facturas PDF")
            st.write("Seleccione facturas en formato PDF y serán procesadas por la IA para extraer los datos más relevantes.")
                
        with cols[1]:
            st.subheader("Transcripción de Audio")
            st.write("Seleccione un fichero de audio y la IA lo transcribirá a texto y crerá un resumen.")
                
        with cols[2]:
            st.subheader("Chat de Texto")
            st.write("Escribe un mensaje y la IA responderá de forma inteligente.")
            
        with st.sidebar:

            st.markdown("---")  # Separador

            # Mensaje de ayuda
            st.markdown("""
            **🆘 Ayuda:**
            1. Selecciona una App (están todas en fase de contrucción).
            2. Tu explorador debe tener libre el puerto **8501**
            3. Cualquier duda contactar con: Steve Carpio (TdA)
            """)
            
            st.markdown("---")  # Separador
            
            # Mensaje informativo
            st.markdown("""
            **ℹ️ Información:**
            - IA TdA, se usan modelos preentrenados para extracción de datos.
            - Soporta ficheros escaneadas (usará OCR)
            - Formato europeo: 1.234,56
            """)
            
            st.markdown("---")  # Separador
            
            # Copyright con año actual
            current_year = datetime.now().year
            st.markdown(f"""
            **© {current_year} - TdA S.A.**
            - Versión 2.0
            - Todos los derechos reservados
            """)

        # Obtener IP del cliente si está disponible
        client_ip = st.context.ip_address  # solo disponible en v1.45.0+
        if client_ip:
            access_time = datetime.now().strftime("%Y-%m-%d > %H:%M:%S")
            #st.write(f"Acceso desde IP local: {client_ip} a las {access_time}")
            with open("/home/robot/Python/x_log/streamlit_ip.log", "a") as f:
                f.write(f"{access_time} > {client_ip} > {app_selection}\n")

    # Cargar la aplicación seleccionada
    else:
        APPS[app_selection].main()

    

if __name__ == "__main__":
    main()
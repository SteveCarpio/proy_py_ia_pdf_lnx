# source venv/bin/activate

import streamlit as st
import base64
from datetime import datetime
from PIL import Image
from app import app1, app2, app3  # Importa tus apps aquí
import gc

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
    
    st.sidebar.title("Selecciona una App")
    app_selection = st.sidebar.radio("Ir a:", list(APPS.keys()))

    #if st.sidebar.button('🔄 Liberar Memoria'):
    #    st.sidebar.success("✅ Memoria liberada manualmente")
    #    gc.collect()
    
    # Página de inicio
    if app_selection == "Inicio":
        
        # Crear dos columnas (una más ancha para el título)
        col1, col2 = st.columns([4, 1])
        with col1:
            st.title("Listado de Aplicaciones")
            st.caption("Selecciona una aplicación desde el menú lateral para comenzar.")

        with col2:
            logo = Image.open("img/logotipo.gif")
            st.image(logo)  # Más pequeño para que quede al lado
          
        # Mostrar miniaturas de las apps disponibles
        cols = st.columns(3)
        with cols[0]:
            st.subheader("Facturas PDF")
            st.markdown(
            """
            <style> .small-text1 {font-size: 0.5em;color: #8B0000; text-align: left;} </style>
            <p class="small-text1">Seleccione facturas en formato PDF y serán procesadas por la IA para extraer los datos más relevantes.</p>
            """, unsafe_allow_html=True)

            st.subheader("Otros 1")
            st.write("Aquí puede ir una de tus propuestas de aplicación IA.")

            st.subheader("Otros 4")
            st.markdown(
            """
            <style> .small-text1 {font-size: 0.5em;color: #8B0000; text-align: left;} </style>
            <p class="small-text1">Aquí puede ir una de tus propuestas de aplicación IA.</p>
            """, unsafe_allow_html=True)
                
        with cols[1]:
            st.subheader("Transcripción de Audio")
            st.write("Seleccione un fichero de audio y la IA lo transcribirá a texto y creará un resumen en formato Word.")

            st.subheader("Otros 2")
            st.markdown(
            """
            <style> .small-text1 {font-size: 0.5em;color: #8B0000; text-align: left;} </style>
            <p class="small-text1">Aquí puede ir una de tus propuestas de aplicación IA.</p>
            """, unsafe_allow_html=True)
                
        with cols[2]:
            st.subheader("ChatTDA")
            st.markdown(
            """
            <style> .small-text1 {font-size: 0.5em;color: #8B0000; text-align: left;} </style>
            <p class="small-text1">Escribe un mensaje y la IA responderá de forma inteligente usando modelos pre-entrenados (en continuo aprendizaje).</p>
            """, unsafe_allow_html=True)
            
            st.subheader("Otros 3")
            st.write("Aquí puede ir una de tus propuestas de aplicación IA.")
        
        st.caption(" ")
        st.caption(" ")
        st.caption(" ")
        st.caption(" ")
        st.markdown("---")  # Separador


        # Pie de página centrado y pequeño
        st.markdown(
            """
            <style>
            .small-text2 {
                font-size: 0.5em;
                color: gray;
                text-align: center;
            }
            </style>
            <p class="small-text2">Para más ayuda, contactar con carpios@tda-sgft.com <br> Versión 1.0.0</p>
            """,
            unsafe_allow_html=True
        )

        # Mostrar el logotipo centrado
        def get_image_base64(path):
            with open(path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        image_base64 = get_image_base64("img/logotipo.ico")
        st.markdown(
            """
            <div style='text-align: center;'>
                <img src='data:image/png;base64,{image_base64}' width='40'>
                <br>
            </div>
            """.format(image_base64=image_base64),
            unsafe_allow_html=True
        )


        # Sidebar con información adicional            
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
            """)

        # Obtener IP del cliente si está disponible
        client_ip = st.context.ip_address  # solo disponible en v1.45.0+
        if client_ip:
            access_time = datetime.now().strftime("%Y-%m-%d > %H:%M:%S > %H:%M:%S")
            #st.write(f"Acceso desde IP local: {client_ip} a las {access_time}")
            with open("/home/robot/Python/x_log/streamlit_ip.log", "a") as f:
                f.write(f"{access_time} > {client_ip} > Pag0 > Inicio\n")

    # Cargar la aplicación seleccionada
    else:
        APPS[app_selection].main()
        gc.collect()  # Limpia la memoria tras ejecutar una app

    

if __name__ == "__main__":
    main()

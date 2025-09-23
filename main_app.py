# source venv/bin/activate
# 🆕 💼 🏛️ 🆕 🗑️ 🟢 📦 📊 🏠 🤖 📈 🔬 🌐

import streamlit as st
import base64
from datetime import datetime
from PIL import Image
from app import app0, app1, app2, app3, app4, app5, app6
import gc

# Configuración
st.set_page_config(
    page_title="Portal Python (TdA)",
    page_icon="💼",
    layout="wide"
)

# Diccionario Inteligencia Artificial
IA_APPS = {
    "1 - Facturas PDF": app1,
    "2 - Transcripción de Audio": app2,
    "3 - ChatTdA": app3,
    "4 - SmartMail": app5,
    "5 - Prueba Steve": app6
}
# Diccionario Data Sciencie
DS_APPS = {
    "1 - Cuadrator": app4,
}
# Diccionario WebScraping
WS_APPS = {
    "1 - Eventos Relevantes": app0,
    "2 - Estados Financieros": app0
}
# Diccionario Reporting
RP_APPS = {
    "1 - Eventos Relevantes": app0,
    "2 - Estados Financieros": app0
}

def mostrar_inicio():

    # [ INTELIGENCIA ARTIFICIAL] ############################################################################################################
    col1, col2 = st.columns([4, 1])
    with col1:
        st.header("> Apps basados en IA: 🤖")
        #st.caption("Selecciona una aplicación desde el menú lateral para comenzar.")
    with col2:
        logo = Image.open("img/logotipo.gif")
        st.image(logo)

    cols = st.columns(3)
    with cols[0]:
        st.subheader("Facturas PDF ")
        st.markdown("""
        <style> .small-text1 {font-size: 0.5em;color: #8B0000;} </style>
        <p class="small-text1">IA que procesa facturas en PDF y extrae información.</p>
        """, unsafe_allow_html=True)

        st.subheader("SmartMail ")
        st.write("Analiza correos ZIMBRA con IA, resume y extrae datos clave.")

        st.subheader(" ")
        st.markdown("""
        <style> .small-text1 {font-size: 0.5em;color: #8B0000;} </style>
        <p class="small-text1">  </p>
        """, unsafe_allow_html=True)

    with cols[1]:
        st.subheader("Transcripción de Audio ")
        st.write("IA para convertir audio a texto con resumen automático.")

        st.subheader("  ")
        st.markdown("""
        <style> .small-text1 {font-size: 0.5em;color: #8B0000;} </style>
        <p class="small-text1"> </p>
        """, unsafe_allow_html=True)

    with cols[2]:
        st.subheader("ChatTDA ")
        st.markdown("""
        <style> .small-text1 {font-size: 0.5em;color: #8B0000;} </style>
        <p class="small-text1">Chat inteligente con modelos preentrenados y archivos adjuntos.</p>
        """, unsafe_allow_html=True)

    # [ DATA SCIENCIE ] ############################################################################################################
    col1, col2 = st.columns([4, 1])
    with col1:
        st.header("> Apps basados en Data Science: 🔬")
        #st.caption("Selecciona una aplicación desde el menú lateral para comenzar.")
    with col2:
        x=None

    cols = st.columns(3)
    with cols[0]:
        st.subheader("Cuadrator")
        st.markdown("""
        <style> .small-text1 {font-size: 0.5em;color: #8B0000;} </style>
        <p class="small-text1">Análisis aleatorio de préstamos con Pandas, Numpy y Montecarlo.</p>
        """, unsafe_allow_html=True)

        st.subheader("  ")
        st.write(" ")

    with cols[1]:
        st.subheader(" ")
        st.write(" ")

        st.subheader(" ")
        st.markdown("""
        <style> .small-text1 {font-size: 0.5em;color: #8B0000;} </style>
        <p class="small-text1"> </p>
        """, unsafe_allow_html=True)

    with cols[2]:
        st.subheader(" ")
        st.markdown("""
        <style> .small-text1 {font-size: 0.5em;color: #8B0000;} </style>
        <p class="small-text1"> </p>
        """, unsafe_allow_html=True)

    # [ WEB SCRAPING ]############################################################################################################

    col1, col2 = st.columns([4, 1])
    with col1:
        st.header("> Apps basados en WebScraping: 🌐")
        #st.caption("Selecciona una aplicación desde el menú lateral para comenzar.")
    with col2:
        x=None

    cols = st.columns(3)
    with cols[0]:
        st.subheader("Eventos Relevantes")
        st.markdown("""
        <style> .small-text1 {font-size: 0.5em;color: #8B0000;} </style>
        <p class="small-text1">Extacción de los datos de eventos relevantes de todos los emisores activos para TDA publicados en BMV.com y BIVA.com</p>
        """, unsafe_allow_html=True)

        st.subheader(" ")
        st.write("")

    with cols[1]:
        st.subheader("Estados Financieros ")
        st.write("Extracción trimestral de los datos contables financieros de la web CNBV.com ")

        st.subheader(" ")
        st.markdown("""
        <style> .small-text1 {font-size: 0.5em;color: #8B0000;} </style>
        <p class="small-text1"> </p>
        """, unsafe_allow_html=True)

    with cols[2]:
        st.subheader(" ")
        st.markdown("""
        <style> .small-text1 {font-size: 0.5em;color: #8B0000;} </style>
        <p class="small-text1"> </p>
        """, unsafe_allow_html=True)

    # [ REPORTING ]############################################################################################################

    col1, col2 = st.columns([4, 1])
    with col1:
        st.header("> Apps basados en Reporting: 📈")
        #st.caption("Selecciona una aplicación desde el menú lateral para comenzar.")
    with col2:
        x=None

    cols = st.columns(3)
    with cols[0]:
        st.subheader("Eventos Relevantes")
        st.markdown("""
        <style> .small-text1 {font-size: 0.5em;color: #8B0000;} </style>
        <p class="small-text1">Historicos de eventos relevantes de todos los emisores activos para TDA publicados en BMV.com y BIVA.com</p>
        """, unsafe_allow_html=True)

        st.subheader(" ")
        st.write(" ")

    with cols[1]:
        st.subheader("Estados Financieros")
        st.write("Total de los datos trimestrales de los datos financieros de la web CNBV.com")

        st.subheader(" ")
        st.markdown("""
        <style> .small-text1 {font-size: 0.5em;color: #8B0000;} </style>
        <p class="small-text1"> </p>
        """, unsafe_allow_html=True)

    with cols[2]:
        st.subheader(" ")
        st.markdown("""
        <style> .small-text1 {font-size: 0.5em;color: #8B0000;} </style>
        <p class="small-text1"> </p>
        """, unsafe_allow_html=True)

    #############################################################################################################
    st.markdown("---")

    st.markdown("""
    <style>
    .small-text2 {
        font-size: 0.5em;
        color: gray;
        text-align: center;
    }
    </style>
    <p class="small-text2">TdA : Titulización de Activos </p>
    """, unsafe_allow_html=True)

    def get_image_base64(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    image_base64 = get_image_base64("img/logotipo.ico")
    st.markdown(
        f"""
        <div style='text-align: center;'>
            <img src='data:image/png;base64,{image_base64}' width='40'>
            <br>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.sidebar.expander("ℹ️ Info"):
        st.markdown("""
        - Agregar la IP http://10.10.30.7:8501/ como ruta de confianza
        - El puerto 8501 debe estar habilitado.
        - Seleccione una Aplicación.
        - Algunas App tendrán valores configurables
        - Para más ayuda contactar con: Steve Carpio
        """)
        st.caption("""
        Los modelos IA están preentrenados en constante aprendisaje.
        """)
        st.markdown("---")
        current_year = datetime.now().year
        st.markdown(f"**© {current_year} - TdA S.A.**")
    
    st.sidebar.caption("..... Ver.2.1 .....")

# ----------------------------------
# LÓGICA PRINCIPAL
# ----------------------------------

# Inicializar la variable de sesión si no existe
if "selected_app_key" not in st.session_state:
    st.session_state.selected_app_key = None

# Botón para volver al inicio
if st.sidebar.button("🏠 Ir a Inicio"):
    st.session_state.selected_app_key = None
    st.rerun()

# Botones para IA
with st.sidebar.expander("🤖 Inteligencia Artificial"):
    for name in IA_APPS:
        if st.button(name, key=f"btn_ia_{name}"):
            st.session_state.selected_app_key = name
            st.rerun()

# Botones para Data Science
with st.sidebar.expander("🔬 Data Science"):
    for name in DS_APPS:
        if st.button(name, key=f"btn_ds_{name}"):
            st.session_state.selected_app_key = name
            st.rerun()

# Botones para Web Scraping
with st.sidebar.expander("🌐 Web Scraping"):
    for name in WS_APPS:
        if st.button(name, key=f"btn_ws_{name}"):
            st.session_state.selected_app_key = name
            st.rerun()

# Botones para Reporting
with st.sidebar.expander("📈 Reporting"):
    for name in RP_APPS:
        if st.button(name, key=f"btn_rp_{name}"):
            st.session_state.selected_app_key = name
            st.rerun()            


# Mostrar la app seleccionada
if st.session_state.selected_app_key:
    if st.session_state.selected_app_key in IA_APPS:
        IA_APPS[st.session_state.selected_app_key].main()
    elif st.session_state.selected_app_key in DS_APPS:
        DS_APPS[st.session_state.selected_app_key].main()
    elif st.session_state.selected_app_key in RP_APPS:
        RP_APPS[st.session_state.selected_app_key].main()
    elif st.session_state.selected_app_key in WS_APPS:
        WS_APPS[st.session_state.selected_app_key].main()

    # Limpia GarbageCollector    
    gc.collect()
else:
    mostrar_inicio()

# source venv/bin/activate
# 🆕 💼 🏛️ 🆕 🗑️ 🟢 📦 📊 🏠 🤖

import streamlit as st
import base64
from datetime import datetime
from PIL import Image
from app import app1, app2, app3, app4, app5, app6
import gc

# Configuración
st.set_page_config(
    page_title="Portal IA (TdA)",
    page_icon="💼",
    layout="wide"
)

###### CUSTOMIZAR BOTONES ###############

#####################


# Diccionarios por bloque
IA_APPS = {
    "1 - Facturas PDF": app1,
    "2 - Transcripción de Audio": app2,
    "3 - ChatTDA": app3,
    "4 - SmartMail": app5
}

DS_APPS = {
    "1 - Cuadrator": app4,
    "2 - Pruebas STEVE": app6
}

RP_APPS = {
    "1 - Reporting": app4,
    "2 - Pruebas STEVE": app6
}


def mostrar_inicio():

    #############################################################################################################
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("Apps basados en IA: 🤖")
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

    #############################################################################################################
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("Apps basados en Data Science: 📊")
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
    <p class="small-text2">Para más ayuda, contactar con carpios@tda-sgft.com <br> Versión 1.0.0</p>
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

    with st.sidebar:
        st.markdown("---")
        st.markdown("""
        **🆘 Ayuda:**
        - Selecciona una App.
        - Puerto 8501 habilitado.
        - Contacto: Steve Carpio
        """)
        st.markdown("---")
        st.markdown("""
        **ℹ️ Información:**
        - IA TdA usa modelos preentrenados para OCR y análisis de datos.
        - Soporta PDF escaneados.
        """)
        st.markdown("---")
        current_year = datetime.now().year
        st.markdown(f"**© {current_year} - TdA S.A.**")

# Interfaz lateral
st.sidebar.title("Portal TdA")

mostrar_inicio_flag = False
selected_app = None

if st.sidebar.button("🏠 Ir a Inicio"):
    mostrar_inicio_flag = True

with st.sidebar.expander("🤖 Inteligencia Artificial"):
    for name, app in IA_APPS.items():
        if st.button(name, key=f"btn_ia_{name}"):
            selected_app = app

with st.sidebar.expander("📊 Data Science"):
    for name, app in DS_APPS.items():
        if st.button(name, key=f"btn_ds_{name}"):
            selected_app = app

# Mostrar app o inicio
if selected_app:
    selected_app.main()
    gc.collect()
else:
    mostrar_inicio()

# source venv/bin/activate
# 🆕 💼 🏛️ 🆕 🗑️ 🟢 📦 📊 🏠 🤖 📈 🔬

import streamlit as st
import base64
from datetime import datetime
from PIL import Image
from app import app1, app2, app3, app4, app5, app6
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
    "3 - ChatTDA": app3,
    "4 - SmartMail": app5
}
# Diccionario Data Sciencie
DS_APPS = {
    "1 - Cuadrator": app4,
    "2 - Data Sciencie2": app6
}
# Diccionario Reporting
RP_APPS = {
    "1 - Eventos Relevantes": app6,
    "2 - Estados Financieros": app6
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
        st.title("Apps basados en Data Science: 🔬")
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
    gc.collect()
else:
    mostrar_inicio()

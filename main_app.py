# source venv/bin/activate
# 🆕 💼 🏛️ 🗑️ 🟢 📦 📊 🏠 🤖 📈 🔬 🌐 🚨 ⏳ 🔄 ℹ️ 📜 📁 🗂️ 📅 📗 ⚠️ ✅ ❌ 🚧 ▶️ 📧

import streamlit as st
import base64
from datetime import datetime
from PIL import Image
from app import app0, app1, app2, app3, app4, app5, app6, app7, app8, app9, app10, app11, app12
import gc

def mantenimiento():
    st.toast(" Para cualquier duda, contactar con **Steve Carpio**.", icon="💬")
    st.toast(" La página se recargará automáticamente cuando el servidor esté disponible nuevamente.", icon="🔄")
    st.toast(" Tiempo estimado de reinicio: 3 minutos.", icon="⏳")
    st.toast(" El servidor se reiniciará en breve.", icon="🚨")

# Configuración
st.set_page_config(
    page_title="Portal IA",
    page_icon="🤖",
    layout="wide"
)

# Evitar cacheo en recursos estáticos
st.markdown(
    """
    <script>
    if ('caches' in window) {
        caches.keys().then(function(names) {
            for (let name of names) caches.delete(name);
        });
    }
    </script>
    """,
    unsafe_allow_html=True
)

# Diccionario Inteligencia Artificial
IA_APPS = {
    "1 - Facturas PDF": app1,
    "2 - Transcripción de Audio": app2,
    "3 - Chat-TdA": app3,
    "4 - SmartMail": app5,
    "5 - Contratos PDF": app6
}
# Diccionario Data Sciencie
DS_APPS = {
    "1 - Cuadrator": app4,
}
# Diccionario WebScraping
WS_APPS = {
    "1 - Eventos Relevantes.": app10,
    "2 - Estados Financieros.": app12
}
# Diccionario Reporting
RP_APPS = {
    "1 - Eventos Relevantes": app7,
    "2 - Estados Financieros": app11,
    "3 - Flujos Bloomberg": app9
}

# Gestor de Proyectos
GP_APPS = {
    "1 - DEV VBA-PYTHON-VBA": app8
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

        st.subheader("Contratos PDF")
        st.markdown("""
        <style> .small-text1 {font-size: 0.5em;color: #8B0000;} </style>
        <p class="small-text1">Carga por rango, analiza por bloques, y pregunta por IA sin superar el límite de contexto.</p>
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
        st.write("Extracción de los datos Financieros para todas las Claves Pizarra publicadas en la CNBV.com")

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
        st.write("Informe de los datos Financieros de todas las Claves Pizarra publicadas en la CNBV.com.")

        st.subheader(" ")
        st.markdown("""
        <style> .small-text1 {font-size: 0.5em;color: #8B0000;} </style>
        <p class="small-text1">  </p>
        """, unsafe_allow_html=True)

    with cols[2]:
        st.subheader("Flujos Bloomberg")
        st.markdown("""
        <style> .small-text1 {font-size: 0.5em;color: #8B0000;} </style>
        <p class="small-text1">Extrae y procesa los flujos de Sabadell que se encuentran en archivos Excel y los convierte en archivos TXT compatibles con Bloomberg.</p>
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

    with st.sidebar.expander("Info", icon=":material/info:"):  # ℹ️
        st.caption("""
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
    
    client_ip = st.context.ip_address
    st.sidebar.caption(f"Portal Python TdA Ver: 2.1 - Connect from: {client_ip}")
    

# ----------------------------------
# LÓGICA PRINCIPAL
# ----------------------------------

# Inicializar variable de sesión
if "selected_app_key" not in st.session_state:
    st.session_state.selected_app_key = None

# Mostrar dos columnas con los botones Inicio y Chat-TdA
col1x, col2x = st.sidebar.columns(2)
with col1x:
    # Siempre mostrar botón "Ir a Inicio"
    if st.button("Ir a Inicio", icon=":material/home:"):  #  🏠   
        st.session_state.selected_app_key = None
        st.rerun()
with col2x:
    valorx = list(IA_APPS.keys())[2]
    # Crear AQUI BOTON a la APP3
    if st.button("IA TdA", key="btn_app3", help="Chatea con la IA de TdA", icon=":material/smart_toy:"): # Chat-TdA 🤖
        st.session_state.selected_app_key = valorx
        st.rerun()
   
# Si NO hay app seleccionada → mostrar los expanders
if st.session_state.selected_app_key is None:

    # Botones para IA
    with st.sidebar.expander("Inteligencia Artificial", icon=":material/smart_toy:"): # 🤖
        for name in IA_APPS:
            if st.button(name, key=f"btn_ia_{name}"):
                st.session_state.selected_app_key = name
                st.rerun()
                

    # Botones para Data Science
    with st.sidebar.expander("Data Science", icon=":material/biotech:"):  #  🔬
        for name in DS_APPS:
            if st.button(name, key=f"btn_ds_{name}"):
                st.session_state.selected_app_key = name
                st.rerun()

    # Botones para Web Scraping
    with st.sidebar.expander("Web Scraping", icon=":material/language:"):  #  🌐
        for name in WS_APPS:
            if st.button(name, key=f"btn_ws_{name}"):
                st.session_state.selected_app_key = name
                st.rerun()

    # Botones para Reporting
    with st.sidebar.expander("Reporting", icon=":material/query_stats:"):  #  📈
        for name in RP_APPS:
            if st.button(name, key=f"btn_rp_{name}"):
                st.session_state.selected_app_key = name
                st.rerun()

    # Botones para Gestor de Proyectos
    with st.sidebar.expander("Gestor Proyectos", icon=":material/library_books:"):  # 📁
        for name in GP_APPS:
            if st.button(name, key=f"btn_gp_{name}"):
                st.session_state.selected_app_key = name
                st.rerun()


# Si hay una app seleccionada → mostrar solo esa app
if st.session_state.selected_app_key:
    key = st.session_state.selected_app_key
    if key in IA_APPS:
        IA_APPS[key].main()
    elif key in DS_APPS:
        DS_APPS[key].main()
    elif key in RP_APPS:
        RP_APPS[key].main()
    elif key in WS_APPS:
        WS_APPS[key].main()
    elif key in GP_APPS:
        GP_APPS[key].main()

    # Limpieza de memoria
    gc.collect()

else:
    # Mostrar la página de inicio
    mostrar_inicio()

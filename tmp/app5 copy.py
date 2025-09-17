import streamlit as st
import imaplib
import email
from email.header import decode_header
import ollama


# ----------------------------------------
# FUNCIONES 
# ----------------------------------------

# CONFIGURACIÓN DEL MODELO
OLLAMA_MODEL = "llama3:instruct"

# FUNCIÓN: Conectar a Zimbra via IMAP
@st.cache_resource
def conectar_imap(usuario, password, servidor, puerto=993):
    mail = imaplib.IMAP4_SSL(servidor, puerto)
    mail.login(usuario, password)
    return mail

# FUNCIÓN: Obtener lista de carpetas del correo
def obtener_carpetas(mail):
    result, data = mail.list()
    carpetas = []
    if result == "OK":
        for item in data:
            partes = item.decode().split(' "/" ')
            if len(partes) == 2:
                carpeta = partes[1].replace('"', '')
                carpetas.append(carpeta)
    return carpetas

# FUNCIÓN: Obtener correos del buzón
def obtener_emails(mail, carpeta="INBOX", cantidad=10):
    mail.select(carpeta)
    result, data = mail.search(None, "ALL")
    ids = data[0].split()[-cantidad:]

    correos = []
    for i in reversed(ids):
        result, data = mail.fetch(i, "(RFC822)")
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        asunto, encoding = decode_header(msg["Subject"])[0]
        if isinstance(asunto, bytes):
            asunto = asunto.decode(encoding or "utf-8", errors="ignore")

        de = msg.get("From")
        cuerpo = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain" and not part.get("Content-Disposition"):
                    payload = part.get_payload(decode=True)
                    if isinstance(payload, bytes):
                        cuerpo = payload.decode(errors="ignore")
                    else:
                        cuerpo = str(payload)
                    break
        else:
            payload = msg.get_payload(decode=True)
            if isinstance(payload, bytes):
                cuerpo = payload.decode(errors="ignore")
            else:
                cuerpo = str(payload)

        correos.append({"asunto": asunto, "de": de, "cuerpo": cuerpo})
    return correos

# FUNCIÓN: Llamar al modelo local con ollama
def preguntar_a_ollama(prompt):
    try:
        respuesta = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return respuesta['message']['content']
    except Exception as e:
        return f"❌ Error al consultar Ollama: {e}"


# ----------------------------------------
# APP PRINCIPAL
# ----------------------------------------

def main():

    # STREAMLIT UI
    st.set_page_config(page_title="Lectura de Correos - app5", layout="wide")
    st.title("📬 Análisis de Correos con IA - App5")

    with st.sidebar:
        st.header("🔐 Configuración IMAP")
        usuario = st.text_input("Correo", placeholder="carpios@tda-sgft.com")
        password = st.text_input("Contraseña", type="password")
        servidor = st.text_input("Servidor IMAP", value="zimbra.tda-sgft.com")
        cantidad = st.slider("Número de correos", 1, 50, 10)

        # Intentar cargar carpetas si ya hay credenciales
        carpetas_disponibles = ["INBOX"]
        if usuario and password and servidor:
            try:
                mail = conectar_imap(usuario, password, servidor)
                carpetas_disponibles = obtener_carpetas(mail)
            except Exception as e:
                st.error(f"❌ Error al obtener carpetas: {e}")

        carpeta = st.selectbox("Selecciona carpeta", carpetas_disponibles)

        if st.button("🔄 Conectar y Cargar Correos"):
            if usuario and password and servidor:
                try:
                    mail = conectar_imap(usuario, password, servidor)
                    st.session_state["correos"] = obtener_emails(mail, carpeta, cantidad)
                    st.success("✅ Correos cargados correctamente.")
                except Exception as e:
                    st.error(f"❌ Error al conectar: {e}")
            else:
                st.warning("⚠️ Por favor completa todos los campos.")

    # Mostrar correos si ya están cargados
    if "correos" in st.session_state:
        st.subheader("📨 Correos recibidos")
        seleccion = st.selectbox("Selecciona un correo", [f"{c['asunto']} - {c['de']}" for c in st.session_state["correos"]])
        correo = next(c for c in st.session_state["correos"] if f"{c['asunto']} - {c['de']}" == seleccion)
        
        st.markdown(f"### ✉️ Asunto: {correo['asunto']}")
        st.markdown(f"**De:** {correo['de']}")
        st.markdown("---")
        st.text_area("📄 Cuerpo del correo", correo["cuerpo"], height=300)

        st.markdown("## 🤖 Procesamiento con IA")

        opcion = st.selectbox("¿Qué quieres hacer con el correo?", ["Resumen", "Extraer información", "Responder pregunta sobre el correo"])
        
        if opcion == "Resumen":
            if st.button("📌 Generar resumen"):
                with st.spinner("Procesando..."):
                    prompt = f"Resume brevemente el siguiente correo:\n\n{correo['cuerpo']}"
                    respuesta = preguntar_a_ollama(prompt)
                    st.success("📝 Resumen:")
                    st.write(respuesta)

        elif opcion == "Extraer información":
            if st.button("🧠 Extraer información"):
                with st.spinner("Extrayendo..."):
                    prompt = f"Extrae los datos importantes del siguiente correo (nombres, fechas, lugares, tareas, etc):\n\n{correo['cuerpo']}"
                    respuesta = preguntar_a_ollama(prompt)
                    st.success("🔎 Información encontrada:")
                    st.write(respuesta)

        elif opcion == "Responder pregunta sobre el correo":
            pregunta = st.text_input("Escribe tu pregunta:")
            if st.button("💬 Responder"):
                with st.spinner("Consultando..."):
                    prompt = f"Lee el siguiente correo:\n\n{correo['cuerpo']}\n\nY responde esta pregunta:\n{pregunta}"
                    respuesta = preguntar_a_ollama(prompt)
                    st.success("🗣️ Respuesta:")
                    st.write(respuesta)


# ----------------------------------------
# EJECUCIÓN PRINCIPAL
# ----------------------------------------

if __name__ == "__main__":
    main()

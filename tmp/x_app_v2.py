import os
import re
import json
import shutil
from io import BytesIO
import tempfile

import streamlit as st
import pandas as pd
import pdfplumber
from pdf2image import convert_from_bytes
import pytesseract
import ollama

# Configuración inicial de la app
st.set_page_config("Lector de Facturas IA", layout="wide")
st.title("📄 Lector de Facturas con IA Mistral (Ollama)")

# Crear directorio temporal para subidas
UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), "facturas_subidas")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Función para limpiar el directorio de subidas
def limpiar_subidas():
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            st.error(f'Error al eliminar {file_path}. Razón: {e}')

# Función para limpiar/rescatar JSON malformado
def limpiar_json_respuesta(respuesta):
    respuesta = respuesta.strip()
    respuesta = respuesta.replace("'", '"')  # comillas simples a dobles
    if respuesta.startswith("{") and not respuesta.endswith("}"):
        respuesta += "}"
    return respuesta

# Opción 1: Selección de carpeta local (como antes)
#st.sidebar.subheader("Opción 1: Procesar desde servidor")
# folder = st.sidebar.text_input("Ruta de carpeta con PDFs en el servidor", value=os.getcwd())
folder = "/home/robot/Descargas"

# Opción 2: Subida de archivos desde el cliente
#st.sidebar.subheader("Opción 2: Subir archivos desde tu PC")
st.sidebar.subheader("Subir archivos desde tu PC")
uploaded_files = st.sidebar.file_uploader(
    "Selecciona archivos PDF para procesar",
    type=["pdf"],
    accept_multiple_files=True
)

# Procesar archivos subidos
if uploaded_files:
    limpiar_subidas()  # Limpiar subidas anteriores
    
    progress_bar = st.sidebar.progress(0)
    total_files = len(uploaded_files)
    
    for i, uploaded_file in enumerate(uploaded_files):
        # Guardar el archivo en el directorio temporal
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        progress_bar.progress((i + 1) / total_files)
    
    st.sidebar.success(f"✅ Se subieron {total_files} archivos correctamente")
    folder = UPLOAD_FOLDER  # Usar la carpeta de subidas para procesamiento

# Verificar si hay archivos para procesar
if not os.path.isdir(folder):
    st.error("❌ No se ha seleccionado una ruta válida o no se han subido archivos.")
    st.stop()

# Botón para procesar PDFs (funciona tanto para la ruta local como para archivos subidos)
if st.sidebar.button("Procesar PDFs"):
    registros = []
    pdf_files = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]
    
    if not pdf_files:
        st.error("❌ No se encontraron archivos PDF en la carpeta seleccionada.")
        st.stop()

    progress_bar = st.progress(0)
    total_pdfs = len(pdf_files)

    for i, fn in enumerate(pdf_files):
        path = os.path.join(folder, fn)
        text = ""

        # Extraer texto con pdfplumber
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        # Si no hay texto, hacer OCR
        if not text.strip():
            with open(path, "rb") as f:
                images = convert_from_bytes(f.read())
            for img in images:
                text += pytesseract.image_to_string(img, lang="spa") + "\n"

        # Prompt a Mistral
        prompt = (
            "Analiza el siguiente texto de una factura y responde SOLO con un objeto JSON plano, sin texto adicional, ni listas, ni explicaciones.\n"
            "Debes extraer estos campos exactamente con estos nombres:\n"
            "- numero_factura (ej: 'M24000103')\n"
            "- fecha (formato dd/mm/yyyy)\n"
            "- base (solo número en euros)\n"
            "- iva (solo número en euros)\n"
            "- irpf (solo número en euros o null)\n"
            "- total (solo número en euros)\n"
            "Si algún campo no se encuentra, pon null.\n\n"
            "Texto:\n" + text
        )

        try:
            resp = ollama.chat(model="llama3:instruct", messages=[{"role": "user", "content": prompt}])
            respuesta_texto = resp["message"]["content"]
        except Exception as e:
            st.error(f"❌ Error llamando a Mistral con archivo {fn}: {e}")
            continue

        # Mostrar respuesta
        #st.subheader(f"🧾 Respuesta de Mistral para: {fn}")
        #st.code(respuesta_texto, language="json")

        # Limpiar y convertir JSON
        respuesta_texto = limpiar_json_respuesta(respuesta_texto)

        try:
            rec = json.loads(respuesta_texto)
        except json.JSONDecodeError as e:
            st.error(f"❌ Error al convertir JSON para {fn}: {e}")
            st.text(respuesta_texto)
            continue

        registros.append({**{"archivo": fn}, **rec})
        progress_bar.progress((i + 1) / total_pdfs)

    # Si no hay registros válidos
    if not registros:
        st.warning("⚠️ No se pudieron extraer datos de ningún PDF.")
        st.stop()

    # Construir DataFrame
    df = pd.DataFrame(registros)
    #st.write("📋 Columnas detectadas:", df.columns.tolist())

    # Validaciones básicas
    if "fecha" in df.columns:
        df["fecha"] = df["fecha"].apply(lambda x: x if re.match(r"\d{2}/\d{2}/\d{4}", str(x)) else "")
    else:
        st.warning("⚠️ Campo 'fecha' no encontrado en la respuesta.")

    # Convertir campos monetarios a float, manejando errores y valores nulos
    # Por esta versión más robusta:
    for col in ["base", "iva", "irpf", "total"]:
        if col in df.columns:
            def convertir_valor(x):
                try:
                    if pd.isna(x) or x is None or str(x).strip() in ["", "null"]:
                        return None
                    # Limpieza más exhaustiva
                    valor_limpio = re.sub(r"[^\d\.,-]", "", str(x).strip())
                    valor_limpio = valor_limpio.replace(",", ".")
                    # Manejo de valores negativos
                    if "-" in valor_limpio and not valor_limpio.startswith("-"):
                        valor_limpio = "-" + valor_limpio.replace("-", "")
                    return float(valor_limpio)
                except Exception as e:
                    st.warning(f"Error convirtiendo {col}={x}: {str(e)}")
                    return None
            
            df[col] = df[col].apply(convertir_valor)
        else:
            st.warning(f"⚠️ Campo '{col}' no encontrado en la respuesta.")



    # Mostrar tabla
    st.subheader("✅ Datos extraídos")
    st.dataframe(df)

    # Descargar Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    output.seek(0)

    st.download_button(
        label="📥 Descargar Excel",
        data=output,
        file_name="facturas.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    # Limpiar archivos subidos después del procesamiento
    limpiar_subidas()
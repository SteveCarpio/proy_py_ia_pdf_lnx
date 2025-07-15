# app.py
# curl https://ollama.ai/install.sh | sh
# ollama pull mistral
#
# sudo apt update
# sudo apt install python3 python3-venv python3-pip tesseract-ocr poppler-utils
# 
## pip install streamlit pdfplumber pytesseract pdf2image pandas ollama xlsxwriter


import os
import re
import json
from io import BytesIO

import streamlit as st
import pandas as pd
import pdfplumber
from pdf2image import convert_from_bytes
import pytesseract
import ollama

# Configuración inicial de la app
st.set_page_config("Lector de Facturas IA", layout="wide")
st.title("📄 Lector de Facturas con IA Mistral (Ollama)")

# Carpeta con PDFs
folder = st.sidebar.text_input("Ruta de carpeta con PDFs", value=os.getcwd())

if not os.path.isdir(folder):
    st.error("❌ La ruta no es válida.")
    st.stop()

# Función para limpiar/rescatar JSON malformado
def limpiar_json_respuesta(respuesta):
    respuesta = respuesta.strip()
    respuesta = respuesta.replace("'", '"')  # comillas simples a dobles
    if respuesta.startswith("{") and not respuesta.endswith("}"):
        respuesta += "}"
    return respuesta

# Botón para procesar PDFs
if st.sidebar.button("Procesar PDFs"):
    registros = []

    for fn in os.listdir(folder):
        if not fn.lower().endswith(".pdf"):
            continue

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
        st.subheader(f"🧾 Respuesta de Mistral para: {fn}")
        st.code(respuesta_texto, language="json")

        # Limpiar y convertir JSON
        respuesta_texto = limpiar_json_respuesta(respuesta_texto)

        try:
            rec = json.loads(respuesta_texto)
        except json.JSONDecodeError as e:
            st.error(f"❌ Error al convertir JSON para {fn}: {e}")
            st.text(respuesta_texto)
            continue

        registros.append({**{"archivo": fn}, **rec})

    # Si no hay registros válidos
    if not registros:
        st.warning("⚠️ No se pudieron extraer datos de ningún PDF.")
        st.stop()

    # Construir DataFrame
    df = pd.DataFrame(registros)
    st.write("📋 Columnas detectadas:", df.columns.tolist())

    # Validaciones básicas
    if "fecha" in df.columns:
        df["fecha"] = df["fecha"].apply(lambda x: x if re.match(r"\d{2}/\d{2}/\d{4}", str(x)) else "")
    else:
        st.warning("⚠️ Campo 'fecha' no encontrado en la respuesta.")

    for col in ["base", "iva", "irpf", "total"]:
        if col in df.columns:
            df[col] = df[col].apply(
                lambda x: float(re.sub(r"[^\d\.,]", "", str(x)).replace(",", ".")) if pd.notna(x) else None
            )
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

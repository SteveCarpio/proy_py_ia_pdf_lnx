# app.py
# curl https://ollama.ai/install.sh | sh
# ollama pull mistral
#
# sudo apt update
# sudo apt install python3 python3-venv python3-pip tesseract-ocr poppler-utils
# 
## pip install streamlit pdfplumber pytesseract pdf2image pandas ollama


import os, re, tempfile
import streamlit as st
import pandas as pd
import pdfplumber
from pdf2image import convert_from_bytes
import pytesseract
import ollama

# Configuración Streamlit
st.set_page_config("Invoice Extractor", layout="wide")
st.title("📄 Lector de Facturas con IA Mistral (Ollama)")

# Navegación de carpeta
folder = st.sidebar.text_input("Carpeta con PDFs", value=os.getcwd())
if not os.path.isdir(folder):
    st.error("Ruta no válida.")

# Botón de procesamiento
if st.sidebar.button("Procesar PDFs"):
    registros = []
    for fn in os.listdir(folder):
        if fn.lower().endswith(".pdf"):
            path = os.path.join(folder, fn)
            with open(path, "rb") as f:
                content = f.read()
            # Obtener texto nativo
            text = ""
            with pdfplumber.open(path) as pdf:
                for p in pdf.pages:
                    t = p.extract_text()
                    if t:
                        text += t + "\n"
            # Si no tiene texto, aplicar OCR
            if not text.strip():
                imgs = convert_from_bytes(content)
                for img in imgs:
                    text += pytesseract.image_to_string(img, lang="spa") + "\n"
            # Llamada a Mistral (Ollama)
            prompt = (
                "Extrae los campos: numero_factura, fecha, base, iva, irpf, total. "
                "Formato JSON. Texto:\n" + text
            )
            resp = ollama.chat(model="mistral", messages=[{"role":"user","content":prompt}])
            try:
                data = resp["message"]["content"]
                rec = st.experimental_memo(pd.read_json)(data, orient="records")
            except:
                rec = {}
            registros.append({**{"archivo":fn}, **rec})

    df = pd.DataFrame(registros)
    # Validación básica con regex
    df["fecha"] = df["fecha"].apply(lambda x: x if re.match(r"\d{2}/\d{2}/\d{4}", str(x)) else "")
    for col in ["base","iva","irpf","total"]:
        df[col] = df[col].apply(lambda x: float(re.sub(r"[^\d\.,]","", str(x)).replace(",", ".")) if re.sub(r"[^\d\.,]","", str(x)) else None)
    st.write(df)

    #st.download_button("Descargar Excel", df.to_excel(index=False), "facturas.xlsx", "application/vnd.ms-excel")

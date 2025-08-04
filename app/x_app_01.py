    # app.py
    # curl https://ollama.ai/install.sh | sh
    # ollama pull mistral
    #
    # sudo apt update
    # sudo apt install python3 python3-venv python3-pip tesseract-ocr poppler-utils
    # 
    # pip install streamlit pdfplumber pytesseract pdf2image pandas ollama xlsxwriter
    # pip install -r requirements.txt
    #
    # python3 -m venv venv
    #
    # source venv/bin/activate
    # streamlit run app.py
    #

def mostrar():
    import os
    import re
    import json
    import shutil
    from io import BytesIO
    import tempfile
    from datetime import datetime
    import streamlit as st
    import pandas as pd
    import pdfplumber
    from pdf2image import convert_from_bytes
    import pytesseract
    import ollama

    # Configuración inicial de la app
    st.set_page_config("(TDA) Lector de Facturas IA", layout="wide")
    st.title("📄 (TDA) Lector de Facturas con IA")
    st.text("Extrae datos de facturas en PDF usando IA y OCR")

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

    # Función para convertir valores al formato europeo
    def convertir_valor_europeo(x):
        """
        Convierte números en formato europeo (1.234,56) a float (1234.56).
        Maneja casos edge como negativos, valores nulos y formatos mixtos.
        """
        try:
            # Verificar valores nulos/vacíos
            if pd.isna(x) or x is None or str(x).strip().lower() in ["", "null", "nan"]:
                return None
            
            valor_str = str(x).strip()
            
            # Eliminar símbolos no numéricos (excepto puntos, comas y signos)
            valor_limpio = re.sub(r"[^\d\.,-]", "", valor_str)
            
            # Caso 1: Formato europeo estándar (1.234,56 → 1234.56)
            if "," in valor_limpio:
                # Eliminar puntos de miles y convertir coma decimal a punto
                partes = valor_limpio.split(",")
                parte_entera = partes[0].replace(".", "")
                valor_final = f"{parte_entera}.{partes[1]}" if len(partes) > 1 else parte_entera
            
            # Caso 2: Ya tiene formato válido (1234.56)
            elif "." in valor_limpio and valor_limpio.count(".") == 1:
                valor_final = valor_limpio
            
            # Caso 3: Sin decimales (1.234 → 1234)
            else:
                valor_final = valor_limpio.replace(".", "")
            
            # Manejar negativos (ej: -1.234,56 o 1.234,56-)
            if "-" in valor_final:
                valor_final = "-" + valor_final.replace("-", "")
            
            return float(valor_final)
        
        except Exception as e:
            st.warning(f"⚠️ Error convirtiendo valor '{x}': {str(e)}")
            return None

    # Función para formatear números en visualización (europeo)
    def formato_europeo(valor):
        if pd.isna(valor) or valor is None:
            return ""
        try:
            return "{:,.2f}".format(float(valor)).replace(",", "X").replace(".", ",").replace("X", ".")
        except:
            return str(valor)

    # Función para limpiar/rescatar JSON malformado
    def limpiar_json_respuesta(respuesta):
        respuesta = respuesta.strip()
        respuesta = respuesta.replace("'", '"')  # comillas simples a dobles
        if respuesta.startswith("{") and not respuesta.endswith("}"):
            respuesta += "}"
        return respuesta

    # Opción 1: Selección de carpeta local
    folder = "/home/robot/Descargas"

    # Opción 2: Subida de archivos desde el cliente
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

    # Botón para procesar PDFs
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

        # Validaciones básicas
        if "fecha" in df.columns:
            df["fecha"] = df["fecha"].apply(lambda x: x if re.match(r"\d{2}/\d{2}/\d{4}", str(x)) else "")
        else:
            st.warning("⚠️ Campo 'fecha' no encontrado en la respuesta.")

        # Convertir campos monetarios
        for col in ["base", "iva", "irpf", "total"]:
            if col in df.columns:
                df[col] = df[col].apply(convertir_valor_europeo)
            else:
                st.warning(f"⚠️ Campo '{col}' no encontrado en la respuesta.")

        # Mostrar tabla con formato europeo
        st.subheader("✅ Datos extraídos")
        
        # Crear DataFrame para visualización
        df_mostrar = df.copy()
        for col in ["base", "iva", "irpf", "total"]:
            if col in df_mostrar.columns:
                df_mostrar[col] = df_mostrar[col].apply(formato_europeo)
        
        st.dataframe(df_mostrar)

        # Descargar Excel (con valores numéricos originales)
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False)
            
            # Aplicar formato europeo en Excel
            workbook = writer.book
            euro_format = workbook.add_format({'num_format': '#.##0,00'})
            worksheet = writer.sheets['Sheet1']
            worksheet.set_column('C:F', 15, euro_format)
        
        output.seek(0)

        st.download_button(
            label="📥 Descargar Excel",
            data=output,
            file_name="facturas.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # Limpiar archivos subidos después del procesamiento
        limpiar_subidas()

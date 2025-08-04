import streamlit as st
import pandas as pd
import os
from ocr_processor import FacturaProcessor
from ollama_integration import OllamaAnalyzer

# Configuración
st.set_page_config(page_title="Procesador Masivo de Facturas", layout="wide")
st.title("📂 Procesador de Facturas con IA")

# Widgets
tab1, tab2 = st.tabs(["Procesar Carpeta", "Procesar Archivo"])

with tab1:
    folder_path = st.text_input("Ruta de carpeta con facturas:", help="Ej: C:/facturas/ o /home/usuario/facturas/")
    if folder_path and os.path.isdir(folder_path):
        processor = FacturaProcessor()
        with st.spinner("Procesando facturas..."):
            df = processor.process_folder(folder_path)
            
            # Mostrar tabla
            st.dataframe(
                df,
                use_container_width=True,
                column_config={
                    "archivo": "Archivo",
                    "total": st.column_config.NumberColumn("Total (EUR)", format="%.2f €")
                }
            )
            
            # Análisis con Ollama (para el primer archivo)
            if st.toggle("¿Analizar primera factura con Ollama?"):
                first_file = os.path.join(folder_path, df.iloc[0]["archivo"])
                text = processor.extract_text(first_file)
                analyzer = OllamaAnalyzer()
                prompt = """
                Extrae en JSON: 
                - "clasificacion": ["factura_electronica", "factura_servicios", "otros"]
                - "resumen": "Resumen en 10 palabras"
                """
                analysis = analyzer.analyze_text(text, prompt)
                st.code(analysis, language="json")

with tab2:
    uploaded_file = st.file_uploader("Sube una factura (PDF/PNG/JPG)")
    if uploaded_file:
    with st.spinner("Extrayendo texto de la factura..."):
        extracted_text = processor.extract_text(file_path)
        fields = processor.extract_fields(extracted_text)  # Extrae TODOS los campos (viejos y nuevos)
        
        st.text_area("Texto extraído:", extracted_text, height=200)
        
        # --- Campos detectados (actualizado) ---
        st.subheader("📊 Campos Detectados")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("N° Factura", fields.get("número_factura", "No detectado"))
            st.metric("Total (EUR)", fields.get("total", "No detectado"))
            st.metric("Cliente", fields.get("cliente", "No detectado"))  # Nuevo
        with col2:
            st.metric("IVA (EUR)", fields.get("iva", "No detectado"))
            st.metric("Fecha", fields.get("fecha", "No detectado"))
            st.metric("IVA %", fields.get("iva_porcentaje", "No detectado"))  # Nuevo
        
        # Campo adicional (dirección)
        st.metric("Dirección", fields.get("dirección", "No detectado"))

        # Guardar texto (opcional)
        saved_path = processor.save_text(extracted_text, uploaded_file.name)
        st.success(f"✅ Texto guardado en: {saved_path}")
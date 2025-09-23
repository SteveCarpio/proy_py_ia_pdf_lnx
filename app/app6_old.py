import streamlit as st

# ----------------------------------------
# EJECUCIÓN PRINCIPAL
# ----------------------------------------
def main():
    st.caption("no usar está página por favor.. ")

    
    import PyPDF2
    import ollama
    import pandas as pd
    from pathlib import Path

    # -------------------------------------
    # CONFIGURACIÓN
    # -------------------------------------
    st.set_page_config(page_title="Análisis de Fideicomisos", layout="wide")
    MODEL = "jobautomation/OpenEuroLLM-Spanish"

    # -------------------------------------
    # FUNCIONES
    # -------------------------------------

    def cargar_pdf(path, max_paginas=250):
        #pdf_file = open(path, 'rb')
        pdf_file = path  # UploadedFile ya es un objeto de tipo archivo
        reader = PyPDF2.PdfReader(pdf_file)
        contenido_paginas = []

        for i, page in enumerate(reader.pages[:max_paginas]):
            text = page.extract_text()
            if text:
                contenido_paginas.append((i + 1, text))

        return contenido_paginas

    def dividir_en_bloques(paginas, tamaño_bloque=10):
        bloques = []
        for i in range(0, len(paginas), tamaño_bloque):
            bloque = paginas[i:i + tamaño_bloque]
            texto_bloque = "\n\n".join([f"[Página {p}] {t}" for p, t in bloque])
            bloques.append((bloque[0][0], bloque[-1][0], texto_bloque))
        return bloques

    def preguntar_al_modelo(prompt):
        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        return response['message']['content']

    # -------------------------------------
    # APP PRINCIPAL
    # -------------------------------------

    st.title("🔍 Análisis de Contrato: Reservas de Fideicomisos")
    uploaded_file = st.file_uploader("📄 Sube tu contrato en PDF", type=["pdf"])

    if uploaded_file:
        st.info("Procesando el PDF... puede tardar unos segundos.")
        contenido = cargar_pdf(uploaded_file)
        bloques = dividir_en_bloques(contenido, tamaño_bloque=10)

        resultados_resumen = []
        formulas_extraidas = []

        # Paso por bloques
        with st.spinner("Analizando por bloques..."):
            for inicio, fin, bloque in bloques:
                pregunta = f"""
    Tengo un contrato legal. Quiero que busques en el siguiente texto todos los artículos o secciones que hagan referencia a cualquier tipo de "reserva de fideicomisos".

    Para cada artículo encontrado, devuélveme:
    1. El número o nombre del artículo
    2. La página (si la menciono en el texto que te doy)
    3. Un resumen en 1 sola frase de qué trata ese artículo

    Además, si el artículo contiene una fórmula o ecuación:
    - Extrae la fórmula exacta (en texto o símbolos)
    - Explica el significado de cada variable o constante
    - Devuélvelo en una tabla con columnas: Artículo, Fórmula, Variable, Definición

    Aquí tienes el texto (de la página {inicio} a {fin}):

    {bloque}
    """
                respuesta = preguntar_al_modelo(pregunta)
                resultados_resumen.append(respuesta)

        # Mostrar resultados combinados
        st.subheader("📌 Resultados resumidos por bloque")
        for i, resultado in enumerate(resultados_resumen):
            st.markdown(f"### 🔹 Bloque {i+1}")
            st.markdown(resultados_resumen[i])

        # (Opcional) Guardar en archivo
        guardar = st.checkbox("💾 Guardar resultado completo en archivo")

        if guardar:
            full_output = "\n\n---\n\n".join(resultados_resumen)
            with open("resumen_fideicomisos.txt", "w", encoding="utf-8") as f:
                f.write(full_output)
            st.success("✅ Resultado guardado como 'resumen_fideicomisos.txt'")






if __name__ == "__main__":
    main()

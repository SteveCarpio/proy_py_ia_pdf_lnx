# 📈 Reporting Eventos Relevantes
import streamlit as st

# ----------------------------------------
# EJECUCIÓN PRINCIPAL
# ----------------------------------------
def main():
    import pandas as pd
    from app.appOra import get_oracle_connection

    st.set_page_config(page_title="Eventos Relevantes - Filtros", layout="wide")
    st.title("📈 Eventos Relevantes - Filtros Interactivos")

    # Cargar datos desde Oracle
    @st.cache_data(show_spinner="Cargando datos...")
    def load_data():
        query = "SELECT * FROM P_BOLSAS_EVENTOS_RELEVANTES"
        with get_oracle_connection() as conn:
            df = pd.read_sql(query, conn)
        return df

    df = load_data()

    # Convertir columnas de fechas
    for col in ["FECHA", "FPROCESO"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])

    # Sidebar de filtros
    st.sidebar.header("🔎 Filtros")

    # Filtro 1: FECHA (slider)
    if "FECHA" in df.columns:
        fecha_min = df["FECHA"].min().date()
        fecha_max = df["FECHA"].max().date()
        fecha_range = st.slider("Rango de FECHA", min_value=fecha_min, max_value=fecha_max,
                                        value=(fecha_min, fecha_max))
        df = df[(df["FECHA"] >= pd.to_datetime(fecha_range[0])) & (df["FECHA"] <= pd.to_datetime(fecha_range[1]))]

    # Filtro 2: FPROCESO (slider)
    if "FPROCESO" in df.columns:
        fproc_min = df["FPROCESO"].min().date()
        fproc_max = df["FPROCESO"].max().date()
        fproc_range = st.slider("Rango de FPROCESO", min_value=fproc_min, max_value=fproc_max,
                                        value=(fproc_min, fproc_max))
        df = df[(df["FPROCESO"] >= pd.to_datetime(fproc_range[0])) & (df["FPROCESO"] <= pd.to_datetime(fproc_range[1]))]

    # Filtro 3: CLAVE (multiselect con búsqueda)
    if "CLAVE" in df.columns:
        claves_unicas = sorted(df["CLAVE"].dropna().unique().tolist())
        claves_seleccionadas = st.sidebar.multiselect(
            "Filtrar por CLAVE",
            options=claves_unicas,
            default=claves_unicas[:10],  # solo los primeros 10 seleccionados al inicio
            help="Selecciona una o varias claves"
        )
        if claves_seleccionadas:
            df = df[df["CLAVE"].isin(claves_seleccionadas)]

    # Filtro 4: SECCION (multiselect)
    if "SECCION" in df.columns:
        secciones = sorted(df["SECCION"].dropna().unique().tolist())
        secciones_seleccionadas = st.sidebar.multiselect("Filtrar por SECCION", options=secciones, default=secciones)
        df = df[df["SECCION"].isin(secciones_seleccionadas)]

    # Filtro 5: ASUNTO (input de texto)
    if "ASUNTO" in df.columns:
        texto_asunto = st.sidebar.text_input("Buscar en ASUNTO", placeholder="Escribe una palabra clave")
        if texto_asunto:
            df = df[df["ASUNTO"].str.contains(texto_asunto, case=False, na=False)]

    # Filtro 6: ORIGEN (checkbox múltiples)
    if "ORIGEN" in df.columns:
        origenes = sorted(df["ORIGEN"].dropna().unique().tolist())
        origenes_seleccionados = st.sidebar.multiselect("Filtrar por ORIGEN", options=origenes, default=origenes)
        df = df[df["ORIGEN"].isin(origenes_seleccionados)]

    # Filtro 7: FILTRO (selección única con valor por defecto)
    if "FILTRO" in df.columns:
        filtro_valores = sorted(df["FILTRO"].dropna().unique().tolist())
        origenes_seleccionados = st.sidebar.multiselect("Filtrar por FILTRO", options=filtro_valores, default=filtro_valores)
        df = df[df["FILTRO"].isin(origenes_seleccionados)]



    # Mostrar tabla filtrada
    st.markdown(f"### Resultados ({len(df)} registros encontrados)")
    st.dataframe(df, use_container_width=True)



if __name__ == "__main__":
    main()

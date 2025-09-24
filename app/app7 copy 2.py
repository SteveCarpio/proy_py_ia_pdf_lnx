# 📈 Reporting Eventos Relevantes
import streamlit as st

# ----------------------------------------
# EJECUCIÓN PRINCIPAL
# ----------------------------------------
def main():
    import pandas as pd
    from app.appOra import get_oracle_connection  # Tu módulo actualizado
    from datetime import datetime, timedelta

    st.set_page_config(page_title="Eventos Relevantes", layout="wide")
    st.title("📋 Reporte de Eventos Relevantes")

    # Cargar datos desde Oracle
    @st.cache_data(show_spinner="Cargando datos desde Oracle...")
    def load_data():
        query = "SELECT * FROM P_BOLSAS_EVENTOS_RELEVANTES"
        with get_oracle_connection() as conn:
            df = pd.read_sql(query, conn)
        return df

    df = load_data()

    # Conversión de columnas de fechas
    for col in ["FECHA", "FPROCESO"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])


    hoy = datetime.now().date()
    inicio_hoy = pd.to_datetime(hoy)
    fin_hoy = inicio_hoy + timedelta(days=1) - timedelta(seconds=1)
    df2 = df[(df["FPROCESO"] >= inicio_hoy) & (df["FPROCESO"] <= fin_hoy)]
    st.dataframe(df2, use_container_width=True)



    # ====== SIDEBAR: FILTROS ======
    st.sidebar.header("🔎 Filtros")

    # --- Filtro 1: FECHA (input de fecha manual) ---
    #if "FECHA" in df.columns:
    #    fecha_min = df["FECHA"].min().date()
    #    fecha_max = df["FECHA"].max().date()
    #    st.sidebar.subheader("📅 Rango de FECHA")
    #    fecha_inicio = st.sidebar.date_input("Desde", value=fecha_min, min_value=fecha_min, max_value=fecha_max, key="fecha_inicio")
    #    fecha_fin = st.sidebar.date_input("Hasta", value=fecha_max, min_value=fecha_min, max_value=fecha_max, key="fecha_fin")
    #    df = df[(df["FECHA"] >= pd.to_datetime(fecha_inicio)) & (df["FECHA"] <= pd.to_datetime(fecha_fin))]

    # --- Filtro 2: FPROCESO (input de fecha manual) ---

    # --- Filtro 2: FPROCESO (input de fecha manual corregido) ---
    if "FPROCESO" in df.columns:
        fproc_min = df["FPROCESO"].min().date()
        fproc_max = df["FPROCESO"].max().date()
        st.sidebar.subheader("🗓️ Rango de FPROCESO")
        fproc_inicio = st.sidebar.date_input("Desde", value=fproc_max, min_value=fproc_min, max_value=fproc_max, key="fproc_inicio")
        fproc_fin = st.sidebar.date_input("Hasta", value=fproc_max, min_value=fproc_min, max_value=fproc_max, key="fproc_fin")

        # Ajuste para incluir todo el día seleccionado
        fproc_fin_dt = pd.to_datetime(fproc_fin) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
        df = df[(df["FPROCESO"] >= pd.to_datetime(fproc_inicio)) & (df["FPROCESO"] <= fproc_fin_dt)]


    # --- Filtro 3: CLAVE (multiselect con búsqueda eficiente) ---
    if "CLAVE" in df.columns:
        claves_unicas = sorted(df["CLAVE"].dropna().unique().tolist())
        claves_seleccionadas = st.sidebar.multiselect(
            "🔑 CLAVE",
            options=claves_unicas,
            default=claves_unicas[:10],  # Solo algunos seleccionados por defecto
            help="Selecciona una o varias claves"
        )
        if claves_seleccionadas:
            df = df[df["CLAVE"].isin(claves_seleccionadas)]

    # --- Filtro 4: SECCION (multiselect con todos seleccionados) ---
    if "SECCION" in df.columns:
        secciones = sorted(df["SECCION"].dropna().unique().tolist())
        secciones_seleccionadas = st.sidebar.multiselect("📚 SECCION", options=secciones, default=secciones)
        df = df[df["SECCION"].isin(secciones_seleccionadas)]

    # --- Filtro 5: ASUNTO (texto libre) ---
    if "ASUNTO" in df.columns:
        texto_asunto = st.sidebar.text_input("📝 Buscar en ASUNTO", placeholder="Escribe una palabra clave...")
        if texto_asunto:
            df = df[df["ASUNTO"].str.contains(texto_asunto, case=False, na=False)]

    # --- Filtro 6: ORIGEN (2 opciones, ambas activas por defecto) ---
    if "ORIGEN" in df.columns:
        origenes = sorted(df["ORIGEN"].dropna().unique().tolist())
        origenes_seleccionados = st.sidebar.multiselect("🌍 ORIGEN", options=origenes, default=origenes)
        df = df[df["ORIGEN"].isin(origenes_seleccionados)]

    # Filtro 7: FILTRO (selección única con valor por defecto)
    if "FILTRO" in df.columns:
        filtro_valores = sorted(df["FILTRO"].dropna().unique().tolist())
        origenes_seleccionados = st.sidebar.multiselect("Filtrar por FILTRO", options=filtro_valores, default=filtro_valores)
        df = df[df["FILTRO"].isin(origenes_seleccionados)]

    # ====== RESULTADOS ======
    st.markdown(f"### 🧾 Resultados: {len(df)} registros encontrados )")
    st.dataframe(df, use_container_width=True)




if __name__ == "__main__":
    main()

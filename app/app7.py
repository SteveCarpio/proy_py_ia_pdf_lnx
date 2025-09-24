# 📈 Reporting Eventos Relevantes
import streamlit as st

# ----------------------------------------
# EJECUCIÓN PRINCIPAL
# ----------------------------------------
def main():
    import pandas as pd
    from app.appOra import get_oracle_connection
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

    # ✅ Cargar y convertir fechas antes de cualquier filtrado
    df = load_data()

    for col in ["FECHA", "FPROCESO"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])

    # ====== SIDEBAR: FILTROS ======
    st.sidebar.header("🔎 Filtros")

    # --- Filtro 1: FPROCESO (input de fecha manual corregido) ---
    if "FPROCESO" in df.columns:
        fproc_min = df["FPROCESO"].min().date()
        fproc_max = df["FPROCESO"].max().date()
        st.sidebar.subheader("🗓️ Rango de FPROCESO")
        fproc_inicio = st.sidebar.date_input("Desde", value=fproc_max, min_value=fproc_min, max_value=fproc_max, key="fproc_inicio")
        fproc_fin = st.sidebar.date_input("Hasta", value=fproc_max, min_value=fproc_min, max_value=fproc_max, key="fproc_fin")

        # ✅ Ajuste para incluir todo el día de la fecha final
        fproc_fin_dt = pd.to_datetime(fproc_fin) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
        df = df[(df["FPROCESO"] >= pd.to_datetime(fproc_inicio)) & (df["FPROCESO"] <= fproc_fin_dt)]


    # --- Filtro 2: CLAVE (sin filtro por defecto) ---
    if "CLAVE" in df.columns:
        claves_unicas = sorted(df["CLAVE"].dropna().unique().tolist())
        claves_seleccionadas = st.sidebar.multiselect(
            "🔑 CLAVE",
            options=claves_unicas,
            help="Selecciona una o varias claves"
        )
        if claves_seleccionadas:
            df = df[df["CLAVE"].isin(claves_seleccionadas)]


    # --- Filtro 3: SECCION (multiselect con todos seleccionados) ---
    if "SECCION" in df.columns:
        secciones = sorted(df["SECCION"].dropna().unique().tolist())
        secciones_seleccionadas = st.sidebar.multiselect("📚 SECCION", options=secciones)
        if secciones_seleccionadas:
            df = df[df["SECCION"].isin(secciones_seleccionadas)]


    # --- Filtro 4: ASUNTO (texto libre) ---
    if "ASUNTO" in df.columns:
        texto_asunto = st.sidebar.text_input("📝 Buscar en ASUNTO", placeholder="Escribe una palabra clave...")
        if texto_asunto:
            df = df[df["ASUNTO"].str.contains(texto_asunto, case=False, na=False)]

    # --- Filtro 5: ORIGEN (2 opciones, ambas activas por defecto) ---
    if "ORIGEN" in df.columns:
        origenes = sorted(df["ORIGEN"].dropna().unique().tolist())
        origenes_seleccionados = st.sidebar.multiselect("🌍 ORIGEN", options=origenes, default=origenes)
        df = df[df["ORIGEN"].isin(origenes_seleccionados)]

    # --- Filtro 6: FILTRO (multiselect con todos activos por defecto) ---
    if "FILTRO" in df.columns:
        filtro_valores = sorted(df["FILTRO"].dropna().unique().tolist())
        filtros_seleccionados = st.sidebar.multiselect("⚙️ FILTRO", options=filtro_valores, default=filtro_valores)
        df = df[df["FILTRO"].isin(filtros_seleccionados)]

    # ====== RESULTADOS ======
    st.markdown(f"### 🧾 Resultados: {len(df)} registros encontrados")
    #st.dataframe(df, use_container_width=True)

    # 👉 Reordenar columnas y ocultar 'FECHA'
    columnas_principales = ["N", "FPROCESO", "ORIGEN", "CLAVE", "SECCION"]
    columnas_ocultas = ["FECHA", "T", "NOTA", "FILTRO"]

    # Asegurar que las columnas existen antes de ordenar
    columnas_principales = [col for col in columnas_principales if col in df.columns]
    columnas_ocultas = [col for col in columnas_ocultas if col in df.columns]

    # Columnas restantes (excluyendo ocultas y principales)
    columnas_restantes = [col for col in df.columns if col not in columnas_principales + columnas_ocultas]

    # Nueva ordenación final
    columnas_ordenadas = columnas_principales + columnas_restantes

    # Mostrar DataFrame con columnas reordenadas y 'FECHA' oculta
    st.dataframe(df[columnas_ordenadas], use_container_width=True)


if __name__ == "__main__":
    main()

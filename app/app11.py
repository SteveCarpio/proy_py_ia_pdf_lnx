# 📈 Reporting Eventos Relevantes

# ----------------------------------------
# EJECUCIÓN PRINCIPAL
# ----------------------------------------
def main():
    import pandas as pd
    from app.appOra import get_oracle_connection
    from datetime import datetime, timedelta
    import plotly.express as px
    import time
    import streamlit as st

    st.title("📈 Reporte de Estados Financieros")
    st.caption("Se extraerán datos de la BBDD de Histórica de Estados Financieros a un DataFrame dinámico. (app11.py)")
    st.sidebar.subheader("📈 : Eventos Relevantes")

    # ==========================
    #     CARGA DE DATOS
    # ==========================
    @st.cache_data(show_spinner="Cargando datos desde Oracle...")
    def load_data():
        start = time.time()
        query = "SELECT * FROM P_CNBV_EEFF_TOTALES2"
        with get_oracle_connection() as conn:
            df = pd.read_sql(query, conn)
        st.write("Tiempo carga Oracle:", time.time() - start)

        # Convertir fechas UNA sola vez
        for col in ["FEnvio"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        return df

    if st.sidebar.button("🔄 Recargar datos"):
        st.cache_data.clear()

    df = load_data()

    # ==========================
    #       FILTROS
    # ==========================
    mask = pd.Series(True, index=df.index)

    # PERIODO
    if "PERIODO" in df.columns:
        claves_unicas = sorted(df["PERIODO"].dropna().unique().tolist())
        claves_seleccionadas = st.sidebar.multiselect("📅 PERIODO", options=claves_unicas)
        if claves_seleccionadas:
            mask &= df["PERIODO"].isin(claves_seleccionadas)

    # CLAVE PIZARRA
    if "CLAVEPIZARRA" in df.columns:
        secciones = sorted(df["CLAVEPIZARRA"].dropna().unique().tolist())
        secciones_seleccionadas = st.sidebar.multiselect("🔑 CLAVEPIZARRA", options=secciones)
        if secciones_seleccionadas:
            mask &= df["CLAVEPIZARRA"].isin(secciones_seleccionadas)



    # Aplicar todos los filtros a la vez
    df = df[mask]

    # ==========================
    #       RESULTADOS
    # ==========================
    st.markdown(f"### 🧾 Resultados: {len(df)} registros encontrados")

    # 'IDEN', '', 'TAXONOMIA'
    columnas_principales = ['PERIODO', 'CLAVEPIZARRA', 'FENVIO', 'TACTIVOS', 'TACTIVOSCIRCULANTES', 'TCAPITALCONTABLE', 'TPASIVOSCIRCULANTES', 'TPASIVOS', 'UTILPERDOPERACION', 'UTILPERDNETA']
    df_ordenado = df[columnas_principales].copy()
    df_ordenado['FENVIO'] = df_ordenado['FENVIO'].dt.date

    # Prepara tabla para una salida con valores ordenados
    df_final = df_ordenado.copy()  

    # Ordena por las columnas indicadas
    df_final = df_final.sort_values(
        by=['PERIODO', 'CLAVEPIZARRA', 'FENVIO'],
        ascending=[False, True, True]   #  False=descending | True=ascending
    ) 

    # Crear Totales
    total_general1 = df_final['TACTIVOS'].sum()
    total_general2 = df_final['TACTIVOSCIRCULANTES'].sum()
    total_general3 = df_final['TCAPITALCONTABLE'].sum()
    total_general4 = df_final['TPASIVOSCIRCULANTES'].sum()
    total_general5 = df_final['TPASIVOS'].sum()
    total_general6 = df_final['UTILPERDOPERACION'].sum()
    total_general7 = df_final['UTILPERDNETA'].sum()

    # Añadir una fila “TOTAL” al DataFrame original
    row_total = pd.DataFrame({
        'PERIODO': ['TOTAL'],
        'TACTIVOS': [total_general1],
        'TACTIVOSCIRCULANTES': [total_general2],
        'TCAPITALCONTABLE': [total_general3],
        'TPASIVOSCIRCULANTES': [total_general4],
        'TPASIVOS': [total_general5],
        'UTILPERDOPERACION': [total_general6],
        'UTILPERDNETA': [total_general7]
    })
    df_totales = pd.concat([df_final, row_total], ignore_index=True)

    # Separdor de miles a todos los campos numericos 
    def formatear_importes(df):
            for col in df.select_dtypes(include=["int", "float"]).columns:
                df[col] = df[col].apply(lambda x: f"{x:,.0f}".replace(",", "."))
            return df
    df_totales = formatear_importes(df_totales)

    # sombrear el campo total
    def highlight_total(row):
            if row['PERIODO'] == 'TOTAL':
                return ['background-color: #f8f8f8']*row.shape[0]
            return ['']*row.shape[0]
    df_totales = df_totales.style.apply(highlight_total, axis=1)

    # Visulizar la tabla
    with st.expander("📜 Listado de Datos:"):
        st.dataframe(df_totales)


    # ==========================
    #      VISUALIZACIONES
    # ==========================


    with st.expander("📊 Visualizaciones:"):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.caption("En construcción")
            
        with col2:
            st.caption("En construcción")


if __name__ == "__main__":
    main()

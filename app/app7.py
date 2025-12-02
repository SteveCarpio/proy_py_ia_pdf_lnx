# 📈 Reporting Eventos Relevantes

# ----------------------------------------
# EJECUCIÓN PRINCIPAL
# ----------------------------------------
def main():
    import pandas as pd
    from dateutil.relativedelta import relativedelta
    from app.appOra import get_oracle_connection
    from datetime import datetime, timedelta
    import plotly.express as px
    import time
    import streamlit as st
    from io import BytesIO

    st.title("📈 Reporte de Eventos Relevantes")
    st.caption("Se extraerán datos de la BBDD de Histórica de Eventos Relevantes en un DataFrame dinámico. (app7.py)")
    st.sidebar.subheader("📈 : Eventos Relevantes")
    st.sidebar.caption("  ")

    # ==========================
    #     FUNCIONES VARIAS
    # ==========================

    # Función para Cargar Datos de Oracle
    @st.cache_data(show_spinner="Cargando datos desde Oracle...")
    def load_data():
        start = time.time()
        query = "SELECT * FROM P_BOLSAS_EVENTOS_RELEVANTES"
        with get_oracle_connection() as conn:
            df = pd.read_sql(query, conn)
        #st.write("Tiempo carga Oracle:", time.time() - start)

        # Convertir fechas UNA sola vez
        for col in ["FECHA", "FPROCESO"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        return df
    
    # Función para descargar fichero excel
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        return output.getvalue()

    # ===============================
    #       INICIO DEL PROGRAMA
    # ===============================

    df = load_data()

    # ==========================
    #       FILTROS
    # ==========================
    mask = pd.Series(True, index=df.index)

    # FPROCESO
    if "FPROCESO" in df.columns:
        fproc_min = df["FPROCESO"].min().date()
        fproc_max = df["FPROCESO"].max().date()
        coldate1, coldate2 = st.sidebar.columns(2)
        with coldate1:
            fproc_inicio = st.date_input("📅 Desde", value=fproc_max, min_value=fproc_min, max_value=fproc_max, help="Histórico desde: 2020/01/02")
        with coldate2:
            fproc_fin    = st.date_input("📅 Hasta", value=fproc_max, min_value=fproc_min, max_value=fproc_max)

        fproc_fin_dt = pd.to_datetime(fproc_fin) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
        mask &= (df["FPROCESO"] >= pd.to_datetime(fproc_inicio)) & (df["FPROCESO"] <= fproc_fin_dt)

    # CLAVE
    if "CLAVE" in df.columns:
        claves_unicas = sorted(df["CLAVE"].dropna().unique().tolist())
        claves_seleccionadas = st.sidebar.multiselect("🔑 CLAVE", options=claves_unicas)
        if claves_seleccionadas:
            mask &= df["CLAVE"].isin(claves_seleccionadas)

    # SECCION
    if "SECCION" in df.columns:
        secciones = sorted(df["SECCION"].dropna().unique().tolist())
        secciones_seleccionadas = st.sidebar.multiselect("📚 SECCION", options=secciones)
        if secciones_seleccionadas:
            mask &= df["SECCION"].isin(secciones_seleccionadas)

    # ASUNTO
    if "ASUNTO" in df.columns:
        texto_asunto = st.sidebar.text_input("📝 Buscar en ASUNTO", placeholder="Escribe una palabra clave...")
        if texto_asunto:
            mask &= df["ASUNTO"].str.contains(texto_asunto, case=False, na=False)

    # ORIGEN
    if "ORIGEN" in df.columns:
        origenes = sorted(df["ORIGEN"].dropna().unique().tolist())
        origenes_seleccionados = st.sidebar.multiselect("🌍 ORIGEN", options=origenes, default=origenes)
        mask &= df["ORIGEN"].isin(origenes_seleccionados)

    # FILTRO
    if "FILTRO" in df.columns:
        filtro_valores = sorted(df["FILTRO"].dropna().unique().tolist())
        filtros_seleccionados = st.sidebar.multiselect("⚙️ FILTRO", options=filtro_valores, default=filtro_valores)
        mask &= df["FILTRO"].isin(filtros_seleccionados)

    # Aplicar todos los filtros a la vez
    df = df[mask]

    # ==========================
    #       RESULTADOS
    # ==========================
    #st.markdown(f"### 🧾 Resultados: {len(df)} registros encontrados")

    columnas_principales = ["FECHA", "ORIGEN", "CLAVE", "SECCION", "ASUNTO", "URL", "ARCHIVO"]
    df_ordenado = df[columnas_principales].copy()

    df_ordenado['FECHA'] = df_ordenado['FECHA'].dt.date

    # Vectorización para enlaces (más rápido que apply)
    df_ordenado["URL"] = df_ordenado["URL"].where(
        ~df_ordenado["URL"].astype(str).str.contains("https", na=False),
        '<a href="' + df_ordenado["URL"].astype(str) + '" target="_blank">Click aquí</a>'
    )
    df_ordenado["ARCHIVO"] = df_ordenado["ARCHIVO"].where(
        ~df_ordenado["ARCHIVO"].astype(str).str.contains("https", na=False),
        '<a href="' + df_ordenado["ARCHIVO"].astype(str) + '" target="_blank">Click aquí</a>'
    )

    # Prepara tabla para una salida con valores ordenados
    df_final = df_ordenado.copy()  

     # Ordena por las columnas indicadas
    df_final = df_final.sort_values(
        by=['FECHA', 'ORIGEN', 'CLAVE', 'SECCION', 'ASUNTO'],
        ascending=[False, True, True, True, True]   #  False=descending | True=ascending
    ) 

    # ==========================
    #    MOSTRAR TABLA HTML
    # ==========================
    # --- 🎨 CSS personalizado ---
    st.markdown("""
    <style>
    /* Centrar los nombres de las columnas y cambiar color */
    table thead th {
        text-align: center !important;
        background-color: #ff7518;  /* 💡 color de fondo Multiva */
        color: white;               /* 💡 color del texto */
        padding: 8px;
    }

    /* Ajustar ancho de la columna FECHA */
    table td:nth-child(1), table th:nth-child(1) {
        min-width: 20px;            /* más ancho para evitar salto de línea */
        white-space: nowrap;        /* no dividir en dos líneas */
    }

    /* Ajustar ancho de la columna URL */
    table td:nth-child(6), table th:nth-child(6) {
        min-width: 20px;            /* más ancho para evitar salto de línea */
        white-space: nowrap;        /* no dividir en dos líneas */
    }

    /* Ajustar ancho de la columna ARCHIVO */
    table td:nth-child(7), table th:nth-child(7) {
        min-width: 20px;            /* más ancho para evitar salto de línea */
        white-space: nowrap;        /* no dividir en dos líneas */
    }

    /* Estilo general de la tabla */
    table {
        width: 100%;
        border-collapse: collapse;
    }

    td, th {
        border: 1px solid #ddd;
        padding: 6px;
    }
    a {
        color: #1a73e8;
        text-decoration: underline;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)
    


    with st.container():
        col1, col2, col3 = st.columns([2,1,2])
        with col1:
            st.subheader("📜 Listado de Datos")
        with col2:
            st.metric("Núm.Registros", len(df_final))
        with col3:
            xxx, btn_col1, btn_col2 = st.columns([6,1,1])
            with btn_col1:
                if st.button("🔄", help="Recargar datos de Oracle"):
                    st.rerun()
            with btn_col2:
                st.download_button(
                    label="📥",
                    data=to_excel(df_final),
                    file_name="EventosRelevantes.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    help=f"Descargar los {len(df_final)} registros a Excel"
                )




    #  Si el intervalo entre la fecha 'Desde' y 'Hasta' es inferior a 1 mes, la tabla se muestra en un formato o otro.
    hace_N_meses  = datetime.now() - relativedelta(months=1) 
    fproc_inicio_dt = datetime.combine(fproc_inicio, datetime.min.time())
    if fproc_inicio_dt < hace_N_meses:
        st.dataframe(df_final)
        st.caption("** Si el intervalo entre la fecha 'Desde' y 'Hasta' es inferior a 1 mes, la tabla se muestra en este formato por temas de rendimiento.")
    else:
        st.markdown(df_final.to_html(escape=False, index=False),unsafe_allow_html=True)

    # ==========================
    #      VISUALIZACIONES
    # ==========================
    df_final['FECHA'] = pd.to_datetime(df_final['FECHA'], format='%Y-%m-%d')
    biva_df = df_final[df_final['ORIGEN'] == 'BIVA']
    bmv_df = df_final[df_final['ORIGEN'] == 'BMV']

    num_total = len(df_final)
    num_biva = len(biva_df)
    num_bmv = len(bmv_df)
    origen_counts = df_final['ORIGEN'].value_counts()

    fig_pie = px.pie(origen_counts, names=origen_counts.index, values=origen_counts.values, title=' ')

    with st.expander("📊 Visualizaciones:"):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.metric(label="Número de Eventos Filtrados:", value=num_total)
            st.metric(label="BIVA", value=num_biva)
            st.metric(label="BMV", value=num_bmv)
            
        with col2:
            st.plotly_chart(fig_pie)

        biva_fecha_counts = biva_df.groupby(pd.Grouper(key='FECHA', freq='D')).size().reset_index()
        bmv_fecha_counts  = bmv_df.groupby(pd.Grouper(key='FECHA', freq='D')).size().reset_index()
        biva_fecha_counts.columns = ['FECHA', 'BIVA']
        bmv_fecha_counts.columns  = ['FECHA', 'BMV']
        merged_df = pd.merge(biva_fecha_counts, bmv_fecha_counts, on='FECHA', how='outer').fillna(0)

        fig = px.bar(merged_df, x='FECHA', y=['BIVA', 'BMV'], title='Número de Eventos Relevantes por Bolsas')
        fig.update_yaxes(title_text=" ")
        fig.update_xaxes(title_text=" ")
        st.plotly_chart(fig)


if __name__ == "__main__":
    main()

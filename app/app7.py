# 📈 Reporting Eventos Relevantes
import streamlit as st

# ----------------------------------------
# EJECUCIÓN PRINCIPAL
# ----------------------------------------
def main():
    import pandas as pd
    from app.appOra import get_oracle_connection
    from datetime import datetime, timedelta
    import plotly.express as px

    st.title("📈 Reporte de Eventos Relevantes")
    st.caption("Se extraerán datos de la BBDD de Histórica de Eventos Relevantes en un DataFrame dinámico")
    st.sidebar.subheader("📈 : Eventos Relevantes")

    # Cargar datos desde Oracle
    @st.cache_data(show_spinner="Cargando datos desde Oracle...")
    def load_data():
        query = "SELECT * FROM P_BOLSAS_EVENTOS_RELEVANTES"
        with get_oracle_connection() as conn:
            df = pd.read_sql(query, conn)
        return df

    if st.sidebar.button("🔄 Recargar datos"):
        st.cache_data.clear()

    # ✅ Cargar y convertir fechas antes de cualquier filtrado
    df = load_data()

    for col in ["FECHA", "FPROCESO"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])

    # ====== SIDEBAR: FILTROS ======
    #st.sidebar.header("🔎 Filtros")

    # --- Filtro 1: FPROCESO (input de fecha manual corregido) ---
    if "FPROCESO" in df.columns:
        fproc_min = df["FPROCESO"].min().date()
        fproc_max = df["FPROCESO"].max().date()
        #st.sidebar.subheader("🗓️ Rango de FPROCESO")
        fproc_inicio = st.sidebar.date_input("📅 FPROCESO: Desde", value=fproc_max, min_value=fproc_min, max_value=fproc_max, key="fproc_inicio")
        fproc_fin = st.sidebar.date_input("📅 FPROCESO: Hasta", value=fproc_max, min_value=fproc_min, max_value=fproc_max, key="fproc_fin")

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

    # Reordenar columnas y mostrar solo las que quiero
    columnas_principales = ["FECHA", "ORIGEN", "CLAVE", "SECCION", "ASUNTO", "URL", "ARCHIVO"]

    # Creo un nuevo DF con los campos que quiero y ordenados
    df_ordenado = df[columnas_principales]

    # Formatear campos de salida: 
    df_ordenado['FECHA'] = df_ordenado['FECHA'].dt.date  # FECHA solo AAAA-MM-DD


    #st.dataframe(df_ordenado, use_container_width=True)

    ########################



    def make_link(x):
        if isinstance(x, str) and "https" in x:
            return f'<a href="{x}" target="_blank">Click aquí</a> '
        return x

    df_ordenado["URL"] = df_ordenado["URL"].apply(make_link)
    df_ordenado["ARCHIVO"] = df_ordenado["ARCHIVO"].apply(make_link)



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

    # Mostrar la TABLA DE DATOS
    with st.expander("📜 Listado de Datos:"):
        # --- 💅 Mostrar DataFrame como HTML con enlaces activos ---
        st.markdown(
            df_ordenado.to_html(escape=False, index=False),
            unsafe_allow_html=True
        )

     # Mostrar la VISUALIZACIONES

    # Df de apoyo
    df_ordenado['FECHA'] = pd.to_datetime(df_ordenado['FECHA'], format='%Y-%m-%d')    # Convertir la columna 'FECHA' a formato datetime
    biva_df = df_ordenado[df_ordenado['ORIGEN'] == 'BIVA']                            # df BIVA
    bmv_df = df_ordenado[df_ordenado['ORIGEN'] == 'BMV']                              # df de BMV


    # Contadores
    num_total = len(df_ordenado)
    num_biva=len(biva_df)
    num_bmv=len(bmv_df)
    origen_counts = df_ordenado['ORIGEN'].value_counts() # Contar los valores únicos en la columna 'ORIGEN'

    # Gráfico de tarta
    fig_pie = px.pie(origen_counts, names=origen_counts.index, values=origen_counts.values, title=' ')

    # Mostrar EXTENDER
    with st.expander("📊 Visualizaciones:"):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.metric(label="Número de Evento Filtrados:", value=num_total)
            st.metric(label="BIVA", value=num_biva)
            st.metric(label="BMV", value=num_bmv)
        with col2:
            st.plotly_chart(fig_pie)

        # Grafico de Lineal
        biva_fecha_counts = biva_df.groupby(pd.Grouper(key='FECHA', freq='D')).size().reset_index() # Agrupar x fecha y contar el -
        bmv_fecha_counts = bmv_df.groupby(pd.Grouper(key='FECHA', freq='D')).size().reset_index()   # num de eventos x cada origen
        biva_fecha_counts.columns = ['FECHA', 'BIVA'] # Renombrar las columnas para claridad 
        bmv_fecha_counts.columns = ['FECHA', 'BMV']   # Renombrar las columnas para claridad
        merged_df = pd.merge(biva_fecha_counts,bmv_fecha_counts, on='FECHA') # Combinar los datos de BMV y BIVA por fecha
        fig = px.bar(merged_df, 
             x='FECHA', 
             y=['BIVA', 'BMV'], 
             title='Número de Eventos Relevantes por Bolsas',
             labels={'variable': 'Bolsas'})  # Titulo de leyenda

        fig.update_yaxes(title_text=" ")     # Titulo de eje Y
        fig.update_xaxes(title_text=" ")     # Titulo de eje X

        st.plotly_chart(fig)


if __name__ == "__main__":
    main()

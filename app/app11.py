# 📈 Reporting Estados Financieros
def main():
    import io
    import time
    import pandas as pd
    import streamlit as st
    import plotly.express as px
    from app.appOra import get_oracle_connection
    from datetime import datetime, timedelta
        
    # ----------------------------------------
    # FUNCIONES DE APOYO
    # ----------------------------------------

    # Carga de datos
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

    # Convertir valores a MILLONES, TRILLONES, etc,,,
    def human_format(num):
        num = float(num)
        for unit in ['', 'K', 'M', 'B', 'T']:
            if abs(num) < 1000:
                return f"{num:,.0f}{unit}".replace(",", ".")
            num /= 1000
        return f"{num:.1f}P"

    # Separdor de miles a todos los campos numericos 
    def formatear_importes(df):
        for col in df.select_dtypes(include=["int", "float"]).columns:
            df[col] = df[col].apply(lambda x: f"{x:,.0f}".replace(",", "."))
        return df

    # Sombrear el campo total
    def highlight_total(row):
        if row['PERIODO'] == 'TOTAL':
            return ['background-color: #EEEEEE ']*row.shape[0]   # #D3D3D3  # muy_claro: f8f8f8
        return ['']*row.shape[0]

    # Diseño de metricas
    def diseno_metricas():
        return """
        <style>
        .card{
            padding:10px;
            background:#1f2937;
            border-radius:8px;
            color:white;
            font-size:1.5rem;
            text-align:right;
            width:100%;
            min-height:110px;
            box-sizing:border-box;
            display:flex;
            flex-direction:column;
            justify-content:space-between;
        }
        /* <--- Cambios aquí --->
        Se elimina white-space, overflow y text‑overflow
        */
        .card-title{
            font-size:0.7rem;
            opacity:0.8;
            text-align:left;
            /* Si el texto sigue muy largo, añade: */
            word-wrap:break-word;      /* rompe la palabra si es necesario */
            /* o bien: */
            /* overflow-wrap:break-word; */
        }
        </style>
        """

    # ==========================
    #       INICIO 
    # ==========================
    st.title("📈 Reporte de Estados Financieros")
    st.caption("Se extraerán datos de la BBDD de Histórica de Estados Financieros a un DataFrame dinámico. (app11.py)")
    st.sidebar.subheader("📈 : Eventos Relevantes")

    # ==========================
    #       SIDEBAR FILTROS
    # ==========================

    # BOTON: RECARGAR DATOS
    if st.sidebar.button("🔄 Recargar datos"):
        st.cache_data.clear()
    df = load_data()
   
    # Acumulador de opciones de Filtros
    mask = pd.Series(True, index=df.index)

    # MULTISELECT: PERIODO
    if "PERIODO" in df.columns:
        claves_unicas = sorted(df["PERIODO"].dropna().unique().tolist())
        claves_maxima = max(claves_unicas)
        claves_seleccionadas = st.sidebar.multiselect("📅 PERIODO", options=claves_unicas, default=claves_maxima)
        if claves_seleccionadas:
            mask &= df["PERIODO"].isin(claves_seleccionadas)

    # MULTISELECT: CLAVE PIZARRA
    if "CLAVEPIZARRA" in df.columns:
        secciones = sorted(df["CLAVEPIZARRA"].dropna().unique().tolist())
        secciones_seleccionadas = st.sidebar.multiselect("🔑 CLAVEPIZARRA", options=secciones)
        if secciones_seleccionadas:
            mask &= df["CLAVEPIZARRA"].isin(secciones_seleccionadas)

    # Aplicar todos los filtros del acumulador
    df = df[mask]

    # BOTON: DESCARGA DATAFRAME FILTRADO TO EXCEL
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False, engine='openpyxl')  # openpyxl es el engine recomendado
    buffer.seek(0)  # Volver al inicio del buffer
    st.sidebar.download_button(
        label="📥 Descargar -> Excel",
        data=buffer,
        file_name="EstadosFinancieros.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    # ==========================
    #       MAIN WEB 
    # ==========================

    # Preparación de los datos: no se incluyen: IDEN, TAXONOMIA
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

    # Crear variables con los totales
    total_general1 = df_final['TACTIVOS'].sum()
    total_general2 = df_final['TACTIVOSCIRCULANTES'].sum()
    total_general3 = df_final['TCAPITALCONTABLE'].sum()
    total_general4 = df_final['TPASIVOSCIRCULANTES'].sum()
    total_general5 = df_final['TPASIVOS'].sum()
    total_general6 = df_final['UTILPERDOPERACION'].sum()
    total_general7 = df_final['UTILPERDNETA'].sum()

    # Crear diccionario para las metricas
    dic_totales = {
    "Número de Registros " : len(df),
    "Total Activos ": total_general1,
    "Total Activos Circulantes": total_general2,
    "Total Capital Contable": total_general3,
    "Total Pasivos Circulantes": total_general4,
    "Total Pasivos ": total_general5,
    "Utilidad (pérdida) Operación": total_general6,
    "Utilidad (pérdida) Neta": total_general7
    }

    # Añadir una fila “TOTAL” al final del DataFrame  de salida
    row_total = pd.DataFrame({
        'PERIODO': ['TOTAL'],
        'CLAVEPIZARRA': [' '],
        'FENVIO': [' '],
        'TACTIVOS': [total_general1],
        'TACTIVOSCIRCULANTES': [total_general2],
        'TCAPITALCONTABLE': [total_general3],
        'TPASIVOSCIRCULANTES': [total_general4],
        'TPASIVOS': [total_general5],
        'UTILPERDOPERACION': [total_general6],
        'UTILPERDNETA': [total_general7]
    })
    df_totales = pd.concat([df_final, row_total], ignore_index=True)

    # Reiniciar el número de índice al valor 1
    df_totales.index = df_totales.index + 1
    
    # Poner los valores con separdor de miles a todas las variables numericas
    df_totales = formatear_importes(df_totales)
    
    # Renombrar nombres de los campos del dataframe a visualizar
    nuevos_nombres = {
        'CLAVEPIZARRA': 'ClavePizarra',
        'FENVIO':'FechaEnvio',
        'TACTIVOS':'TActivos',
        'TACTIVOSCIRCULANTES':'TActivosCirculantes',
        'TCAPITALCONTABLE':'TCapitalContable',
        'TPASIVOSCIRCULANTES':'TPasivosCirculantes',
        'TPASIVOS':'TPasivos',
        'UTILPERDOPERACION':'UtilPerdOperacion',
        'UTILPERDNETA':'UtilPerdNeta'
    }
    df_visualizar = df_totales.rename(columns=nuevos_nombres)

    # sombrear el registro nuevo creado con los totales
    df_visualizar = df_visualizar.style.apply(highlight_total, axis=1)


    # ==========================
    #       WIDGETS MAIN 
    # ==========================

    # APARTADO 1: Metricas con diseño html
    card_style = diseno_metricas()
    st.markdown(card_style, unsafe_allow_html=True)
    cols = st.columns(8)
    for i, (label, value) in enumerate(dic_totales.items()):
        with cols[i % 8]:
            st.markdown(f"""
            <div class="card">
                <div class="card-title">{label}</div>
                {human_format(value)}
            </div>
            """, unsafe_allow_html=True)

    # APARTADO 2: Visualización de la tabla 
    st.write(" ")
    st.dataframe(df_visualizar)

    # APARTADO 3: Gráficos
    with st.expander("📊 Visualizaciones:"):

        df_pct = df_final.copy()

        cols_valores = [
            'TACTIVOS', 'TACTIVOSCIRCULANTES', 'TCAPITALCONTABLE',
            'TPASIVOSCIRCULANTES', 'TPASIVOS', 'UTILPERDOPERACION', 'UTILPERDNETA'
        ]

        # Convertir a % del total por campo
        for col in cols_valores:
            df_pct[col] = (df_final[col] / df_final[col].sum()) * 100

        # Filtrar solo columnas necesarias para el gráfico
        fig1 = px.bar(
            df_pct,
            x='PERIODO',
            y=['TACTIVOS', 'TACTIVOSCIRCULANTES', 'TCAPITALCONTABLE', 'TPASIVOSCIRCULANTES', 'TPASIVOS', 'UTILPERDOPERACION', 'UTILPERDNETA'],
            color='CLAVEPIZARRA',
            barmode='group',
            title="Porcentaje de TACTIVOS , TACTIVOSCIRCULANTES por Periodo y Clave Pizarra (%)"
        )
        fig1.update_layout(yaxis_title="% del total")
        st.plotly_chart(fig1, use_container_width=True)

        df_g2 = df_pct.groupby('CLAVEPIZARRA')[['TACTIVOS', 'TACTIVOSCIRCULANTES', 'TCAPITALCONTABLE', 'TPASIVOSCIRCULANTES', 'TPASIVOS', 'UTILPERDOPERACION', 'UTILPERDNETA']].sum().reset_index()
        fig2 = px.bar(
            df_g2,
            x='CLAVEPIZARRA',
            y=['TACTIVOS', 'TACTIVOSCIRCULANTES', 'TCAPITALCONTABLE', 'TPASIVOSCIRCULANTES', 'TPASIVOS', 'UTILPERDOPERACION', 'UTILPERDNETA'],
            barmode='group',
            title="Totales por Clave Pizarra expresados como % del total"
        )
        fig2.update_layout(yaxis_title="% del total")
        st.plotly_chart(fig2, use_container_width=True)

if __name__ == "__main__":
    main()

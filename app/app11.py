# 📈 Reporting Eventos Relevantes
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

# sombrear el campo total
def highlight_total(row):
    if row['PERIODO'] == 'TOTAL':
        return ['background-color: #f8f8f8']*row.shape[0]
    return ['']*row.shape[0]

# ----------------------------------------
# EJECUCIÓN PRINCIPAL
# ----------------------------------------
def main():
    st.title("📈 Reporte de Estados Financieros")
    st.caption("Se extraerán datos de la BBDD de Histórica de Estados Financieros a un DataFrame dinámico. (app11.py)")
    st.sidebar.subheader("📈 : Eventos Relevantes")

    # ==========================
    #       SIDEBAR FILTROS
    # ==========================

    # BOTON: recargar datos
    if st.sidebar.button("🔄 Recargar datos"):
        st.cache_data.clear()
    df = load_data()
   
    # Acumulador de opciones de Filtros
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

    # Crear variables y dic de Totales
    total_general1 = df_final['TACTIVOS'].sum()
    total_general2 = df_final['TACTIVOSCIRCULANTES'].sum()
    total_general3 = df_final['TCAPITALCONTABLE'].sum()
    total_general4 = df_final['TPASIVOSCIRCULANTES'].sum()
    total_general5 = df_final['TPASIVOS'].sum()
    total_general6 = df_final['UTILPERDOPERACION'].sum()
    total_general7 = df_final['UTILPERDNETA'].sum()
    dic_totales = {
    "TACTIVOS": total_general1,
    "TACTIVOSCIRCULANTES": total_general2,
    "TCAPITALCONTABLE": total_general3,
    "TPASIVOSCIRCULANTES": total_general4,
    "TPASIVOS": total_general5,
    "UTILPERDOPERACION": total_general6,
    "UTILPERDNETA": total_general7
    }

    # Añadir una fila “TOTAL” al final del DataFrame  de salida
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
    
    # Poner los valores con separdor de miles a todas las variables numericas
    df_totales = formatear_importes(df_totales)
    
    # sombrear el registro nuevo creado con los totales
    df_totales = df_totales.style.apply(highlight_total, axis=1)


    # ==========================
    #       WIDGETS MAIN 
    # ==========================

    # APARTADO 1: Titulo de número de registros
    st.markdown(f"### 🧾 Resultados: {len(df)} registros encontrados")

    # APARTADO 2: Metricas
    cols = st.columns(7)
    for i, (label, value) in enumerate(dic_totales.items()):
        with cols[i % 7]:
            st.metric(label, human_format(value))

    # APARTADO 3: Visualización de la tabla 
    with st.expander("📜 Listado de Datos:"):
        st.dataframe(df_totales)

    # APARTADO 4: Gráficos con los datos filtrados
    with st.expander("📊 Visualizaciones:"):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.caption("En construcción")
            
        with col2:
            st.caption("En construcción")


if __name__ == "__main__":
    main()

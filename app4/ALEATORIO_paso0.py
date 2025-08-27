from app4.ALEATORIO_librerias import *
import app4.ALEATORIO_variables as sTv
import streamlit as st


def sTv_paso0():
    
    df1 = None
    file_name1 = None
    file_name2 = None

    col1, col2 = st.columns(2)
    with col1:
        # Crea un espacio para subir el archivo
        
        #st.write("<span style='color:blue; font-size:14px;'> Sube un archivo de entrada (csv, txt, excel) </span>", unsafe_allow_html=True)
        file_upload1 = st.file_uploader("Subir un archivo de entrada (CSV, TXT, EXCEL)", type=["csv", "txt", "xlsx"])
        if file_upload1 is not None:
            file_name1 = file_upload1.name
            # Lee el archivo en formato DataFrame con Pandas
            if file_upload1.name.endswith('.csv'):
                df1 = pd.read_csv(file_upload1)
            elif file_upload1.name.endswith('.txt'):
                df1 = pd.read_csv(file_upload1, delimiter='\t')  # Suponiendo que el separador es un tabulador
            elif file_upload1.name.endswith('.xlsx'):
                df1 = pd.read_excel(file_upload1)

            col1A, col1B = st.columns(2)
            with col1A:
                st.caption(f'- Número de Registros del fichero de entrada: <br> {len(df1):,.0f}', unsafe_allow_html=True)
            with col1B:
                st.caption(f'- Suma Total del fichero: <br> {df1['TOTAL'].sum():,.0f}', unsafe_allow_html=True)

    with col2:
        # Crea un espacio para subir el archivo
        file_upload2 = st.file_uploader("Subir los préstamos que no se deben incluir (CSV, TXT, EXCEL) — opcional.", type=["csv", "txt", "xlsx"])
        if file_upload2 is not None:
            file_name2 = file_upload2.name
            # Lee el archivo en formato DataFrame con Pandas
            if file_upload2.name.endswith('.csv'):
                df2 = pd.read_csv(file_upload2)
            elif file_upload2.name.endswith('.txt'):
                df2 = pd.read_csv(file_upload2, delimiter='\t')  # Suponiendo que el separador es un tabulador
            elif file_upload2.name.endswith('.xlsx'):
                df2 = pd.read_excel(file_upload2)

            col2A, col2B = st.columns(2)
            with col2A:
                st.caption(f'- Número de Registros del fichero de entrada: <br> {len(df2):,.0f}', unsafe_allow_html=True)
                st.caption(f'- Número de Registros eliminados: <br> {len(df2):,.0f}', unsafe_allow_html=True)
            with col2B:
                st.caption(f'- Importe Total Eliminado: <br> {df2['TOTAL'].sum():,.0f}', unsafe_allow_html=True)
                st.caption(f'- **(Nueva) Suma Total del fichero**: <br> {df2['TOTAL'].sum():,.0f}', unsafe_allow_html=True)

    st.markdown("---")

    ### Solicitar datos de entrada

    importe_Fijado   = 600000000     # Máximo importe total acumulado
    num_Simulaciones = 5000          # Número de Simulaciones 
    diferencia_Menor = 40            # Es el valor más bajo para crear los Excel
    diferencia_Stop  = 1.0           # Es el valor más deseable, hará un stop del proceso

    v3 = st.sidebar.slider("Importe a Buscarx:         ", importe_Fijado - (int(importe_Fijado / 10)*9), importe_Fijado * 2, step=int(importe_Fijado / 20), value=importe_Fijado)
    v4 = st.sidebar.slider("Número de Simulaciones: ", 1000, 10000, step=1000, value=num_Simulaciones)
    v5 = st.sidebar.slider(f"Diferencia Máxima:     ", 1, 100, step=1, value=diferencia_Menor)
    v6 = st.sidebar.slider(f"Diferencia Minima:      ", 0.0, 10.0, step=0.1, value=diferencia_Stop, format="%f")
 

    importe_Fijado = v3
    num_Simulaciones = v4
    diferencia_Menor = v5
    diferencia_Stop = v6

    return importe_Fijado, num_Simulaciones, diferencia_Menor, diferencia_Stop, df1, file_name1, file_name2
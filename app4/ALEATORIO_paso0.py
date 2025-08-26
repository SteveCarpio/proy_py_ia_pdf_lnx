from app4.ALEATORIO_librerias import *
import app4.ALEATORIO_variables as sTv
import streamlit as st


def sTv_paso0(importe_Fijado, num_Simulaciones, diferencia_Menor, diferencia_Stop):
    #st.write('2 - Introducir los Valores que usará el modelo ')

    # Solicitar datos de entrada
    
    # Crear dos columnas
    col1, col2 = st.columns(2)

    # Colocar un slider en cada columna
    with col1:
        v3 = st.slider("Indique el Importe Fijado", importe_Fijado - (int(importe_Fijado / 10)*9) , importe_Fijado * 2, step=int(importe_Fijado / 20) , value=importe_Fijado)
        v5 = st.slider(f"Indique la Diferencia Menor:      ", 1, 50, step=1, value=diferencia_Menor)

    with col2:
        v4 = st.slider("Indique el Número de Simulaciones", 100, 5000, step=10, value=num_Simulaciones)
        v6 = st.slider(f"Indique la Diferencia Stop:       ", 0.0, 10.0, step=0.1, value=diferencia_Stop, format="%f")
 
    # Mostramos valores en el sidebar
    st.sidebar.write(f"Importe Fijado:                    {v3:,}")
    st.sidebar.write(f"Número de Simulaciones:            {v4:,}")
    st.sidebar.write(f"Diferencia Menor:                  {v5}")
    st.sidebar.write(f"Diferencia Stop:                   {v6:.1f}")
    
    importe_Fijado = v3
    num_Simulaciones = v4
    diferencia_Menor = v5
    diferencia_Stop = v6

    return importe_Fijado, num_Simulaciones, diferencia_Menor, diferencia_Stop
from app4.ALEATORIO_librerias import *
import app4.ALEATORIO_variables as sTv
import streamlit as st


def sTv_paso0(importe_Fijado, num_Simulaciones, diferencia_Menor, diferencia_Stop):
    st.write('2 - Introducir los Valores que usará el modelo ')

    # Solicitar datos de entrada
    #os.system("cls") 
    v3 = st.text_input("Indique el Importe Fijado:          " , value = importe_Fijado)
    v4 = st.text_input(f"Indique el Número de Simulaciones: " , value = num_Simulaciones)
    v5 = st.text_input(f"Indique la Diferencia Menor:       " , value = diferencia_Menor)
    v6 = st.text_input(f"Indique la Diferencia Stop:        " , value = diferencia_Stop)

    st.write("\n***\n")
    # Evaluamos el Importe Fijado.
    try:
        v3_int = int(v3)
    except ValueError:
        st.sidebar.write(f"Importe Fijado:                    ({importe_Fijado})")
    else:
        st.sidebar.write(f"Importe Fijado:                    ({v3}) - * ")
        importe_Fijado = int(v3)

    # Evaluamos Número de Simulaciones
    try:
        v4_int = int(v4)
    except ValueError:
        st.sidebar.write(f"Número Simulaciones:               ({num_Simulaciones})")
    else:
        st.sidebar.write(f"Número de Simulaciones:            ({v4}) - nuevo valor")
        num_Simulaciones = int(v4)

    # Evaluamos la Diferencia menor
    try:
        v5_int = int(v5)
    except ValueError:
        st.sidebar.write(f"Diferencia Menor:                  ({diferencia_Menor})")
    else:
        st.sidebar.write(f"Diferencia Menor:                  ({v5}) - nuevo valor")
        diferencia_Menor = int(v5)

    # Evaluamos el Diferencia Stop
    try:
        v6_int = int(v6)  # Intenta convertir a entero
        st.sidebar.write(f"Diferencia Stop:                   ({v6_int}) - nuevo valor")
        diferencia_Stop = int(v6)
    except ValueError:
        try:
            v6_float = float(v6)  # Si no es entero, intenta convertir a flotante
            st.sidebar.write(f"Diferencia Stop:                   ({v6_float}) - nuevo valor")
            diferencia_Stop = float(v6)
        except ValueError:
            st.sidebar.write(f"Diferencia Stop:                   ({diferencia_Stop})")

    return importe_Fijado, num_Simulaciones, diferencia_Menor, diferencia_Stop
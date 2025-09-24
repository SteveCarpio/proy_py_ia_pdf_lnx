#import streamlit as st
from app4.ALEATORIO_librerias import *
from app4.ALEATORIO_paso0 import sTv_paso0
from app4.ALEATORIO_paso1 import sTv_paso1
from app4.ALEATORIO_paso2 import sTv_paso2
from app4.ALEATORIO_paso3 import sTv_paso3
from app4.ALEATORIO_paso4 import sTv_paso4

def main():
    
    st.title("📊 Simulador de Números Aleatorios ")  # 🗂️ 📄  🤖
    st.caption("Se ejecutarán varios modelos de simulación de números aleatorios usando matrices multidimensionales (Numpy y Pandas) y técnicas de Data Science.")
    
    st.sidebar.title("🤖 : Cuadrator")

    # PASO 0: Solicitar Datos y Valores de entrada ##############################################################################
    importe_Fijado, num_Simulaciones, diferencia_Menor, diferencia_Stop, df, file_name1, file_name2 = sTv_paso0()



    # PASO 3: Procesar Modelo Numpy #############################################################################################
    if st.sidebar.button("Procesar Modelo"):
        if df is not None:
            access_inicio = dt.now().strftime("%H:%M:%S")
            cont = sTv_paso3(df, num_Simulaciones, importe_Fijado, diferencia_Menor, diferencia_Stop, file_name1, file_name2)
            # Obtener IP del cliente si está disponible
            client_ip = st.context.ip_address  # solo disponible en v1.45.0+
            if client_ip:
                access_time = dt.now().strftime(f"%Y-%m-%d > {access_inicio} > %H:%M:%S")
                #st.write(f"Acceso desde IP local: {client_ip} a las {access_time}")
                with open("/home/robot/Python/x_log/streamlit_ip.log", "a") as f:
                    f.write(f"{access_time} > {client_ip} > APPS_DS > Cuadrator > {file_name1} > {importe_Fijado}|{num_Simulaciones}|{diferencia_Menor}|{diferencia_Stop}|{cont} \n")
        else:
            st.warning("No existe un DataFrame de entrada")



    # PASO 4: Descagar Ficheros Excel ###########################################################################################

    # Ruta en tu servidor Linux donde están los archivos Excel
    DIRECTORIO_EXCEL = "/tmp/salida_aleatorios/"

    # Verificar si existe la ruta
    if not os.path.exists(DIRECTORIO_EXCEL):
        #st.error(f"La ruta {DIRECTORIO_EXCEL} no existe.")
        os.makedirs(DIRECTORIO_EXCEL)
    else:
        # Obtener lista de archivos .xlsx o .xls ordenados inversamente
        archivos_excel = [f for f in sorted(os.listdir(DIRECTORIO_EXCEL), reverse=True)
                        if f.endswith(('.xlsx', '.xls'))]

        if archivos_excel:
            st.subheader("Archivos disponibles:")

            for archivo in archivos_excel:
                ruta_archivo = os.path.join(DIRECTORIO_EXCEL, archivo)

                # Mostrar en una fila horizontal: botón de descarga y de eliminación
                col1, col2 = st.columns([5, 1])

                with col1:
                    with open(ruta_archivo, "rb") as f:
                        contenido = f.read()
                        st.download_button(
                            label=f"📥 Descargar: {archivo}",
                            data=contenido,
                            file_name=archivo,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key=f"descargar_{archivo}"
                        )

                with col2:
                    if st.button("🗑️", key=f"eliminar_{archivo}"):
                        try:
                            os.remove(ruta_archivo)
                            #st.success(f"Archivo eliminado: {archivo}")
                            st.rerun()  # Recargar para actualizar la lista
                        except Exception as e:
                            st.error(f"Error al eliminar {archivo}: {e}")
        #else:
            #st.info("No hay archivos Excel en el directorio.")

    #st.markdown("---")


    with st.expander("📖 Ayuda", expanded=False):
        st.markdown("""
        **Proceso de Selección de Números Aleatorios (Cuadrator).**  

        Valores de entrada:  
        - Importe a Buscar: Es el importe máximo que se debe alcanzar.
        - Número de Simulaciones: Es el número de intentos que se realizarán para llegar el importe esperado.
        - Diferencia Máxima: Es la diferencia en la que comenzará a crear los archivos Excel de salida.
        - Diferencia Mínima: Es la diferencia más pequeña que se asume como esperada; en caso de llegar a este valor, el proceso se detendrá.

        **Nota Técnica:**  

        Este programa está desarrollado en Python, utilizando dos librerías muy potentes: NumPy y Pandas, ampliamente usadas en investigación y ciencia de datos. 

        Ambas librerías permiten ejecutar modelos matemáticos para encontrar soluciones mediante la selección de números aleatorios, siendo NumPy especialmente eficiente por su uso de matrices.


        - NumPy: Librería de Python para trabajar con arrays y realizar cálculos numéricos de forma rápida.
        - Pandas: Librería para manipular y analizar datos estructurados, como si fueran hojas de cálculo.
        
        Más info: 
        - Python: https://es.wikipedia.org/wiki/Python
        - NumPy: https://es.wikipedia.org/wiki/NumPy
        - Pandas: https://es.wikipedia.org/wiki/Pandas_(software) 
        
        

        > *Si necesita más ayuda consultar con SteveCarpio - Python-v1.2025*  
        """)


"""
    # PASO 1: Importamos el txt con los prestamos a un DataFrame
    df1 = sTv_paso1(nombre_Entrada, nombre_Salida, v1)

    # PASO 2: Elimino ID prestamos que tenemos en un excel
    df2 = sTv_paso2(df1)
"""
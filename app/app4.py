#import streamlit as st
from app4.ALEATORIO_librerias import *
from app4.ALEATORIO_paso0 import sTv_paso0
from app4.ALEATORIO_paso1 import sTv_paso1
from app4.ALEATORIO_paso2 import sTv_paso2
from app4.ALEATORIO_paso3 import sTv_paso3
from app4.ALEATORIO_paso4 import sTv_paso4

def main():
    access_ini = dt.now().strftime("%Y%m%d - %H:%M:%S")
    st.title("📊 Simulador de Números Aleatorios ")  # 🗂️ 📄  🤖
    st.caption("Se ejecutarán varios modelos de simulación de números aleatorios usando matrices multidimensionales (Numpy y Pandas) y técnicas de Data Science.")
    st.sidebar.markdown("---")  # Separador

    # PASO 0: Solicitar Datos y Valores de entrada ##############################################################################
    importe_Fijado, num_Simulaciones, diferencia_Menor, diferencia_Stop, df, file_name1, file_name2 = sTv_paso0()



    # PASO 3: Procesar Modelo Numpy #############################################################################################
    if st.sidebar.button("Procesar Modelo"):
        if df is not None:
            sTv_paso3(df, num_Simulaciones, importe_Fijado, diferencia_Menor, diferencia_Stop, file_name1, file_name2)

        else:
            st.warning("No existe un DataFrame de entrada")



    # PASO 4: Descagar Ficheros Excel ###########################################################################################

    # Ruta en tu servidor Linux donde están los archivos Excel
    DIRECTORIO_EXCEL = "/tmp/salida_aleatorios/"

    # Verificar si existe la ruta
    if not os.path.exists(DIRECTORIO_EXCEL):
        st.error(f"La ruta {DIRECTORIO_EXCEL} no existe.")
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

        **Tips**  
        - …  
        - …

        > *By sTv*  
        """)

    access_fin = dt.now().strftime("%H:%M:%S")
    st.caption(f"{access_ini} -- {access_fin} ")



"""

def option_0():
    # PASO 1: Importamos el txt con los prestamos a un DataFrame
    df1 = sTv_paso1(nombre_Entrada, nombre_Salida, v1)

    # PASO 2: Elimino ID prestamos que tenemos en un excel
    df2 = sTv_paso2(df1)



def option_Help():
    print(Fore.MAGENTA + "------------- [ Proceso de Selección de Números Aleatorios ] -------------  \n")
    print(Fore.YELLOW + "Valores de Ejecución: \n")
    print(Fore.CYAN + "- Importe Fijado: " + Fore.WHITE + "Es el importe máximo que podrá agrupar el modelo.")
    print(Fore.CYAN + "- Num Simulaciones: "  + Fore.WHITE + "Es la cantidad de veces que el modelo generará simulaciones para alcanzar el importe fijado.")
    print(Fore.CYAN + "- Diferencia Menor: "  + Fore.WHITE + "Es el valor mínimo esperado que puede devolver el modelo.")
    print(Fore.CYAN + "- Diferencia Stop: "  + Fore.WHITE + "Es el valor más bajo permitido que utilizará el modelo como límite.\n")
    print(Fore.YELLOW + "Nota Técnica: \n")
    print("Este programa está desarrollado en Python, utilizando dos librerías muy potentes: NumPy y Pandas, ampliamente usadas en investigación y ciencia de datos.")
    print("Ambas librerías permiten ejecutar modelos matemáticos para encontrar soluciones mediante la selección de números aleatorios, siendo NumPy especialmente eficiente por su uso de matrices.\n")
    print(Fore.CYAN + "- NumPy: " + Fore.WHITE + "Librería de Python para trabajar con arrays y realizar cálculos numéricos de forma rápida.")
    print(Fore.CYAN + "- Pandas: " + Fore.WHITE + "Librería para manipular y analizar datos estructurados, como si fueran hojas de cálculo.\n")
    print(Fore.YELLOW + "Más info: \n")
    print(Fore.CYAN + "- Python: " + Fore.WHITE + "https://es.wikipedia.org/wiki/Python")
    print(Fore.CYAN + "- NumPy: " + Fore.WHITE + "https://es.wikipedia.org/wiki/NumPy")
    print(Fore.CYAN + "- Pandas: " + Fore.WHITE + "https://es.wikipedia.org/wiki/Pandas_(software) \n")
    print(Fore.YELLOW + " \n")
    print("Si necesita más ayuda consultar con " + Fore.RED + "SteveCarpio" + Fore.WHITE + " - " + Fore.GREEN + "Python-v1.2025")

# Función para limpiar la pantalla (en sistemas basados en UNIX)
def limpiar_pantalla():
    os.system("cls")  

# Menú interactivo
def mostrar_menu():
    limpiar_pantalla()
    print(Fore.MAGENTA + "=" * 37)
    print(Fore.WHITE + "        🖥️   MENÚ PRINCIPAL 🖥️")
    print(Fore.MAGENTA + "=" * 37)
    print(Fore.CYAN + "- File de Entrada:  " + str(nombre_Entrada) + "." + str(v11))
    print(Fore.CYAN + "- Importe Fijado:   " + str(importe_Fijado))
    print(Fore.CYAN + "- Núm Simulaciones: " + str(num_Simulaciones))
    print(Fore.CYAN + "- Diferencia Menor: " + str(diferencia_Menor))
    print(Fore.CYAN + "- Diferencia Stop:  " + str(diferencia_Stop))
    print(Fore.MAGENTA + "=" * 37)
    print(Fore.WHITE   + "0) ⚪ Ejecutar Modelo Numpy y Pandas")
    print(Fore.YELLOW  + "1) 🟡 Ejecutar Modelo Numpy ")
    print(Fore.YELLOW  + "2) 🟡 Ejecutar Modelo Pandas")
    print(Fore.CYAN  + "3) 🟡 Modificar Valores     ")
    print(Fore.MAGENTA + "?) 🟣 Ayuda                 ")
    print(Fore.RED     + "x) ❌ Salir del programa   " + Fore.WHITE + "    (.v3)")
    print(Fore.MAGENTA + "=" * 37)

# Función principal para gestionar el menú
def ejecutar_menu():
    while True:
        mostrar_menu()
        option = input(Fore.WHITE + "Selecciona una opción: ")
        limpiar_pantalla()
        if option   == '0':
            option_0()
        elif option == '1':
            option_1()
        elif option == '2':
            option_2()
        elif option == '3':
            option_3()            
        elif option == '?':
            option_Help()
        elif option.upper() == 'X':
            print(Fore.RED + "\n¡Saliendo del programa! \n")
            break
        else:
            print(Fore.RED + "\n ❌ Opción no válida, por favor elige una opción válida ❌\n")
        
        # Pausa para que el usuario vea los resultados
        input(Fore.MAGENTA + f'\n------------- [ Pulse una tecla para volver al menú - {dt.now()} ] -------------')

ejecutar_menu()

"""
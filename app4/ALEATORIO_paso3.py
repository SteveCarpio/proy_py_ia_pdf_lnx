#----------------------------------
# Modelo usando matrices con NUMPY
#----------------------------------

from  app4.ALEATORIO_librerias import *
import app4.ALEATORIO_variables as sTv

# --- Función que ejecuta un algoritmo y crea un Array.Numpy con los reg Aleatorios
def PROC_Crea_Seleccion_Aleatoria3(ar, importe_Fijado):

    # Baraja el array de NumPy
    np.random.shuffle(ar)
    # Crea un Array.Numpy vació con la longitud de 'ar'
    seleccionados = np.empty((len(ar), ar.shape[1]))
    suma = 0
    count = 0
    # Selección aleatoria de registros
    for row in ar:
        valor = row[1]  # Se asume que la segunda columna corresponde a 'TOTAL'
        if valor != 0:
            if suma + valor <= importe_Fijado:
                seleccionados[count] = row
                suma += valor
                count += 1
            if suma >= importe_Fijado:
                break
    # Re dimensiona el array solo con los filas incluidas
    seleccionados = seleccionados[:count]
    # Devolvemos el Array.Numpy y la Suma acumulada
    del ar
    # Retornamos el resultado
    return seleccionados, suma 

def sTv_paso3(df3, num_Simulaciones, importe_Fijado, diferencia_Menor, diferencia_Stop, file_name1, file_name2):

    sw=0
    access_inicio = dt.now().strftime("%Y%m%d_%H%M%S")

    # Total del fichero de entrada
    var_total = df3['TOTAL'].sum()

    # Convertir el DataFrame en un Array Numpy
    ar_tmp = df3.to_numpy()
    
    # Crear una barra de progreso vacía
    progress_bar = st.progress(0)

    # Crear un marcador de texto para mostrar el progreso numérico
    status_text = st.empty()

    # Bucle que nos servirá para Lanzar las N Simulaciones 
    for i in range(1 , num_Simulaciones + 1):

        # Crear una barra de estado y información de N simulaciones leídas)
        progress = i / num_Simulaciones
        progress_bar.progress(progress)
        status_text.text(f"Simulación {i} de {num_Simulaciones}")

        # Llama func, creará un Array.Numpy con datos aleatorios con el importe fijado
        ar_Resultado, suma=PROC_Crea_Seleccion_Aleatoria3(ar_tmp, importe_Fijado)

        # Evaluo... 
        if importe_Fijado - suma < diferencia_Menor:
            time.sleep(0.5)   #   CREO que como va con el reloj si hago un sleep lo mismo tengo mas posibilidades.
            sw=1
            # Convierto el Array.Numpy "ar_Resultado" en un DataFrame
            df_Resultado = pd.DataFrame(ar_Resultado, columns=['ID', 'TOTAL'])

            # Exporto el DataFrame a un excel
            df_Resultado.to_excel(f'/tmp/salida_aleatorios/{access_inicio}__Simulación_{i}__Diferencia_{importe_Fijado-suma}.xlsx',index=False)

            # Mostrar resultados
            st.caption(f"Simulación Número: {i} -- Número de Registros: {len(df_Resultado)} -- Importe Total Conseguido: {suma:,.2f} -- Diferencia Encontrada: {importe_Fijado - suma}" )
                       
        # Detener el bucle si la DIF es igual a CERO
        if importe_Fijado - suma < diferencia_Stop:
            #st.markdown("---")
            st.info(f"¡ Enhorabuena se encontró el valor más bajo en la Simulación {i} !")
            break

    if sw == 0:
        st.warning("¡ No hubo resultados con los valores introducidos !")
    else:
        st.success("¡ Proceso Finalizado !")
 
    # Liberar memoria de los objetos
    del ar_tmp, ar_Resultado, df3

    
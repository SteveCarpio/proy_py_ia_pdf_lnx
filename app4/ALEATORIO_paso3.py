#----------------------------------
# Modelo usando matrices con NUMPY
#----------------------------------

from  app4.ALEATORIO_librerias import *
import app4.ALEATORIO_variables as sTv

#-------------------------------------------------------------------------------------------------------------
# Suponemos que tienes el DataFrame original como df
# df = pd.read_csv('tu_archivo.csv') # o como corresponda

# 1- Enfoque aleatorio simple: Selecciona IDs aleatoriamente hasta alcanzar el límite.
def seleccion_aleatoria(df, objetivo):
    df = df.sample(frac=1).reset_index(drop=True)  # Mezcla aleatoriamente
    suma = 0
    ids = []
    for _, row in df.iterrows():
        if suma + row['TOTAL'] <= objetivo:
            suma += row['TOTAL']
            ids.append(row['ID'])
        if suma >= objetivo:
            break
    return df[df['ID'].isin(ids)]

# Ejemplo de uso:
# df_resultado = seleccion_aleatoria(df, 60000)



# 2- Algoritmo de mochila (knapsack): Usa programación dinámica para buscar una combinación óptima.
#    El método knapsack es más exhaustivo, pero puede requerir bastante RAM para un objetivo grande.
def seleccion_knapsack(df, objetivo):
    # Convertimos los totales a enteros si es necesario
    valores = df['TOTAL'].astype(int).values
    ids = df['ID'].values
    n = len(valores)
    dp = np.zeros(objetivo + 1, dtype=int)
    seleccion = [[] for _ in range(objetivo + 1)]

    for i in range(n):
        for j in range(objetivo, valores[i]-1, -1):
            if dp[j-valores[i]] + valores[i] > dp[j]:
                dp[j] = dp[j-valores[i]] + valores[i]
                seleccion[j] = seleccion[j-valores[i]] + [ids[i]]
    mejor_suma = dp.max()
    mejor_j = dp.argmax()
    return df[df['ID'].isin(seleccion[mejor_j])]

# Ejemplo de uso:
# df_resultado = seleccion_knapsack(df, 60000)

# 3- Enfoque de Monte Carlo: Prueba muchas combinaciones aleatorias y se queda con la mejor.
#    El Monte Carlo puede hallar buenas soluciones si aumentas el número de iteraciones.
import pandas as pd
import numpy as np

def seleccion_montecarlo(df, objetivo, iteraciones=10000):
    mejor_ids = []
    mejor_suma = 0
    for _ in range(iteraciones):
        muestra = df.sample(frac=np.random.uniform(0.01, 0.1))  # Fracción aleatoria
        suma = muestra['TOTAL'].sum()
        if suma <= objetivo and suma > mejor_suma:
            mejor_suma = suma
            mejor_ids = muestra['ID'].tolist()
    return df[df['ID'].isin(mejor_ids)]

# Ejemplo de uso:
# df_resultado = seleccion_montecarlo(df, 60000)
#-------------------------------------------------------------------------------------------------------------


# --- Función que ejecuta un algoritmo y crea un Array.Numpy con los reg Aleatorios
def PROC_Crea_Seleccion_Aleatoria3(ar, importe_Fijado):

    # Selecciona índices aleatorios sin reemplazo
    #indices = np.random.choice(len(ar), len(ar), replace=False)
    #ar_random = ar[indices]

    # Cambiar la semilla que usa Numpy
    np.random.seed(int(time.time() * 1000) % 2**32)

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

    #df_resultado = seleccion_knapsack(df3, 600000000)  # Esto me peto el servidor.
    df_resultado = seleccion_montecarlo(df, 600000000)

    st.write(df_resultado)


    sw=0
    access_inicio = dt.now().strftime("%Y%m%d_%H%M%S")
    start_time = time.time()

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
        if importe_Fijado - int(suma) < diferencia_Menor:
            time.sleep(0.5)   #   CREO que como va con el reloj si hago un sleep lo mismo tengo mas posibilidades.
            sw=1
            # Convierto el Array.Numpy "ar_Resultado" en un DataFrame
            df_Resultado = pd.DataFrame(ar_Resultado, columns=['ID', 'TOTAL'])

            # Exporto el DataFrame a un excel
            df_Resultado.to_excel(f'/tmp/salida_aleatorios/{access_inicio}__Simulación_{i}__Diferencia_{importe_Fijado-suma}.xlsx',index=False)

            # Mostrar resultados
            st.caption(f"Simulación Número: {i} -- Número de Registros: {len(df_Resultado)} -- Importe Total Conseguido: {suma:,.2f} -- Diferencia Encontrada: {importe_Fijado - suma}" )
                       
        # Detener el bucle si la DIF es igual a CERO
        if importe_Fijado - int(suma) < diferencia_Stop:
            #st.markdown("---")
            st.info(f"¡ Enhorabuena se encontró el valor más bajo en la Simulación {i} !")
            break

    end_time = time.time()
    tiempo_total = end_time - start_time
    minutos = int(tiempo_total // 60)
    segundos = int(tiempo_total % 60)
    if sw == 0:
        st.warning(f"¡ No hubo resultados con los valores introducidos ! - Tiempo de ejecución {minutos}:{segundos}")
    else:
        st.success(f"¡ Proceso Finalizado ! - Tiempo de ejecución {minutos}:{segundos}")
 
    # Liberar memoria de los objetos
    del ar_tmp, ar_Resultado, df3

    
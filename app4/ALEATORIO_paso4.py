#----------------------------------
# Modelo usando matrices con PANDAS
#----------------------------------

from app4.ALEATORIO_librerias import *
import app4.ALEATORIO_variables as sTv

# --- Función para comprobar la memoria en uso
def PROC_Ver_Tamano_Objetos(nombre,objeto,opcion):
    # Tamaño en memoria del DataFrame en bytes
    if opcion == 1:
        tamaño_df_bytes = objeto.memory_usage(deep=True).sum()
        tamaño_df_mb = tamaño_df_bytes / (1024 * 1024)  # Convertir a MB
        #print(f'Tamaño en memoria del DataFrame ({nombre}): {tamaño_df_mb:.2f} MB')
    # Tamaño en memoria del array en bytes
    if opcion == 2:
        tamaño_array_bytes = objeto.nbytes
        tamaño_array_mb = tamaño_array_bytes / (1024 * 1024)  # Convertir a MB
        #print(f'Tamaño en memoria del array ({nombre}): {tamaño_array_mb:.2f} MB')

# --- Función que ejecuta un algoritmo y crea un DataFrame con los registros Aleatorios
def PROC_Crea_Seleccion_Aleatoria4(df, importe_Fijado):
    # Baraja el DataFrame
    df = df.sample(frac=1)
    # Defino Listas y variables
    seleccionados = []
    suma = 0
    # Selección aleatoria de registros
    for index, row in df.iterrows():
        valor = row['TOTAL']  # stv: round() int()  el resultado luego es ficticio
        if valor != 0:
            if suma + valor <= importe_Fijado:
                seleccionados.append(row)
                suma += valor
            if suma >= importe_Fijado:
                break
    # Crea el nuevo DataFrame con los valores aleatorios
    resultados_df = pd.DataFrame(seleccionados)
    return resultados_df.reset_index(drop=True), suma

def sTv_paso4(df4, num_Simulaciones, importe_Fijado, diferencia_Menor, diferencia_Stop, nombre_Salida ):

    print(Fore.YELLOW + f'\n------------- [ Paso 4: Modelo Pandas - {dt.now()} ]------------- \n')
    print(f"Procesando ({num_Simulaciones}) simulaciones aleatorias")

    # Total del fichero de entrada
    var_total = df4['TOTAL'].sum()
    
    sw=0
    simuinfo = num_Simulaciones // 5
    trocear=0
    # --- Bucle que nos servirá para Lanzar las N Simulaciones
    for i in range(1,num_Simulaciones + 1):

        # Mostrar avisos cada X, esta dividido x 5 las num_Simulaciones
        trocear=trocear+1
        if trocear == simuinfo:
            print(f"Procesando ({i}/{num_Simulaciones}) - {dt.now().strftime("%H:%M")} ")
            trocear=0

        # Crea DF con datos aleatorios
        df_Resultado, suma=PROC_Crea_Seleccion_Aleatoria4(df4, importe_Fijado)

        # Evaluamos los importes 
        if importe_Fijado - suma < diferencia_Menor:
            sw=1
            # Exporto el DataFrame a un excel
            df_Resultado.to_excel(f'{sTv.var_RutaInforme}{nombre_Salida}_Sim{i}_Dif_{importe_Fijado-suma}_pandas.xlsx',index=False)

            # Mostrar resultados
            print(Fore.YELLOW + f"\n--------------------- Simulación Número: {i}")
            print(f'Num Reg TEntrada   : {len(df4)}')
            print(f'Num Reg TSalida    : {len(df_Resultado)}')
            print(f'Importe Total      : {var_total}')
            print(f'Importe Fijado     : {importe_Fijado} ')
            print(f'Importe Conseguido : {suma}')
            print(Fore.GREEN + f'        Diferencia : {importe_Fijado - suma}\n')
            

        # Detener el bucle si la DIF es igual a CERO
        if importe_Fijado - suma < diferencia_Stop:
            print(Fore.GREEN + f"----------------------------------------------------------------------------------")
            print(Fore.GREEN + f"-------- ¡¡¡ Enhorabuena se encontró el valor más bajo en el Nº: {i} !!! ---------")
            print(Fore.GREEN + f"----------------------------------------------------------------------------------\n")
            break

    if sw == 0:
        print(f"\n")
        print(Fore.RED + f"      ¡ No hubo resultados con los valores introducidos !\n")

    # Invocar función para visualizar en tamaño del Objeto
    #PROC_Ver_Tamano_Objetos('df_tmp',df3,1)
    #PROC_Ver_Tamano_Objetos('ar_tmp',ar_tmp,2)
    #PROC_Ver_Tamano_Objetos('ar_Resultado',ar_Resultado,2)

    # Liberar memoria de los objetos
    #del ar_tmp, ar_Resultado, df3
    

from app4.ALEATORIO_librerias import *
import app4.ALEATORIO_variables as sTv

# --- Función que nos sirve para importar el fichero de entrada .txt
def Leer_desde_excel(nombre_Entrada, nombre_Salida):
    
    df = pd.read_excel(f'{sTv.var_RutaFileIn}{nombre_Entrada}.xlsx')

    # Exporto el DataFrame a un excel para tenerlo
    df.to_excel(f'{sTv.var_RutaInforme}{nombre_Salida}.xlsx', index=False)

    # Mostrar el DataFrame
    print(f"Nombre del Fichero  : {nombre_Entrada}.txt")
    print(f"Número de Registros : {len(df)}")
    
    return df

# --- Función que nos sirve para importar el fichero de entrada .txt
def Leer_desde_txt(nombre_Entrada, nombre_Salida):
    # Inicializar listas vacías para cada campo
    campo1_list = []
    campo2_list = []
    campo3_list = []

    # Detectar la codificación del archivo
    with open(f"{sTv.var_RutaFileIn}{nombre_Entrada}.txt", 'rb') as file:  # Abrir el archivo en modo binario para detectar la codificación
        raw_data = file.read(1000)     # Leer solo los primeros 1000 bytes
        result = chardet.detect(raw_data)
        encoding = result['encoding']  # utf-8, ansi, ascii, etc....

    # Abrir el archivo y leer línea por línea
    with open(f"{sTv.var_RutaFileIn}{nombre_Entrada}.txt", "r", encoding=encoding, errors='replace') as file:  # utf-8

        for line in file:
            # Campo1 "NUMPRES" en la posición 8, ancho 15
            campo1 = line[7:22].strip()  # Índices 7:22 para los 15 caracteres
            campo1_list.append(campo1)
            
            # Campo2 "IMPINICIAL" en la posición 31, ancho 15 (formato doble con signo, 13 enteros, 2 decimales)
            campo2 = float(line[30:45].strip())  # Convertimos a tipo flotante
            campo2_list.append(campo2)
            
            # Campo3 "PD" en la posición 645, ancho 5 (formato doble, 3 enteros, 2 decimales)
            #campo3 = float(line[644:649].strip())  # Convertimos a tipo flotante
            #campo3_list.append(campo3)

    # Crear el DataFrame con los campos extraídos
    df = pd.DataFrame({
        'ID': campo1_list,
        'TOTAL': campo2_list #,
        #'PD': campo3_list
    })

    # Exporto el DataFrame a un excel para tenerlo
    df.to_excel(f'{sTv.var_RutaInforme}{nombre_Salida}.xlsx', index=False)

    # Mostrar el DataFrame
    print(f"Nombre del Fichero  : {nombre_Entrada}.txt")
    print(f"Número de Registros : {len(df)}")
    print(f"Encoding de Entrada : {encoding}")
    
    return df

def sTv_paso1(nombre_Entrada, nombre_Salida, v1):
    print(Fore.CYAN + f'\n------------- [ Paso 1: Importación del Fichero de Entrada ]------------- \n')
    if v1 == "1":
        df = Leer_desde_txt(nombre_Entrada, nombre_Salida)
    if v1 == "2":
        df = Leer_desde_excel(nombre_Entrada, nombre_Salida)
    return df
import pandas as pd
import datetime
import re
import sys
from pandas.tseries.offsets import MonthEnd, MonthBegin, BMonthBegin, DateOffset

# Mostrar todas las filas y columnas
pd.set_option('display.max_rows', None) 

# Nombre del Fichero Excel
file_excel1="TDACAM9_INFFLUJOS_ES_202509.xls"      #   OK
file_excel2="TDAPENEDES1_INFFLUJOS_ES_202509.xls"  #   NO es igual
file_excel3="TDACAM6_INFFLUJOS_ES_202509.xls"      #   OK, Borre una columna que estaba fuera de la columna O  
file_excel4="TDACAM11_INFFLUJOS_ES_201709_v3.xls"  #   OK, Borre columnas
file_excel5="TDACAM4_INFFLUJOS_ES_202509_v2.xls"   #   
file_excel6="SABADELL5_INFFLUJOS_ES_202509.xls"    #   

# Ruta del Fichero Excel
file_excel = file_excel1
ruta_excel = f"/home/robot/Python/proy_py_ia_pdf_lnx/excel/{file_excel}"

# Creo diccionario según el tipo de file de entrada
if "TDACAM9_INFFLUJOS_ES" in file_excel:
    dic_nomBono = [
        {'BONO': 'Bono-A1','NUM_BONOS': 100},
        {'BONO': 'Bono-A2','NUM_BONOS': 100},
        {'BONO': 'Bono-A3','NUM_BONOS': 100},
        {'BONO': 'Bono-B','NUM_BONOS': 100},
        {'BONO': 'Bono-C','NUM_BONOS': 100},
        {'BONO': 'Bono-D','NUM_BONOS': 100}
    ]
    df_numBono = pd.DataFrame(dic_nomBono)

if "TDACAM6_INFFLUJOS_ES" in file_excel:
    dic_nomBono = [
        {'BONO': 'Bono-A3','NUM_BONOS': 100},
        {'BONO': 'Bono-B','NUM_BONOS': 100}
    ]
    df_numBono = pd.DataFrame(dic_nomBono)

if "TDACAM11_INFFLUJOS_ES" in file_excel:
    dic_nomBono = [
        {'BONO': 'Bono-A1','NUM_BONOS': 100},
        {'BONO': 'Bono-A2','NUM_BONOS': 100},
        {'BONO': 'Bono-A3','NUM_BONOS': 100},
        {'BONO': 'Bono-A4','NUM_BONOS': 100},
        {'BONO': 'Bono-B','NUM_BONOS': 100},
        {'BONO': 'Bono-C','NUM_BONOS': 100},
        {'BONO': 'Bono-D','NUM_BONOS': 100}
    ]
    df_numBono = pd.DataFrame(dic_nomBono)


if "TDACAM4_INFFLUJOS_ES" in file_excel:
    dic_nomBono = [
        {'BONO': 'Bono-B','NUM_BONOS': 100}
    ]
    df_numBono = pd.DataFrame(dic_nomBono)


############################################################################################################

# Lee el archivo sin encabezados
df_excel = pd.read_excel(ruta_excel, header=None, dtype=str)
#df_excel = pd.read_excel(ruta_excel, header=None, dtype=str, usecols="A:O")  # Lee solo columnas A a O
#df_excel  = pd.read_excel(ruta_excel, header=None, dtype=str, usecols=range(15))

# Reemplaza NaN por cadena vacía en todo el DataFrame
df_excel = df_excel.fillna('')

# Crea una lista y variables de apoyo
filas_bono1 = []
filas_bono2 = []
filas_bono3 = []

bonoX1, bonoX2, isinX1, isinX2, taaX1, taaX2, taaX3, taaX4, taaX5, taaX6 = "", "", "", "", "", "", "", "", "",""
bonoX = ""
contBlancos = 0
# Recorro cada fila
for idx, fila in df_excel.iterrows():
    #print(f"{idx}:{fila} ")
    # Agrego cada valor de cada celda en una variable
    var_a, var_b, var_c, var_d, var_e, var_f, var_g, var_h, var_i, var_j, var_k, var_l, var_m = str(fila[0]), str(fila[1]), str(fila[2]), str(fila[3]), str(fila[4]), str(fila[5]), str(fila[6]), str(fila[7]), str(fila[8]), str(fila[9]), str(fila[10]), str(fila[11]), str(fila[12])

    ############## Creo la LISTA de [ BONOS ] 
    if "Bono" in var_e:
        isinX1 = df_excel.iloc[idx + 3, 3]
        isinX2 = df_excel.iloc[idx + 3, 10]
        taaX1 = float(df_excel.iloc[idx + 7, 3]) * 100
        taaX2 = float(df_excel.iloc[idx + 7, 5]) * 100
        taaX3 = float(df_excel.iloc[idx + 7, 7]) * 100

        #taaX4 = float(df_excel.iloc[idx + 7, 10]) * 100
        #taaX5 = float(df_excel.iloc[idx + 7, 12]) * 100
        #taaX6 = float(df_excel.iloc[idx + 7, 14]) * 100
        valor4 = df_excel.iloc[idx + 7, 10]
        taaX4 = float(valor4) * 100 if str(valor4).strip() != "" else 0.0
        valor5 = df_excel.iloc[idx + 7, 12]
        taaX5 = float(valor5) * 100 if str(valor5).strip() != "" else 0.0
        valor6 = df_excel.iloc[idx + 7, 14]
        taaX6 = float(valor6) * 100 if str(valor6).strip() != "" else 0.0

        filas_bono1.append([var_e.strip(), isinX1.strip(), taaX1, taaX2, taaX3])
        if var_l != "":
                filas_bono1.append([var_l.strip(), isinX2.strip(), taaX4, taaX5, taaX6])
    
    ############## Creo la LISTA [ TABLA_BONO ]
    # Leo la variable Bono
    if "Bono" in var_i:
        bonoX = var_i.strip()

    if bonoX != "":
        if var_c.strip() != "" and var_c.strip() != "Fecha" and var_c.strip() != "Total" and var_c.strip() != "00:00:00" and var_d != "(*)" and re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", var_c):
            var_c2 = datetime.datetime.strptime(var_c, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
            filas_bono2.append([bonoX, var_c2, round(float(var_d),2), round(float(var_f),2), round(float(var_h),2), round(float(var_j),2), round(float(var_k),2), round(float(var_m),2)])
            #print(f'{idx} : {bonoX} - {var_c} - {var_d} - {var_f} : {var_h} - {var_j} : {var_k} - {var_m} ')  

    if var_d == "(*)":
        filas_bono3.append([bonoX, var_f])
    
    # ------- Fin del Bucle -------
    if var_c == "":
        contBlancos = contBlancos + 1
        if contBlancos > 50:
            print("---- FIN ----")
            break
    else:
        contBlancos = 0



############### FASE 1 - Tratamiento de los datos de Bonos ############################################

### TRATAMIENTO DATAFRAME: BONO1
df_bono1 = pd.DataFrame(filas_bono1, columns=['BONO', 'ISIN', 'TAA_1', 'TAA_2', 'TAA_3'])
df_bono1_union = pd.merge(df_bono1, df_numBono, on='BONO')
df_bono1_union['N0'] = df_bono1_union.index.map(lambda x: x + 1)
print(df_bono1_union)

### TRATAMIENTO DATAFRAME: BONO2
df_bono2 = pd.DataFrame(filas_bono2, columns=['BONO', 'FECHA', 'AP_1', 'IB_1', 'AP_2', 'IB_2', 'AP_3', 'IB_3'])
print(df_bono2.head(10))

### TRATAMIENTO DATAFRAME: BONO3 --> INTERES BRUTO
df_bono3 = pd.DataFrame(filas_bono3, columns=['BONO', 'INT_BRUTO'])


### UNION BONO1 y BONO3: Agregar a la tabla bono1 el campo Ineres Bruto
df_bono3_union = pd.merge(df_bono3, df_bono1_union, on='BONO')

### UNION DATAFRAME BONO1 y BONO2
df_union1 = pd.merge(df_bono3_union, df_bono2, on='BONO')
df_union1 = df_union1.reindex(columns=['N0', 'BONO', 'FECHA', 'ISIN', 'NUM_BONOS', 'INT_BRUTO', 'TAA_1', 'AP_1', 'IB_1', 'TAA_2', 'AP_2', 'IB_2', 'TAA_3', 'AP_3', 'IB_3'])


############### FASE 2 - Crear Toales ############################################

### AGRUPAR BONOS Y SUMAR TOTALES
df_bono2_totales = df_bono2.groupby('BONO')[['AP_1', 'AP_2', 'AP_3']].sum().reset_index()

### RENOMBRAR COLUMNAS
df_bono2_totales.rename(columns={'AP_1': 'T_AP_1', 'AP_2': 'T_AP_2', 'AP_3': 'T_AP_3'}, inplace=True)

### AGREGAR RESULTADO 2 AL DF PRINCIPAL
df_principal1 = pd.merge(df_bono2_totales, df_union1, on='BONO')

### CREP COLUMNA N1
df_principal1['N1'] = df_principal1.index.map(lambda x: x + 1)

### ORDENAR CAMPOS
df_principal1 = df_principal1.reindex(columns=['N0', 'N1', 'BONO', 'FECHA', 'ISIN', 'NUM_BONOS', 'INT_BRUTO', 'TAA_1', 'AP_1', 'IB_1', 'T_AP_1', 'TAA_2', 'AP_2', 'IB_2', 'T_AP_2', 'TAA_3', 'AP_3', 'IB_3', 'T_AP_3'])


############### FASE 3 - Desagrupar grupos de Importes 1, 2 y 3 y agruparos en una sola tabla ############################################

# Columnas fijas que no cambian
cols_fijas = ['N0', 'N1', 'BONO', 'FECHA', 'ISIN', 'NUM_BONOS', 'INT_BRUTO']

# Detectamos automáticamente los grupos (_1, _2, _3, etc.)
grupos = sorted({col.split('_')[-1] for col in df_principal1.columns if '_' in col and col.split('_')[-1].isdigit()}, key=int)

# Lista donde iremos guardando las filas transformadas
filas1 = []
filas2 = []
filas3 = []
filasx = []
cont = 0
sw = 1

# Recorremos cada fila del DF original
for _, fila in df_principal1.iterrows():

    cont = cont + 1
    
    filas1.append({
        'N0': fila['N0'],
        'N1': fila['N1'],
        'N2': 1,
        'N3': cont,
        'BONO': fila['BONO'],
        'FECHA': fila['FECHA'],
        'ISIN': fila['ISIN'],
        'NUM_BONOS': fila['NUM_BONOS'],
        'INT_BRUTO': fila['INT_BRUTO'],
        'TAA': fila[f'TAA_1'],
        'AP': fila[f'AP_1'],
        'IB': fila[f'IB_1'],
        'T_AP': fila[f'T_AP_1']
    })

    filas2.append({
        'N0': fila['N0'],
        'N1': fila['N1'],
        'N2': 2,
        'N3': cont,
        'BONO': fila['BONO'],
        'FECHA': fila['FECHA'],
        'ISIN': fila['ISIN'],
        'NUM_BONOS': fila['NUM_BONOS'],
        'INT_BRUTO': fila['INT_BRUTO'],
        'TAA': fila[f'TAA_2'],
        'AP': fila[f'AP_2'],
        'IB': fila[f'IB_2'],
        'T_AP': fila[f'T_AP_2']
    })
    filas3.append({
        'N0': fila['N0'],
        'N1': fila['N1'],
        'N2': 3,
        'N3': cont,
        'BONO': fila['BONO'],
        'FECHA': fila['FECHA'],
        'ISIN': fila['ISIN'],
        'NUM_BONOS': fila['NUM_BONOS'],
        'INT_BRUTO': fila['INT_BRUTO'],
        'TAA': fila[f'TAA_3'],
        'AP': fila[f'AP_3'],
        'IB': fila[f'IB_3'],
        'T_AP': fila[f'T_AP_3']
    })

filasx = filas1 + filas2 + filas3
    
# Creamos el nuevo DataFrame
df_principal2 = pd.DataFrame(filasx)

# Ordenamos el dataframe por campo2 y luego por campo3
df_principal3 = df_principal2.copy() # es necesario hacerlo en un copia previa
df_principal3 = df_principal3.sort_values(by=['N0', 'N2', 'N3'])

### CREP COLUMNA N1, es necesario resetear el valor de registro
df_principal3 = df_principal3.reset_index(drop=True)
df_principal3['N4'] = df_principal3.index + 1

### ORDENO COLUMNAS DE SALIDA
df_principal3 = df_principal3.reindex(columns=['N0', 'N1', 'N2', 'N3', 'N4', 'BONO', 'FECHA', 'ISIN', 'NUM_BONOS', 'INT_BRUTO', 'TAA', 'AP', 'IB', 'T_AP'])

############### FASE 4 - Creo columnas N4, trato el campo INT_BRUTO y campos TT de salida ############################################

filas4 = []
cont2 = 0
sw = 1
for _, fila4 in df_principal3.iterrows():

    # Variables temporales
    v_numBonos = int(fila4['NUM_BONOS'])
    v_tIntBrut = float(fila4['INT_BRUTO'])
    v_totAmoPr = float(fila4['T_AP'])
    v_amoPrinc = float(fila4['AP'])
    v_intBruto = float(fila4['IB'])

    # Reinicio el contador para cada sub-grupo de N2    
    if sw == fila4['N2']:
        cont2 = cont2 + 1
    else:
        sw = fila4['N2']
        cont2 = 1

    # Creo variables de salida TT1 y TT2        
    if cont2 == 1:
        TT2 = (v_intBruto + v_tIntBrut) * v_numBonos
        TT1 = (v_totAmoPr - v_amoPrinc) * v_numBonos
    else:
        TT2 = v_intBruto * v_numBonos
        TT1  =  TT1 - (v_amoPrinc * v_numBonos)

    filas4.append({
        'N0': fila4['N0'],
        'N1': fila4['N1'],
        'N2': fila4['N2'],
        'N3': fila4['N3'],
        'N4': cont2,
        'BONO': fila4['BONO'],
        'FECHA': fila4['FECHA'],
        'ISIN': fila4['ISIN'],
        'NUM_BONOS': fila4['NUM_BONOS'],
        'INT_BRUTO': float(fila4['INT_BRUTO']) if cont2 == 1 else 0,
        'TAA': fila4['TAA'],
        'AP': fila4['AP'],
        'IB': fila4['IB'],
        'T_AP': fila4['T_AP'],
        'TT1': float(TT1),
        'TT2': float(TT2)
    })
    sw = fila4['N2']
# Creo el dataframe
df_principal4 = pd.DataFrame(filas4)

### ELIMINO CAMPOS NO NECESARIOS
df_principal5 = df_principal4.drop(['N1', 'N3'], axis=1).copy()

### REDONDEO DE COLUMNAS
df_principal5['TT1'] = df_principal5['TT1'].round(2) 
df_principal5['TT2'] = df_principal5['TT2'].round(2)

############### FASE 5 - Eliminamos registros con ultimo valor a CERO ############################################
filas5 = []
G = 1
cont5 = 0

for _, fila5 in df_principal5.iterrows():
    cont5 = cont5 + 1
    if int(fila5['N2']) == G:
        filas5.append({
            'N0': fila5['N0'],
            'N2': fila5['N2'],
            'N4': fila5['N4'],
            'BONO': fila5['BONO'],
            'FECHA': fila5['FECHA'],
            'ISIN': fila5['ISIN'],
            'NUM_BONOS': fila5['NUM_BONOS'],
            'INT_BRUTO': fila5['INT_BRUTO'],
            'TAA': fila5['TAA'],
            'AP': fila5['AP'],
            'IB': fila5['IB'],
            'T_AP': fila5['T_AP'],
            'TT1': fila5['TT1'],
            'TT2': fila5['TT2']
        })

        if int(fila5['TT1']) == 0:
            if int(fila5['N2']) == 1:
                G = 2
            if int(fila5['N2']) == 2:
                G = 3
            if int(fila5['N2']) == 3:
                G = 1
        
df_principal6 = pd.DataFrame(filas5)

############### FASE 6 - Creamos la columna CALL_DATE y FIRST_DATE ############################################
# CALL_DATE:  es el ultimo valor de FECHA
# FIRST_DATE: es el primer valor de FECHA

# Me quedo con la Fecha Maxima y Minima agrupando N2, BONO N4
df_calldate_max = df_principal6.loc[df_principal6.groupby(['N2', 'BONO'])['N4'].idxmax(), ['N2', 'N4', 'BONO', 'FECHA']]
df_calldate_min = df_principal6.loc[df_principal6.groupby(['N2', 'BONO'])['N4'].idxmin(), ['N2', 'N4', 'BONO', 'FECHA']]

# Renombra campo
df_calldate_max = df_calldate_max.rename(columns={'FECHA': 'CALL_DATE'})
df_calldate_min = df_calldate_min.rename(columns={'FECHA': 'FIRST_DATE'})

# Creamos una copia para no alterar df_principal6
df_principal7 = df_principal6.copy()

# Hacemos merge (left join) 
df_principal7 = df_principal7.merge(
    df_calldate_max[['N2', 'BONO', 'CALL_DATE']],   # solo campos necesarios
    on=['N2', 'BONO'],
    how='left',                                 # mantiene todo df_principal6
    suffixes=('', '_nuevo')                     # evita conflictos si ya existe FECHA
)

# Hacemos merge (left join) 
df_principal7 = df_principal7.merge(
    df_calldate_min[['N2', 'BONO', 'FIRST_DATE']],   # solo campos necesarios
    on=['N2', 'BONO'],
    how='left',                                 # mantiene todo df_principal6
    suffixes=('', '_nuevo')                     # evita conflictos si ya existe FECHA
)

############### FASE 7 - Crear el campo DATED_DATE  ############################################
# Será un campo calculado, teniendo en cuenta el campo FECHA, restamos 3 
# meses atrás, si cae en sábado o domingo pillamos el 1º día hábil

# Creamos una copia para no alterar df_principal
df_principal8 = df_principal7.copy()

# Convertir FECHA a datetime temporalmente (sin modificar la columna original)
fechas_dt = pd.to_datetime(df_principal8['FECHA'], format='%d/%m/%Y')

# Restar 3 meses
fechas_menos_3m = fechas_dt - pd.DateOffset(months=3)

# Ajustar al primer día hábil del mes resultante
# Si el primer día del mes es sábado o domingo, lo mueve al lunes siguiente
primer_dia_habil = fechas_menos_3m.dt.to_period('M').dt.to_timestamp()  # primer día del mes
primer_dia_habil = primer_dia_habil.apply(lambda d: d + pd.offsets.BDay(0) if d.weekday() < 5 else d + pd.offsets.BDay(1))

# Convertir al formato dd/mm/yyyy
df_principal8['DATED_DATE'] = primer_dia_habil.dt.strftime('%d/%m/%Y')

############### FASE 8 - Agregamos un registro nuevo: Sera un reg CALCULADO en la posición 0 ############################################
filas8 = []
for _, fila8 in df_principal8.iterrows():
    if fila8['N4'] == 1:
        v_TT1 = fila8['T_AP'] * fila8['NUM_BONOS']
        filas8.append({
            'N0': fila8['N0'],
            'N2': fila8['N2'],
            'N4': 0,
            'BONO': fila8['BONO'],
            'FECHA': fila8['DATED_DATE'],
            'ISIN': fila8['ISIN'],
            'NUM_BONOS': fila8['NUM_BONOS'],
            'INT_BRUTO': fila8['INT_BRUTO'],
            'TAA': fila8['TAA'],
            'AP': fila8['AP'],
            'IB': fila8['IB'],
            'T_AP': fila8['T_AP'],
            'TT1': v_TT1,
            'TT2': 0,
            'CALL_DATE': fila8['CALL_DATE'],
            'FIRST_DATE': fila8['FIRST_DATE'],
            'DATED_DATE': fila8['DATED_DATE']
        })
    filas8.append({
            'N0': fila8['N0'],
            'N2': fila8['N2'],
            'N4': fila8['N4'],
            'BONO': fila8['BONO'],
            'FECHA': fila8['FECHA'],
            'ISIN': fila8['ISIN'],
            'NUM_BONOS': fila8['NUM_BONOS'],
            'INT_BRUTO': fila8['INT_BRUTO'],
            'TAA': fila8['TAA'],
            'AP': fila8['AP'],
            'IB': fila8['IB'],
            'T_AP': fila8['T_AP'],
            'TT1': fila8['TT1'],
            'TT2': fila8['TT2'],
            'CALL_DATE': fila8['CALL_DATE'],
            'FIRST_DATE': fila8['FIRST_DATE'],
            'DATED_DATE': fila8['DATED_DATE']
    }) 
df_principal9 = pd.DataFrame(filas8)

############### RESULTADO ############################################
print(df_principal9.head(10))
df_principal9.to_excel('/home/robot/Python/proy_py_ia_pdf_lnx/tmp/a_R3.xlsx', sheet_name='hoja1', index=False)


############### FASE 9 - Construir la SALIDA a fichero EXCEL ############################################

# Abrir el archivo una sola vez en modo escritura
with open("/home/robot/Python/proy_py_ia_pdf_lnx/tmp/a_R3.txt", "w", encoding="utf-8") as f:
    l01 = f"mccf version: 1.0\n"
    l02 = f"sender: Titulización de Activos\n"
    l03 = f"phone: +34 917020808\n"
    l04 = f"autorelease: replace\n"
    f.write(l01)
    f.write(l02)
    f.write(l03)
    f.write(l04)

    for _, fila9 in df_principal9.iterrows():
        if fila9['N4'] == 0:
            l05 = f"new flow:\n"                        #FIJO
            l06 = f"cusip: {fila9['ISIN']}\n"
            l07 = f"prepay speed: {fila9['TAA']}\n"
            l08 = f"prepay type: CPR\n"                 #FIJO
            l09 = f"first payment date: {fila9['FIRST_DATE']}\n"
            l10 = f"dated date: {fila9['DATED_DATE']}\n"
            l11 = f"frequency: 04\n"                    #FIJO
            l12 = f"call date: {fila9['CALL_DATE']}\n"
            l13 = f"assumed collateral: no\n"           #FIJO
            l14 = f"vectors: balances interests\n"      #FIJO
            l15 = f"{fila9['FECHA']}\t{fila9['TT1']}\t{fila9['TT2']}\n"
            f.write(l05)
            f.write(l06)
            f.write(l07)
            f.write(l08)
            f.write(l09)
            f.write(l10)
            f.write(l11)
            f.write(l12)
            f.write(l13)
            f.write(l14)
            f.write(l15)
        else:
            l16 = f"{fila9['FECHA']}\t{fila9['TT1']}\t{fila9['TT2']}\n"
            f.write(l16)

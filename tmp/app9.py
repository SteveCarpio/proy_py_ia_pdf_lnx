import pandas as pd
import datetime
import re

pd.set_option('display.max_rows', None) 

# Ruta al archivo Excel en tu servidor
ruta_excel = "/home/robot/Python/proy_py_ia_pdf_lnx/excel/TDACAM9_INFFLUJOS_ES_202509.xls"

tipoExcel = "TDACAM9_INFFLUJOS_ES_202509.xls"

if "TDACAM9_INFFLUJOS_ES" in tipoExcel:
    dic_nomBono = [
        {'BONO': 'Bono-A1','NUM_BONOS': 100},
        {'BONO': 'Bono-A2','NUM_BONOS': 100},
        {'BONO': 'Bono-A3','NUM_BONOS': 100},
        {'BONO': 'Bono-B','NUM_BONOS': 100},
        {'BONO': 'Bono-C','NUM_BONOS': 100},
        {'BONO': 'Bono-D','NUM_BONOS': 100}
    ]
    df_numBono = pd.DataFrame(dic_nomBono)


# Lee el archivo sin encabezados
df_excel = pd.read_excel(ruta_excel, header=None, dtype=str)

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
    # Agrego cada valor de cada celda en una variable
    var_a, var_b, var_c, var_d, var_e, var_f, var_g, var_h, var_i, var_j, var_k, var_l, var_m = str(fila[0]), str(fila[1]), str(fila[2]), str(fila[3]), str(fila[4]), str(fila[5]), str(fila[6]), str(fila[7]), str(fila[8]), str(fila[9]), str(fila[10]), str(fila[11]), str(fila[12])

    ############## Creo la LISTA de [ BONOS ] 
    if "Bono" in var_e:
        isinX1 = df_excel.iloc[idx + 3, 3]
        isinX2 = df_excel.iloc[idx + 3, 10]
        taaX1 = float(df_excel.iloc[idx + 7, 3]) * 100
        taaX2 = float(df_excel.iloc[idx + 7, 5]) * 100
        taaX3 = float(df_excel.iloc[idx + 7, 7]) * 100
        taaX4 = float(df_excel.iloc[idx + 7, 10]) * 100
        taaX5 = float(df_excel.iloc[idx + 7, 12]) * 100
        taaX6 = float(df_excel.iloc[idx + 7, 14]) * 100
        filas_bono1.append([var_e.strip(), isinX1.strip(), taaX1, taaX2, taaX3])
        if var_l != "":
                filas_bono1.append([var_l.strip(), isinX2.strip(), taaX4, taaX5, taaX6])
    
    ############## Creo la LISTA [ TABLA_BONO ]
    # Leo la variable Bono
    if "Bono" in var_i:
        bonoX = var_i.strip()

    if bonoX != "":
        if var_c.strip() != "" and var_c.strip() != "Fecha" and var_c.strip() != "Total" and var_c.strip() != "00:00:00" and var_d != "(*)":
            #print(f'{idx} : {bonoX} - {var_c} - {var_d} - {var_f} : {var_h} - {var_j} : {var_k} - {var_m} ')
            var_c2 = datetime.datetime.strptime(var_c, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
            filas_bono2.append([bonoX, var_c2, round(float(var_d),2), round(float(var_f),2), round(float(var_h),2), round(float(var_j),2), round(float(var_k),2), round(float(var_m),2)])

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



### TRATAMIENTO DATAFRAME: BONO2
df_bono2 = pd.DataFrame(filas_bono2, columns=['BONO', 'FECHA', 'AP_1', 'IB_1', 'AP_2', 'IB_2', 'AP_3', 'IB_3'])

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
v_tt1 = 1

for _, fila5 in df_principal5.iterrows():

    if v_tt1 > 0:
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

    v_n2 = int(fila5['N2'])
    v_tt1 = int(fila5['TT1'])

df_principal6 = pd.DataFrame(filas5)


print(df_principal6.head(20))
df_principal6.to_excel('/home/robot/Python/proy_py_ia_pdf_lnx/tmp/a_R3.xlsx', sheet_name='hoja1', index=False)
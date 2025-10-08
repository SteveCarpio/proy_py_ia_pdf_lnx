import pandas as pd
import datetime
#import re

# Ruta al archivo Excel en tu servidor
ruta_excel = "/home/robot/Python/proy_py_ia_pdf_lnx/excel/TDACAM9_INFFLUJOS_ES_202509.xls"

tipoExcel = "TDACAM9_INFFLUJOS_ES_202509.xls"

if "TDACAM9_INFFLUJOS_ES" in tipoExcel:
    dic_nomBono = [
        {'BONO': 'Bono-A1','NUM_BONOS': 100},
        {'BONO': 'Bono-A2','NUM_BONOS': 200},
        {'BONO': 'Bono-A3','NUM_BONOS': 300},
        {'BONO': 'Bono-B','NUM_BONOS': 400},
        {'BONO': 'Bono-C','NUM_BONOS': 500},
        {'BONO': 'Bono-D','NUM_BONOS': 600}
    ]
    df_numBono = pd.DataFrame(dic_nomBono)


# Lee el archivo sin encabezados
df_excel = pd.read_excel(ruta_excel, header=None, dtype=str)

# Reemplaza NaN por cadena vacía en todo el DataFrame
df_excel = df_excel.fillna('')

# Crea una lista y variables de apoyo
filas_bono1 = []
filas_bono2 = []
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

    # ------- Fin del Bucle -------
    if var_c == "":
        contBlancos = contBlancos + 1
        if contBlancos > 50:
            print("---- FIN ----")
            break
    else:
        contBlancos = 0


############### RESULTADO1 ############################################
### TRATAMIENTO DATAFRAME: BONO1
df_bono1 = pd.DataFrame(filas_bono1, columns=['BONO', 'ISIN', 'TAA_1', 'TAA_2', 'TAA_3'])
df_bono1_union = pd.merge(df_bono1, df_numBono, on='BONO')

### TRATAMIENTO DATAFRAME: BONO2
df_bono2 = pd.DataFrame(filas_bono2, columns=['BONO', 'FECHA', 'AP_1', 'IB_1', 'AP_2', 'IB_2', 'AP_3', 'IB_3'])

### UNION DATAFRAME BONO1 y BONO2
df_union1 = pd.merge(df_bono1_union, df_bono2, on='BONO')
df_union1 = df_union1.reindex(columns=['BONO', 'FECHA', 'ISIN', 'NUM_BONOS', 'TAA_1', 'AP_1', 'IB_1', 'TAA_2', 'AP_2', 'IB_2', 'TAA_3', 'AP_3', 'IB_3'])

#print("--- RESULTADO 1 ---")
#print(df_union1.head(20))

############### RESULTADO2 ############################################

### AGRUPAR BONOS Y SUMAR TOTALES
df_bono2_totales = df_bono2.groupby('BONO')[['AP_1', 'AP_2', 'AP_3']].sum().reset_index()

### RENOMBRAR COLUMNAS
df_bono2_totales.rename(columns={'AP_1': 'T_AP_1', 'AP_2': 'T_AP_2', 'AP_3': 'T_AP_3'}, inplace=True)

### AGREGAR RESULTADO 2 AL DF PRINCIPAL
df_principal1 = pd.merge(df_bono2_totales, df_union1, on='BONO')

### ORDENAR CAMPOS
df_principal1 = df_principal1.reindex(columns=['BONO', 'FECHA', 'ISIN', 'NUM_BONOS', 'TAA_1', 'AP_1', 'IB_1', 'T_AP_1', 'TAA_2', 'AP_2', 'IB_2', 'T_AP_2', 'TAA_3', 'AP_3', 'IB_3', 'T_AP_3'])

print("\n--- RESULTADO 2 ---")
print(df_bono2_totales)
print(df_principal1)
pd.set_option('display.max_rows', None) 

############### RESULTADO3 ############################################

print("\n--- RESULTADO 3 ---")
#df_resultado3_1 = df_principal1.copy()     # copia del DataFrame original
#df_resultado3_1['AP'] = (df_resultado3_1['campo1'] - df_resultado3_1['campo2']) * df_resultado3_1['campo3']

import pandas as pd

# Columnas fijas que no cambian
cols_fijas = ['BONO', 'FECHA', 'ISIN', 'NUM_BONOS']

# Detectamos automáticamente los grupos (_1, _2, _3, etc.)
grupos = sorted({col.split('_')[-1] for col in df_principal1.columns if '_' in col and col.split('_')[-1].isdigit()},
                key=int)

# Lista donde iremos guardando las filas transformadas
filas = []

# Recorremos cada fila del DF original
for _, fila in df_principal1.iterrows():
    for i in grupos:
        filas.append({
            'BONO': fila['BONO'],
            'FECHA': fila['FECHA'],
            'ISIN': fila['ISIN'],
            'NUM_BONOS': fila['NUM_BONOS'],
            'TAA': fila[f'TAA_{i}'],
            'AP': fila[f'AP_{i}'],
            'IB': fila[f'IB_{i}'],
            'T_AP': fila[f'T_AP_{i}']
        })

# Creamos el nuevo DataFrame
df_principal2 = pd.DataFrame(filas)

# Reordenamos para mantener el orden por BONO y por grupo (TAA_1, TAA_2, TAA_3)
df_principal2 = df_principal2.sort_values(by=['BONO','TAA','FECHA']).reset_index(drop=True)

print(df_principal2.head(200))

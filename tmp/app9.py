import pandas as pd
#import re

# Ruta al archivo Excel en tu servidor
ruta_excel = "/home/robot/Python/proy_py_ia_pdf_lnx/excel/TDACAM9_INFFLUJOS_ES_202509.xls"

# Lee el archivo sin encabezados
df_excel = pd.read_excel(ruta_excel, header=None, dtype=str)

# Reemplaza NaN por cadena vacía en todo el DataFrame
df_excel = df_excel.fillna('')

# Crea una lista y variables de apoyo
filas_bono1 = []
filas_bono2 = []
bonoX1, bonoX2, isinX1, isinX2, taaX1, taaX2, taaX3, taaX4, taaX5, taaX6 = "", "", "", "", "", "", "", "", "",""

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
    

    ############## Creo la LISTA [ TABLA_BOBO ]
    

    # Fin del Bucle
    if var_b == 'Escenarios de flujos futuros de los bonos unitarios':
        print("FIN")
        break

############### RESULTADO ############################################
# Creo la tabla de BONOS en un DataFrame
df_bono = pd.DataFrame(filas_bono1, columns=['BONO', 'ISIN', 'TAA_1', 'TAA_2', 'TAA_3'])
print(df_bono)
print(len(df_bono))

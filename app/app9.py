import streamlit as st

def main():
    import plotly.express as px
    import pandas as pd
    import io
    import sys

    list_flujos = [
        'ParaQueEmpieceDesdeEl_01',
        'FTPYMETDACAM4_INFFLUJOS_ES',     # 01 - (Bono-B   , Bono-C   , Bono-D                                                    ) pyme_cam4_web0925.xls
        'PENEDESFTGENCAT1_INFFLUJOS_ES',  # 02 - (Bono-C                                                                          ) PENEDES FTGENCAT 1_web0925.xls
        'PENEDESPYMES1_INFFLUJOS_ES',     # 03 - (Bono-C                                                                          ) CAIXA_PENEDES_PYMES1_web0925.xls
        'SABADELL5_INFFLUJOS_ES',         # 04 - (Bono-A   , Bono-B                                                               ) SABADELL5_web0925.xls
        'SCFAUTOS_INFFLUJOS_ES',          # 05 - (Bono-A   , Bono-B   , Bono-C  , Bono-D  , Bono-E  , Bono-F                      ) SCFAUTOS_web0925.xls 
        'SCFAUTOS_2_INFFLUJOS_ES',        # 06 - (Bono-A   , Bono-B   , Bono-C  , Bono-D  , Bono-E  , Bono-F                      ) none: sTv este registro se borra más abajo en el DF
        'TDA26_INFFLUJOS_ES',             # 07 - (Bono 1-A1, Bono 1-A2, Bono 1-B, Bono 1-C, Bono 1-D, Bono 2-A, Bono 2-B, Bono 2-C) TDA26_web0925.xls
        'TDA29_INFFLUJOS_ES',             # 08 - (Serie-A1 , Serie-A2 , Serie-B , Serie-C , Serie-D                               ) tda29_web0925.xls
        'TDACAM4_INFFLUJOS_ES',           # 09 - (Bono-A   , Bono-B                                                               ) TDACAM4_web1025.xls
        'TDACAM5_INFFLUJOS_ES',           # 10 - (Bono-A   , Bono-B                                                               ) TDACAM5_web0925.xls
        'TDACAM6_INFFLUJOS_ES',           # 11 - (Bono-A3  , Bono-B                                                               ) TDACAM6_web0925.xls
        'TDACAM7_INFFLUJOS_ES',           # 12 - (Bono-A2  , Bono-A3  , Bono-B                                                    ) TDACAM7_web0925.xls
        'TDACAM8_INFFLUJOS_ES',           # 13 - (Bono-A   , Bono-B   , Bono-C  , Bono-D                                          ) TDACAM8_web0925.xls
        'TDACAM9_INFFLUJOS_ES',           # 14 - (Bono-A1  , Bono-A2  , Bono-A3 , Bono-B  , Bono-C  , Bono-D                      ) TDACAM9_web0925.xls
        'TDACAM11_INFFLUJOS_ES',          # 15 - (Bono-A1  , Bono-A2  , Bono-A3 , Bono-A4 , Bono-B  , Bono-C  , Bono-D            ) none: sTv este registro se borra más abajo en el DF
        'TDAPENEDES1_INFFLUJOS_ES'        # 16 - (Bono-A   , Bono-B   , Bono-C                                                    ) CAIXA_PENEDES1_web0925.xls
        ]

    # ================================================
    # FUNCIONES AUXILIARES
    # ================================================

    def get_dic_nomBono(file_name: str):
        """Devuelve el diccionario de bonos según el nombre del fichero."""

        if list_flujos[1] in file_name:
            dic_nomBono = [
                {'BONO': 'Bono B','NUM_BONOS': 100},
                {'BONO': 'Bono C','NUM_BONOS': 200},
                {'BONO': 'Bono D','NUM_BONOS': 300}
            ]

        elif list_flujos[2] in file_name:
            dic_nomBono = [
                {'BONO': 'Bono-C','NUM_BONOS': 100}
            ]

        elif list_flujos[3] in file_name:
            dic_nomBono = [
                {'BONO': 'Bono-C','NUM_BONOS': 100}
            ]

        elif list_flujos[4] in file_name:
            dic_nomBono = [
                {'BONO': 'Bono-A','NUM_BONOS': 100},
                {'BONO': 'Bono-B','NUM_BONOS': 200}
            ]

        elif list_flujos[5] in file_name:
            dic_nomBono = [
                {'BONO': 'Bono-A','NUM_BONOS': 100},
                {'BONO': 'Bono-B','NUM_BONOS': 200},
                {'BONO': 'Bono-C','NUM_BONOS': 300},
                {'BONO': 'Bono-D','NUM_BONOS': 400},
                {'BONO': 'Bono-E','NUM_BONOS': 500},
                {'BONO': 'Bono-F','NUM_BONOS': 600}
            ]
        
        #elif list_flujos[6] in file_name:
        #    dic_nomBono = [
        #        {'BONO': 'Bono-A','NUM_BONOS': 100},
        #        {'BONO': 'Bono-B','NUM_BONOS': 200},
        #        {'BONO': 'Bono-C','NUM_BONOS': 300},
        #        {'BONO': 'Bono-D','NUM_BONOS': 400},
        #        {'BONO': 'Bono-E','NUM_BONOS': 500},
        #        {'BONO': 'Bono-F','NUM_BONOS': 600}
        #    ]
        
        elif list_flujos[7] in file_name:
            dic_nomBono = [
                {'BONO': 'Bono 1-A1','NUM_BONOS': 100},
                {'BONO': 'Bono 1-A2','NUM_BONOS': 200},
                {'BONO': 'Bono 1-B','NUM_BONOS': 300},
                {'BONO': 'Bono 1-C','NUM_BONOS': 400},
                {'BONO': 'Bono 1-D','NUM_BONOS': 500},
                {'BONO': 'Bono 2-A','NUM_BONOS': 600},
                {'BONO': 'Bono 2-B','NUM_BONOS': 700},
                {'BONO': 'Bono 2-C','NUM_BONOS': 800}
            ]

        elif list_flujos[8] in file_name:
            dic_nomBono = [
                {'BONO': 'Serie-A1','NUM_BONOS': 100},
                {'BONO': 'Serie-A2','NUM_BONOS': 200},
                {'BONO': 'Serie-B','NUM_BONOS': 300},
                {'BONO': 'Serie-C','NUM_BONOS': 400},
                {'BONO': 'Serie-D','NUM_BONOS': 500}
            ]

        elif list_flujos[9] in file_name:
            dic_nomBono = [
                {'BONO': 'Bono-A','NUM_BONOS': 100},
                {'BONO': 'Bono-B','NUM_BONOS': 200}
            ]

        elif list_flujos[10] in file_name:
            dic_nomBono = [
                {'BONO': 'Bono-A','NUM_BONOS': 100},
                {'BONO': 'Bono-B','NUM_BONOS': 200}
            ]

        elif list_flujos[11] in file_name:
            dic_nomBono = [
                {'BONO': 'Bono-A3','NUM_BONOS': 100},
                {'BONO': 'Bono-B','NUM_BONOS': 200}
            ]

        elif list_flujos[12] in file_name:
            dic_nomBono = [
                {'BONO': 'Bono-A2','NUM_BONOS': 100},
                {'BONO': 'Bono-A3','NUM_BONOS': 200},
                {'BONO': 'Bono-B','NUM_BONOS': 300}
            ]

        elif list_flujos[13] in file_name:
            dic_nomBono = [
                {'BONO': 'Bono-A','NUM_BONOS': 100},
                {'BONO': 'Bono-B','NUM_BONOS': 200},
                {'BONO': 'Bono-C','NUM_BONOS': 300},
                {'BONO': 'Bono-D','NUM_BONOS': 400}
            ]

        elif list_flujos[14] in file_name:
            dic_nomBono = [
                {'BONO': 'Bono-A1','NUM_BONOS': 100},
                {'BONO': 'Bono-A2','NUM_BONOS': 200},
                {'BONO': 'Bono-A3','NUM_BONOS': 300},
                {'BONO': 'Bono-B','NUM_BONOS': 400},
                {'BONO': 'Bono-C','NUM_BONOS': 500},
                {'BONO': 'Bono-D','NUM_BONOS': 600}
            ]
        
        #elif list_flujos[15] in file_name:
        #    dic_nomBono = [
        #        {'BONO': 'Bono-A1','NUM_BONOS': 100},
        #        {'BONO': 'Bono-A2','NUM_BONOS': 200},
        #        {'BONO': 'Bono-A3','NUM_BONOS': 300},
        #        {'BONO': 'Bono-A4','NUM_BONOS': 400},
        #        {'BONO': 'Bono-B','NUM_BONOS': 500},
        #        {'BONO': 'Bono-C','NUM_BONOS': 600},
        #        {'BONO': 'Bono-D','NUM_BONOS': 700}
        #    ]
        
        elif list_flujos[16] in file_name:
            dic_nomBono = [
                {'BONO': 'Bono-A','NUM_BONOS': 100},
                {'BONO': 'Bono-B','NUM_BONOS': 200},
                {'BONO': 'Bono-C','NUM_BONOS': 300}
            ]

        else:
            dic_nomBono = []
        return dic_nomBono


    # ================================================
    # FUNCIÓN DE PROCESAMIENTO
    # ================================================

    ##########################
    def procesar_datos2(df_excel: pd.DataFrame, dic_nomBono_actualizado: list):
        import datetime
        import re
        from pandas.tseries.offsets import MonthEnd, MonthBegin, BMonthBegin, DateOffset

        # Crea el dataFrame de numBonos
        df_numBono = pd.DataFrame(dic_nomBono_actualizado)

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
            #st.write(f"{idx}:{fila}XXX")     #  DEBUG
            # Agrego cada valor de cada celda en una variable
            var_a, var_b, var_c, var_d, var_e, var_f, var_g, var_h, var_i, var_j, var_k, var_l, var_m = str(fila[0]), str(fila[1]), str(fila[2]), str(fila[3]), str(fila[4]), str(fila[5]), str(fila[6]), str(fila[7]), str(fila[8]), str(fila[9]), str(fila[10]), str(fila[11]), str(fila[12])
            #st.write(f'{idx} : {bonoX} - {var_c} | {var_d} : {var_f} | {var_h} : {var_j} | {var_k} : {var_m} ')        #  DEBUG

            ############## Creo la LISTA de [ BONOS ] 
            #if "Bono" in var_e:
            if "Bono" in var_e or "Serie" in var_e: 
                #st.write(f'{idx} : {var_e} - {var_c} | {var_d} : {var_f} | {var_h} : {var_j} | {var_k} : {var_m} ')        #  DEBUG

                isinX1 = df_excel.iloc[idx + 3, 3]
                isinX2 = df_excel.iloc[idx + 3, 10]

                #taaX1 = float(df_excel.iloc[idx + 7, 3]) * 100
                #taaX2 = float(df_excel.iloc[idx + 7, 5]) * 100
                #taaX3 = float(df_excel.iloc[idx + 7, 7]) * 100
                #taaX4 = float(df_excel.iloc[idx + 7, 10]) * 100
                #taaX5 = float(df_excel.iloc[idx + 7, 12]) * 100
                #taaX6 = float(df_excel.iloc[idx + 7, 14]) * 100

                valor1 = df_excel.iloc[idx + 7, 3]
                taaX1 = float(valor1) * 100 if str(valor1).strip() not in ("", "-") else 0.0

                valor2 = df_excel.iloc[idx + 7, 5]
                taaX2 = float(valor2) * 100 if str(valor2).strip() not in ("", "-") else 0.0

                valor3 = df_excel.iloc[idx + 7, 7]
                taaX3 = float(valor3) * 100 if str(valor3).strip() not in ("", "-") else 0.0

                valor4 = df_excel.iloc[idx + 7, 10]
                taaX4 = float(valor4) * 100 if str(valor4).strip() not in ("", "-") else 0.0
                
                valor5 = df_excel.iloc[idx + 7, 12]
                taaX5 = float(valor5) * 100 if str(valor5).strip() not in ("", "-") else 0.0
                
                valor6 = df_excel.iloc[idx + 7, 14]
                taaX6 = float(valor6) * 100 if str(valor6).strip() not in ("", "-") else 0.0

                filas_bono1.append([var_e.strip(), isinX1.strip(), taaX1, taaX2, taaX3])
                if var_l != "":
                        filas_bono1.append([var_l.strip(), isinX2.strip(), taaX4, taaX5, taaX6])
                #st.write(filas_bono1)     #  DEBUG

            ############## Creo la LISTA [ TABLA_BONO ]
            # Leo la variable Bono
            #if "Bono" in var_i:
            if "Bono" in var_i or "Serie" in var_i:
                bonoX = var_i.strip()
                #st.write(bonoX)   #  DEBUG

            if bonoX != "":
                #st.write(f'{idx} : {bonoX} - {var_c} | {var_d} : {var_f} | {var_h} : {var_j} | {var_k} : {var_m} ')        #  DEBUG
                if var_c.strip() != "" and var_c.strip() != "Fecha" and var_c.strip() != "Total" and var_c.strip() != "00:00:00" and var_d != "(*)" and re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", var_c):
                    var_c2 = datetime.datetime.strptime(var_c, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
                    filas_bono2.append([bonoX, var_c2, round(float(var_d),2), round(float(var_f),2), round(float(var_h),2), round(float(var_j),2), round(float(var_k),2), round(float(var_m),2)])
                    #st.write(f'{idx} : {bonoX} - {var_c} | {var_d} - {var_f} | {var_h} - {var_j} | {var_k} - {var_m} ')        #  DEBUG

            if var_d == "(*)":
                filas_bono3.append([bonoX, var_f])
                #st.write(filas_bono3)     #  DEBUG
            
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
        #st.write(df_bono1_union)    #  DEBUG

        ### TRATAMIENTO DATAFRAME: BONO2
        df_bono2 = pd.DataFrame(filas_bono2, columns=['BONO', 'FECHA', 'AP_1', 'IB_1', 'AP_2', 'IB_2', 'AP_3', 'IB_3'])
        print(df_bono2.head(10))

        ### TRATAMIENTO DATAFRAME: BONO3 --> INTERES BRUTO
        df_bono3 = pd.DataFrame(filas_bono3, columns=['BONO', 'INT_BRUTO'])


        ### UNION BONO1 y BONO3: Agregar a la tabla bono1 el campo Ineres Bruto
        df_bono3_union = pd.merge(df_bono3, df_bono1_union, on='BONO')

        #st.write(df_bono3_union.to_html(index=False), unsafe_allow_html=True)

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

        ### CREAR TABLA y GRAFICO PARA PRESENTARLA SOLO EN STREAMLIT
        df_cuadro_bonos = pd.merge(df_bono2_totales, df_bono3_union, on='BONO')
        df_cuadro_bonos = df_cuadro_bonos.reindex(columns=['BONO', 'ISIN', 'NUM_BONOS', 'INT_BRUTO', 'TAA_1', 'T_AP_1', 'TAA_2', 'T_AP_2', 'TAA_3', 'T_AP_3'])

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

        ############### FASE 8 - Agregamos un registro nuevo: Sera un reg CALCULADO en la posición 0 #####################
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
        #print(df_principal9.head(10))
        rutaSalida="/home/robot/Python/proy_py_ia_pdf_lnx/tmp/"
        fileSalida="FLUJOS_BLOOMBERG"

        df_principal9.to_excel(f'{rutaSalida}{fileSalida}.xlsx', sheet_name='hoja1', index=False)


        ############### FASE 9 - Construir la SALIDA a fichero EXCEL ############################################

        # Abrir el archivo una sola vez en modo escritura
        with open(f'{rutaSalida}{fileSalida}.txt', "w", encoding="utf-8") as f:
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

        return rutaSalida, fileSalida, df_principal9, df_cuadro_bonos


    # ================================================
    # INTERFAZ STREAMLIT
    # ================================================

    st.title("📈 Carga de flujos de Sabadell para Bloomberg")
    st.caption("Aplicación de automatización que extrae y procesa los flujos de Sabadell que se encuentran en archivos Excel y los convierte en archivos TXT totalmente compatibles con Bloomberg.")

    st.sidebar.subheader("📈 : Flujos Bloomberg")

    # Subir fichero
    file_excel = st.sidebar.file_uploader("📁 Sube un fichero Excel", type=["xls", "xlsx"])

    # Mostrar lista de Excel Activos
    #st.info(" Carga de parámetros")
    with st.expander("📄 Lista de ficheros excel de 'Flujos' activos en la Aplicación:"):
        df_lstFlujos = pd.DataFrame(list_flujos, columns=['Excel_de_Flujos_Admitidos'])
        df_lstFlujos.drop(index=0, inplace=True)   # Borrra el primer registro
        df_lstFlujos.drop(df_lstFlujos[df_lstFlujos['Excel_de_Flujos_Admitidos'] == 'SCFAUTOS_2_INFFLUJOS_ES'].index, inplace=True)
        df_lstFlujos.drop(df_lstFlujos[df_lstFlujos['Excel_de_Flujos_Admitidos'] == 'TDACAM11_INFFLUJOS_ES'].index, inplace=True)
        df_lstFlujos.reset_index(drop=True, inplace=True) 
        df_lstFlujos.index += 1
        st.table(df_lstFlujos)

    if file_excel:
        file_name = file_excel.name
        file_name_sin_extension = file_name.split('.')[0]
        #st.sidebar.write(f"**Archivo cargado:** {file_name}")

        dic_nomBono = get_dic_nomBono(file_name)
        
        if not dic_nomBono:
            st.warning("⚠️ No se reconoce el tipo de fichero. No hay diccionario asociado.")
        else:
            #st.sidebar.subheader("Bonos Activos:")
            
            # Convertir a DataFrame
            df_nomBono = pd.DataFrame(dic_nomBono)
            df_nomBono.reset_index(drop=True, inplace=True)
            df_nomBono.index += 1

            # Permitir eliminar filas
            bonos_to_remove = st.sidebar.multiselect(
                "🗑️ Selecciona bonos a eliminar:",
                options=df_nomBono["BONO"].tolist()
            )

            if bonos_to_remove:
                df_nomBono = df_nomBono[~df_nomBono["BONO"].isin(bonos_to_remove)]

            # Tabla editable
            #st.caption(f"*** Opcional: Edita el campo (NUM_BONOS) si es necesario para tratar el fichero: {file_name_sin_extension}.xls")
            #st.caption(f"*** Importante: Comprobar que el nombre del campo BONO este igual en el excel, ejm: '**Bono A**' no es igual que '**Bono-A**'")
            #with st.sidebar.expander("📄 Modificar Número de Bonos"):
            #    edited_df = st.data_editor(
            #        df_nomBono,
            #        num_rows="fixed",
            #        key="editor_nomBono"
            #    )
            edited_df = st.sidebar.data_editor(
                df_nomBono,
                num_rows="fixed",
                key="editor_nomBono"
                )

            dic_nomBono_actualizado = edited_df.to_dict(orient="records")

            # Leer el Excel
            try:
                df_excel = pd.read_excel(file_excel, header=None, dtype=str)
            except Exception as e:
                st.error(f"Error al leer el Excel: {e}")
                df_excel = None

            # ================================================
            # BOTÓN PARA PROCESAR DATOS
            # ================================================
            if st.sidebar.button("🔄 Procesar datos"):
                if df_excel is not None:
                    # Procesar el archivo
                    rutaSalida, fileSalida, df_principal9, df_cuadro_bonos = procesar_datos2(df_excel, dic_nomBono_actualizado)

                    ####################################
                    st.success("✅ Resultado Excel: Datos Procesados")

                    col1, col2 = st.columns([1, 1])

                    with col1:
                        st.write("")
                        st.write("")

                        import streamlit.components.v1 as components
                        # HTML con estilos CSS (ajusta font-size a lo que necesites)
                        html = f"""
                        <style>
                        table {{
                            border-collapse: collapse;
                            font-size: 11px;            /* tamaño de letra */
                        }}
                        table th, table td {{
                            padding: 4px 6px;           /* reduce padding */
                            border: 2px solid #ddd;
                        }}
                        </style>
                        {df_cuadro_bonos.to_html(index=False, escape=False)}
                        """
                        # muestra el HTML dentro de Streamlit (scrolling/height opcional)
                        components.html(html, height=350, scrolling=True)
                      
                    with col2:
                        # Crear gráfico
                        fig = px.bar(
                            df_cuadro_bonos,
                            x="BONO",
                            y=["T_AP_1", "T_AP_2", "T_AP_3"],
                            barmode="group"
                        )

                        # Ajustes visuales
                        fig.update_layout(
                            height=400,
                            margin=dict(t=40, b=10, l=40, r=40),  # menos espacio abajo
                            xaxis_title=None,                     # quitamos título de abajo
                        )

                        # Mover título del eje X arriba
                        fig.add_annotation(
                            text=" ",                   # texto del título
                            xref="paper", yref="paper",
                            x=0.5, y=1.1,               # posición arriba centrada
                            showarrow=False,
                            font=dict(size=14)
                        )

                        # Mostrar gráfico alineado arriba
                        st.plotly_chart(fig, use_container_width=True)
                
                    with st.expander("📄 Ver el resumen de los datos procesados"):
                        st.write(df_principal9)


                    ####################################
                    st.success("✅ Resultado Txt: Flujos Bloomberg")
                    
                    '''
                    # Guardar contenido del TXT en session_state
                    try:
                        with open(f'{rutaSalida}{fileSalida}.txt', "r", encoding="utf-8") as f:
                            st.session_state["contenido_txt"] = f.read()
                        st.session_state["file_name_salida"] = f"{file_name_sin_extension}_SALIDA.txt"
                    except Exception as e:
                        st.error(f"No se pudo leer el archivo generado: {e}")
                    '''

                    try:
                        with open(f'{rutaSalida}{fileSalida}.txt', "r", encoding="utf-8") as f:
                            contenido = f.read()

                        file_name_salida = f"{file_name_sin_extension}_SALIDA.txt"

                        
                        with st.expander(f'📄 Ver el file de salida:  {file_name_salida}', expanded=False):
                            st.code(contenido, language="text")

                        # Botón de descarga
                        st.sidebar.download_button(
                            label=f"💾 Descargar File Txt",
                            data=contenido,
                            file_name=file_name_salida,
                            mime="text/plain"
                        )


                    except Exception as e:
                        st.error(f"No se pudo leer el archivo generado: {e}")


                else:
                    st.error("❌ No se ha podido leer el Excel correctamente.")



            # ================================================
            # MOSTRAR Y DESCARGAR RESULTADOS
            # ================================================
            '''
            if "contenido_txt" in st.session_state:
                # Mostrar en expander
                with st.expander("📄 Ver el contenido del fichero que se cargará en los flujos de Bloomberg"):
                    st.text_area("Contenido del archivo:", st.session_state["contenido_txt"], height=300)

                # Botón de descarga
                st.download_button(
                    label=f"💾 Descargar Flujos Bloomberg: {file_name_sin_extension}.txt",
                    data=st.session_state["contenido_txt"],
                    file_name=st.session_state["file_name_salida"],
                    mime="text/plain"
                )
            '''

if __name__ == "__main__":

    main()

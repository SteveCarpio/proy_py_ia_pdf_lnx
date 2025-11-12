#STEVE: este código me sirvió para agregar los emisores que estaban en los excel a la bbdd qlite.

import pandas as pd
import sqlite3

def CARGA_DATOS(EXCEL_RUTA, DB_RUTA):
    # ---------- 1. Leer el Excel ----------
    df = pd.read_excel(EXCEL_RUTA, sheet_name='FILTRO', engine='openpyxl')
    # Renombrar columnas para que coincidan con la tabla SQLite
    df.rename(columns={'TO': 'TO_EMAIL', 'CC': 'CC_EMAIL'}, inplace=True)
    # Reordenar columnas
    df = df[['CLAVE', 'CODIGO', 'FILTRO', 'ESTADO', 'GRUPO', 'TO_EMAIL', 'CC_EMAIL', 'C3']]

    # ---------- 2. Conectar a SQLite ----------
    conn = sqlite3.connect(DB_RUTA)
    # ---------- 3. Insertar en la tabla ----------
    df.to_sql(name='configuracion', con=conn, if_exists='append', index=False)
    # ---------- 4. Ver contenido de la tabla -------- 

    # ---------- 5. Cerrar conexión ----------    
    conn.close()

# Cambia la ruta al archivo que corresponda
EXCEL_RUTA1 = '/srv/apps/MisCompilados/PROY_BOLSA_MX/BIVA/CONFIG/BIVA_Filtro_Emisores_PRO.xlsx'
DB_RUTA1 = '/home/robot/Python/proy_py_ia_pdf_lnx/data/app10_config_BIVA.db'
EXCEL_RUTA2 = '/srv/apps/MisCompilados/PROY_BOLSA_MX/BMV/CONFIG/BMV_Filtro_Emisores_PRO.xlsx'
DB_RUTA2 = '/home/robot/Python/proy_py_ia_pdf_lnx/data/app10_config_BMV.db'


CARGA_DATOS(EXCEL_RUTA1, DB_RUTA1)
CARGA_DATOS(EXCEL_RUTA2, DB_RUTA2)
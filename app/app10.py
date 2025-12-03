# WebScraping: Eventos Relevantes - BIVA y BMV
import streamlit as st
import sqlite3
import pandas as pd
import pathlib
import datetime
import shutil
import locale
import sys
import os
from datetime import timedelta

# --------------------------
# CONFIGURACIÓN GENERAL
# --------------------------
os.makedirs("data", exist_ok=True)  
DB_FILE1 = "data/app10_config_BIVA.db"
DB_FILE2 = "data/app10_config_BMV.db"
LOG_DIR1 = pathlib.Path("/srv/apps/MisCompilados/PROY_BOLSA_MX/BIVA/LOG")
LOG_DIR2 = pathlib.Path("/srv/apps/MisCompilados/PROY_BOLSA_MX/BMV/LOG")
R_BOLSAS = "/srv/apps/MisCompilados/PROY_BOLSA_MX/"

# -----------------------------------
# EXPORTO BBDD A EXCEL DE PRODUCCION
# -----------------------------------
def export_to_excel(db_path, output_path, table_name="configuracion"):
    """
    Exporta los campos deseados de una tabla SQLite a un archivo Excel.
    """
    # 1️⃣ Conectarse a la base de datos
    try:
        conn = sqlite3.connect(db_path)
    except sqlite3.Error as e:
        print(f"Error al conectar a la BD: {e}")
        sys.exit(1)

    # 2️⃣ Crear la consulta SQL
    query = f"""
        SELECT CLAVE, CODIGO, FILTRO, ESTADO, GRUPO,
               TO_EMAIL, CC_EMAIL, C3
        FROM {table_name}
    """

    # 3️⃣ Cargar los datos en un DataFrame
    try:
        df = pd.read_sql_query(query, conn)
        df.rename(columns={'TO_EMAIL': 'TO', 'CC_EMAIL': 'CC'}, inplace=True)
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        conn.close()
        sys.exit(1)

    # 4️⃣ Cerrar la conexión
    conn.close()

    # 5️⃣ Si el directorio de salida no existe, crearlo
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 6️⃣ Guardar en Excel (xlsx)
    try:
        df.to_excel(output_path, index=False, engine='openpyxl', sheet_name="FILTRO")
        print(f"✅ Exportado con éxito a: {output_path}")
    except Exception as e:
        print(f"Error al escribir el archivo Excel: {e}")
        sys.exit(1)

# --------------------------------------------------
# HAGO UNA COPIA DE SEGURIDAD DEL XLS DE PRODUCCION
# --------------------------------------------------
def copia_seguridad_xls(ruta_fichero):
    """
    Copia 'fichero' en la misma carpeta con un nombre nuevo que termina con _AAAAMMDD_HHMM
    """
    # Convierte a Path (más cómodo trabajar con rutas)
    p = pathlib.Path(ruta_fichero)

    # Si la ruta no existe, lanzamos excepción
    if not p.is_file():
        raise FileNotFoundError(f"No existe el fichero: {p}")

    # Formateamos la fecha/hora actual
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M")

    # Construimos el nuevo nombre: <nombre>_<timestamp>.<ext>
    nuevo_nombre = f"{p.stem}_{ts}{p.suffix}"

    # Ruta completa del destino (mismo directorio)
    destino = p.parent / nuevo_nombre

    # Copiamos manteniendo metadatos
    shutil.copy2(p, destino)  

# --------------------------
# BUSCAR LOG DE UNA CARPETA
# --------------------------
def obtener_ultimos_logs(directorio: pathlib.Path, cantidad=10):
    """
    Devuelve una lista de pathlib.Path con los `cantidad` logs más recientes.
    Solo considera archivos con extensión .log.
    """
    logs = [f for f in directorio.glob("*.log") if f.is_file()]
    logs.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    return logs[:cantidad]

# --------------------------
# BASE DE DATOS
# --------------------------
def init_db(DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS configuracion (
            CLAVE TEXT,
            CODIGO INTEGER,
            FILTRO TEXT,
            ESTADO TEXT CHECK(ESTADO IN ('S','N')),
            GRUPO TEXT DEFAULT 'M',
            TO_EMAIL TEXT DEFAULT 'monica.jimenez@multiva.com.mx,erendira.morales@multiva.com.mx,jose.agis@multiva.com.mx,alfredo.basurto@multiva.com.mx,javiereduardo.ortega@multiva.com.mx',
            CC_EMAIL TEXT DEFAULT 'notificacionespy@tda-sgft.com,repcomun@tda-sgft.com',
            C3 TEXT
        )
    """)
    # monica.jimenez@multiva.com.mx,erendira.morales@multiva.com.mx,jose.agis@multiva.com.mx,alfredo.basurto@multiva.com.mx,javiereduardo.ortega@multiva.com.mx
    # notificacionespy@tda-sgft.com,repcomun@tda-sgft.com

    conn.commit()
    conn.close()

def get_data(DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    try:
        df = pd.read_sql_query(
            """
            SELECT *
            FROM configuracion
            WHERE CLAVE <> 'DESACTIVADO'
            ORDER BY CLAVE ASC
            """,
            conn
        )  # CLAVE <> DESACTIVADO: ese registro existe para q el grupo Patricia al menos tenga 1 registro y no error.
    except Exception:
        init_db(DB_FILE)
        df = pd.DataFrame(columns=[
            "CLAVE", "CODIGO", "FILTRO", "ESTADO", "GRUPO",
            "TO_EMAIL", "CC_EMAIL", "C3"
        ])
    conn.close()
    return df

def update_data(df, DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("DELETE FROM configuracion")
    df.to_sql("configuracion", conn, if_exists="append", index=False)
    conn.close()

def delete_record(clave, DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM configuracion WHERE CLAVE = ?", (clave,))
    conn.commit()
    conn.close()

def ejecutar_sh_con_parametros(SH_FILE, param1, param2, resultado):
    """
    Ejecuta el archivo .sh con los parámetros de DIAS y ENTORNO
    """
    import subprocess  # Solo lo usará este apartado.
    # 1. Definir el comando y los parámetros

    comando = [
        "nohup",  # Desvincula el proceso de la terminal
        SH_FILE,
        param1,
        param2
    ]
    try:
        # `preexec_fn=os.setsid` garantiza que el proceso no se cierre con la sesión
        proceso = subprocess.Popen(
            comando,
            stdout=subprocess.DEVNULL,   # Desconecta la salida estándar
            stderr=subprocess.DEVNULL,   # Desconecta la salida de error
            preexec_fn=os.setsid,        # Desvincula del TTY
            close_fds=True
        )
        print(f"✅ El script `{SH_FILE}` se está ejecutando en segundo plano (PID: {proceso.pid}).")
    except FileNotFoundError:
        resultado.error(f"❌ El archivo `{SH_FILE}` no existe. Revisa la ruta.")
    except Exception as e:
        resultado.error(f"❌ Error inesperado: {e}")


def ejecutar_proceso_sh(is_running, resultado, SH_FILE, BOLSA):
    if BOLSA == "BIVA":
        if st.session_state.parametro_c1 == "EJECUTAR":
            if is_running == "":
                ejecutar_sh_con_parametros(SH_FILE, st.session_state.parametro_a1, st.session_state.parametro_b1, resultado)
                resultado.info("Proceso 'BIVA' lanzado en segundo plano; para ver el estado de ejecución pulse el botón de '🔄 Refrescar'")
            else:
                resultado.warning("El proceso 'BIVA' se está ejecutando en segundo plano; por favor, espere o pulse el botón de '🔄 Refrescar' ")
            # Reset del campo
            st.session_state.parametro_c1 = "xxxxx"   
        else:
            resultado.warning(f"¡ La palabra de paso '{st.session_state.parametro_c1}' no es correcta !")

    if BOLSA == "BMV":
        if st.session_state.parametro_c2 == "EJECUTAR":
            if is_running == "":
                ejecutar_sh_con_parametros(SH_FILE, st.session_state.parametro_a2, st.session_state.parametro_b2, resultado)
                resultado.info("Proceso 'BMV' lanzado en segundo plano; para ver el estado de ejecución pulse el botón de '🔄 Refrescar'")
            else:
                resultado.warning("El proceso 'BMV' se está ejecutando en segundo plano; por favor, espere o pulse el botón de '🔄 Refrescar' ")
            # Reset del campo
            st.session_state.parametro_c2 = "xxxxx"   
        else:
            resultado.warning(f"¡ La palabra de paso '{st.session_state.parametro_c2}' no es correcta !")

    if BOLSA == "BOLSAS":
        if st.session_state.parametro_c3 == "EJECUTAR":
            if is_running == "":
                ejecutar_sh_con_parametros(SH_FILE, st.session_state.parametro_a3, st.session_state.parametro_b3, resultado)
                #resultado.write(f"{SH_FILE} {st.session_state.parametro_a3} {st.session_state.parametro_b3}")
                resultado.info("Email enviado; verifique su cuenta de correo 📧 Zimbra")
            else:
                resultado.warning("El proceso de envió del Email se está ejecutando en segundo plano; por favor, espere o pulse el botón de '🔄 Refrescar' ")
            # Reset del campo
            st.session_state.parametro_c3 = "xxxxx"   
        else:
            resultado.warning(f"¡ La palabra de paso '{st.session_state.parametro_c3}' no es correcta !")

def comprobar_excel_email(x):
    # Generemos una fecha según el día de procesamiento, tener en cuenta que buscaremos el día X - 1
    dias = int(x) + 1  
    hoy = datetime.datetime.now()
    fecha = hoy - timedelta(days=dias)
    fecha_final = fecha.strftime("%Y%m%d")

    ruta1 = f"/srv/apps/MisCompilados/PROY_BOLSA_MX/BIVA/INFORMES/BIVA_{fecha_final}_M.xlsx"
    ruta2 = f"/srv/apps/MisCompilados/PROY_BOLSA_MX/BMV/INFORMES/BMV_{fecha_final}_M.xlsx"

    se_manda_email = "NO"
    if os.path.isfile(ruta1) and os.path.isfile(ruta2):
        se_manda_email = "SI"

    if os.path.isfile(ruta1):
        res1 = f"✅ Existen datos en la tabla de **BIVA**"
    else:
        res1 = f"❌ No hay datos de **BIVA** para mandar el email"

    if os.path.isfile(ruta2):
        res2 = f"✅ Existen datos en la tabla de **BMV**"
    else:
        res2 = f"❌ No hay datos de **BMV** para mandar el email"

    return res1, res2, se_manda_email, ruta1, ruta2

def fecha_de_proceso_seleccionado(dias):
    # Para que me de los días de la semana en español
    locale.setlocale(locale.LC_TIME, 'es_ES.utf8')
    # Obtenemos el día de hoy 
    hoy = datetime.datetime.today()
    # Calcular fechas restando N días
    fecha1 = hoy - timedelta(days=int(dias))
    fecha2 = hoy - timedelta(days=int(dias) + 1)
    # Establezco un formato
    formato = "%A %d de %B %Y"
    # Creo las variables con el formato deseado
    VAR1 = fecha1.strftime(formato)
    VAR2 = fecha2.strftime(formato)
    return VAR1, VAR2

# -----------------------------------------------------------------------------------------------------------------------------------------
# MAIN: INTERFAZ PRINCIPAL
# -----------------------------------------------------------------------------------------------------------------------------------------
def main():
    st.title("🌐 WebScraping: Eventos Relevantes - BIVA y BMV")
    st.caption("Panel de configuración del prceso de Eventos Relavantes de las Bolsas (BIVA y BMV). (app10.py)")
    st.sidebar.subheader("🌐 : Eventos Relevantes")

    # ------------------------------------------------------------------
    # INICIO: Login
    # ------------------------------------------------------------------
    # ── 1. Definir las claves de los "widgets" 
    USER_KEY = "usuario_input"
    PASS_KEY = "contraseña_input"
    # ── 2. Botón “Cerrar Sesión” (sTv: se debe poner al principio el botón) 
    #if st.sidebar.button("❌ Cerrar Sesión"):
    #    st.session_state[USER_KEY] = ""
    #    st.session_state[PASS_KEY] = ""
    #    st.session_state.pop("usuario", None)
    #    st.session_state.pop("rol", None)
    #    st.rerun()          # opcional: si quere,os refrescar inmediatamente
    # ── 3. Widget de login usamos "text_input"
    username = st.sidebar.text_input("Usuario", key=USER_KEY)
    password = st.sidebar.text_input("Contraseña", type="password", key=PASS_KEY)
    if st.sidebar.button("🔐 Acceder"):
        if username == "admin" and password == "admin1234":
            st.session_state["usuario"] = username
            st.rerun()
        else:
            st.sidebar.error("❌ Credenciales inválidas")
    # ── 4. Validación, si le hemos dado "Cerrar Sesión" entrará aquí, hará un stop.
    if "usuario" not in st.session_state:
        st.stop()
    # ------------------------------------------------------------------
    # FIN: Login
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------------------------
    # Inicio del Programa
    # ------------------------------------------------------------------------------------------------------------------------------------
    
    # Cargamos en un DataFrame los datos de la tabla, si no existe la bbdd la crea.
    df1 = get_data(DB_FILE1)
    df2 = get_data(DB_FILE2)

    # Obtener una lista con las logs de las Bolsas
    lista_logs1_10 = obtener_ultimos_logs(LOG_DIR1, 10)
    lista_logs1_1  = obtener_ultimos_logs(LOG_DIR1, 1)
    lista_logs2_10 = obtener_ultimos_logs(LOG_DIR2, 10)
    lista_logs2_1  = obtener_ultimos_logs(LOG_DIR2, 1)

    # Ocultar columnas innecesarios del DataFrame
    for col in ["C3", "FILTRO", "TO_EMAIL", "CC_EMAIL", "GRUPO"]:
        if col in df1.columns:
            df1 = df1.drop(columns=[col])
    for col in ["C3", "FILTRO", "TO_EMAIL", "CC_EMAIL", "GRUPO"]:
        if col in df2.columns:
            df2 = df2.drop(columns=[col])

    # ------------------------------------------------------------------------------------------------------------------------------------
    # Datos
    # ------------------------------------------------------------------------------------------------------------------------------------

    # TABLA: BIVA --------------------------------------------------------------------- 

    # Bloque del titulo Biva ---------------
    is_running1 = ""
    if bool(os.popen('ps aux | grep BIVA.sh | grep -v grep').read().strip()):
        is_running1 = "ℹ️ Proceso en ejecución"
    info_archivo_ok = os.stat(lista_logs1_1[0])
    info_fecha_ok  = datetime.datetime.fromtimestamp(info_archivo_ok.st_ctime)
    info_nombre_ko  = lista_logs1_1[0].name.replace("_out.log", "_err.log")
    info_ruta_ko    = LOG_DIR1 / info_nombre_ko
    info_archivo_ko = os.stat(info_ruta_ko)
    info_fecha_ko  = datetime.datetime.fromtimestamp(info_archivo_ko.st_ctime)
    if info_archivo_ko.st_size != 0:
        var_ESTADO1  = "⚠️"
        var_FECHA1   = info_fecha_ko.strftime('%Y-%m-%d %H:%M')
        var_MENSAJE1 = f"AVISO: Posible **error** en la ejecución del día **{info_fecha_ko.strftime('%Y-%m-%d')}** ejecutado a las **{info_fecha_ko.strftime('%H:%M')}h**, revisar la Log '**{info_nombre_ko}**'"
    else:
        var_ESTADO1  = "☑️" # ☑️ ✅
        var_FECHA1   = info_fecha_ok.strftime('%Y-%m-%d %H:%M')
        var_MENSAJE1 = ""
    c1, c2, c3, c4 = st.columns([2,1,1,2])
    with c1:
        st.subheader(f"{var_ESTADO1} - BIVA ")
    with c2:
        st.caption(f" ")
        st.caption(is_running1)
    with c4:
        st.caption(f" ")
        st.caption(f"Fecha y hora de la última ejecución: {var_FECHA1}")
    
    # Mensaje de ayuda    
    st.caption(f"{var_MENSAJE1}")

    # Bloque de los Expanders ---------------
    with st.expander(f"📗 Listado de Emisores: :gray[(Número de emisores activos en BIVA: {len(df1)} -- En el radar de TDA: {(df1['ESTADO'] == "S").sum()})]", expanded=False):
        # Añadimos columna de selección
        df1["Seleccionar"] = False
        # Editor de datos interactivo
        edited_df1 = st.data_editor(
            df1,
            num_rows="dynamic",
            use_container_width=True,
            key="data_editor1",
            column_config={
                "CLAVE":    st.column_config.TextColumn("CLAVE", help="Nombre del Emisor"),
                "ESTADO":   st.column_config.SelectboxColumn("ESTADO", options=["S", "N"], help="S = Envió de Email"),
                #"GRUPO":    st.column_config.TextColumn("GRUPO", default="M", help="M = Mónica "),
                "CODIGO":   st.column_config.NumberColumn("CODIGO", help="Debe ser número entero"),
                #"TO_EMAIL": st.column_config.TextColumn("TO", default="stv.madrid@gmail.com"),
                #"CC_EMAIL": st.column_config.TextColumn("CC", default="paco@gmail.com"),
                "Seleccionar": st.column_config.CheckboxColumn("Seleccionar")
            }
        )

        col1, col3, col111, col333 = st.columns(4)
        
        # BOTÓN: Guardar cambios BIVA
        if col1.button("Guardar registro 💾 "):
            copia_seguridad_xls(f"{R_BOLSAS}BIVA/CONFIG/BIVA_Filtro_Emisores_PRO.xlsx")
            # eliminamos columna de selección antes de guardar
            if "Seleccionar" in edited_df1.columns:
                edited_df1 = edited_df1.drop(columns=["Seleccionar"])
            update_data(edited_df1, DB_FILE1)
            export_to_excel(DB_FILE1, f"{R_BOLSAS}BIVA/CONFIG/BIVA_Filtro_Emisores_PRO.xlsx", "configuracion")
            st.toast("Cambios guardados correctamente en la tabla BIVA", icon="✅")

        # BOTÓN: Borrar Registros BIVA
        if col333.button("Eliminar registro seleccionado 🗑️ "):
            # Guardamos en el estado que se ha pulsado el botón
            st.session_state["confirm_borrar1"] = True
        # Si el usuario ya pulsó el botón, mostramos la ventana de confirmación
        if st.session_state.get("confirm_borrar1", False):
            # Creamos un contenedor con dos botones
            with st.container():
                st.warning("⚠️ ¿Borrar Registro de BIVA?")
                col31, col32 = st.columns(2)
                with col31:
                    if st.button("✅ Sí, borrar", key="confirm_si1"):
                        rows_to_delete = edited_df1[edited_df1["Seleccionar"] == True]
                        for _, row in rows_to_delete.iterrows():
                            delete_record(row["CLAVE"], DB_FILE1)
                        st.success(f"✅ {len(rows_to_delete)} registro(s) eliminado(s).")
                        # Reiniciamos la flag para evitar que se repita la confirmación
                        st.session_state["confirm_borrar1"] = False
                        st.rerun()        
                with col32:
                    if st.button("❌ No, cancelar", key="confirm_no1"):
                        st.session_state["confirm_borrar1"] = False
                        st.rerun()

    with st.expander("🗂️ Logs de ejecución"):
        if not lista_logs1_10:
            st.warning("No se encontraron archivos *.log en la ruta especificada.")
        else:
            # Nombres legibles para el usuario
            nombres_logs = [f.name for f in lista_logs1_10]
            # Selección
            log_seleccionado = st.selectbox("Selecciona un log para ver su contenido:", nombres_logs)
            # Ruta completa del log elegido
            ruta_completa = LOG_DIR1 / log_seleccionado
            # Lectura y visualización
            try:
                # Si tu log está en otra codificación, cambia el encoding
                with open(ruta_completa, "r", encoding="utf-8") as f:
                    contenido = f.read()
                st.code(contenido, language="text")
            except Exception as e:
                st.error(f"Error al leer el archivo: {e}")

    with st.expander("▶️ Panel de ejecución") as panel: 
        # Contenedor donde se escribirán los resultados
        resultado1 = st.container()
        # --- Configuración del Archivo SH ---
        SH_FILE1 = "/home/robot/Python/proy_py_bolsa_mx/BIVA.sh" 
        col1, col3, col4 = st.columns(3)
        # Obtener parámetros del usuario
        with col1:
            st.selectbox(
                label="  **Día de ejecución:**",
                options=["0", "1", "2", "3", "4"],      # Valores disponibles
                index=0,                                # Valor por defecto (0 → "0")
                key="parametro_a1",                     # Identificador único
                help="Ejemplo: 0, 1, 2, 3...etc -- '0' indica el día de hoy, '1' el día de ayer, etc.. "
            )
            VAR1, VAR2 = fecha_de_proceso_seleccionado(st.session_state.parametro_a1)
            st.caption(f"Ejecución del: **{VAR1}**")
            st.caption(f"Con datos del: **{VAR2}**")
        with col3:
            st.selectbox(
                label="  **Entorno de ejecución:**",
                options=["PRO"],             # Valores disponibles
                index=0,                     # Valor por defecto (0 → "PRO")
                key="parametro_b1"           # Identificador único
            )
        with col4:
            st.text_input("**Palabra de paso:**", "-----",key="parametro_c1",help="Por seguridad escriba EJECUTAR")
        st.write(" ")
        # Botón con callback
        st.button("**Ejecutar Proceso WebScraping BIVA**", on_click=ejecutar_proceso_sh, args=(is_running1, resultado1, SH_FILE1, "BIVA"))

    st.caption(f" ")
    # TABLA: BMV ---------------------------------------------------------------------
    
    # Bloque del titulo BMV ---------------
    is_running2 = ""
    if bool(os.popen('ps aux | grep BMV.sh | grep -v grep').read().strip()):
        is_running2 = "ℹ️ Proceso en ejecución"
    info_archivo_ok = os.stat(lista_logs2_1[0])
    info_fecha_ok  = datetime.datetime.fromtimestamp(info_archivo_ok.st_ctime)
    info_nombre_ko  = lista_logs2_1[0].name.replace("_out.log", "_err.log")
    info_ruta_ko    = LOG_DIR2 / info_nombre_ko
    info_archivo_ko = os.stat(info_ruta_ko)
    info_fecha_ko  = datetime.datetime.fromtimestamp(info_archivo_ko.st_ctime)
    if info_archivo_ko.st_size != 0:
        var_ESTADO2  = "⚠️"
        var_FECHA2  = info_fecha_ko.strftime('%Y-%m-%d %H:%M')
        var_MENSAJE2 = f"AVISO: Posible **error** en la ejecución del día **{info_fecha_ko.strftime('%Y-%m-%d')}** ejecutado a las **{info_fecha_ko.strftime('%H:%M')}h**, revisar la Log '**{info_nombre_ko}**'"
    else:
        var_ESTADO2  = "☑️" # ☑️ ✅
        var_FECHA2   = info_fecha_ok.strftime('%Y-%m-%d %H:%M')
        var_MENSAJE2 = ""
    c1, c2, c3, c4 = st.columns([2,1,1,2])
    with c1:
        st.subheader(f"{var_ESTADO2} - BMV ")
    with c2:
        st.caption(f" ")
        st.caption(is_running2)
    with c4:
        st.caption(f" ")
        st.caption(f"Fecha y hora de la última ejecución: {var_FECHA2}")
    
    # Mensaje de ayuda    
    st.caption(f"{var_MENSAJE2}")

    # Bloque de los Expanders ---------------
    with st.expander(f"📗 Listado de Emisores: :gray[(Número de emisores activos en BMV: {len(df2)} -- En el radar de TDA: {(df2['ESTADO'] == "S").sum()})]", expanded=False):
        # Añadimos columna de selección
        df2["Seleccionar"] = False
        # Editor de datos interactivo
        edited_df2 = st.data_editor(
            df2,
            num_rows="dynamic",
            use_container_width=True,
            key="data_editor2",
            column_config={
                "CLAVE":    st.column_config.TextColumn("CLAVE", help="Nombre del Emisor"),
                "ESTADO":   st.column_config.SelectboxColumn("ESTADO", options=["S", "N"], help="S = Envió de Email"),
                #"GRUPO":    st.column_config.TextColumn("GRUPO", default="M", help="M = Mónica "),
                "CODIGO":   st.column_config.NumberColumn("CODIGO", help="Debe ser número entero"),
                #"TO_EMAIL": st.column_config.TextColumn("TO", default="stv.madrid@gmail.com"),
                #"CC_EMAIL": st.column_config.TextColumn("CC", default="paco@gmail.com"),
                "Seleccionar": st.column_config.CheckboxColumn("Seleccionar")
            }
        )
 
        col2, col4, col222, col444 = st.columns(4)

        # BOTÓN: Guardar cambios BMV
        if col2.button(" Guardar registro 💾 "):
            copia_seguridad_xls(f"{R_BOLSAS}BMV/CONFIG/BMV_Filtro_Emisores_PRO.xlsx")
            # eliminamos columna de selección antes de guardar
            if "Seleccionar" in edited_df2.columns:
                edited_df2 = edited_df2.drop(columns=["Seleccionar"])
            update_data(edited_df2, DB_FILE2)
            export_to_excel(DB_FILE2, f"{R_BOLSAS}BMV/CONFIG/BMV_Filtro_Emisores_PRO.xlsx", "configuracion")
            st.toast("Cambios guardados correctamente en la tabla BMV", icon="✅")

        # BOTÓN: Borrar Registros BMV
        if col444.button(" Eliminar registro seleccionado 🗑️ "):
            # Guardamos en el estado que se ha pulsado el botón
            st.session_state["confirm_borrar2"] = True
        # Si el usuario ya pulsó el botón, mostramos la ventana de confirmación
        if st.session_state.get("confirm_borrar2", False):
            # Creamos un contenedor con dos botones
            with st.container():
                st.warning("⚠️ ¿Borrar Registro de BMV?")
                col41, col42 = st.columns(2)
                with col41:
                    if st.button("✅ Sí, borrar", key="confirm_si2"):
                        rows_to_delete = edited_df2[edited_df2["Seleccionar"] == True]
                        for _, row in rows_to_delete.iterrows():
                            delete_record(row["CLAVE"], DB_FILE2)
                        st.success(f"✅ {len(rows_to_delete)} registro(s) eliminado(s).")
                        # Reiniciamos la flag para evitar que se repita la confirmación
                        st.session_state["confirm_borrar2"] = False
                        st.rerun()      
                with col42:
                    if st.button("❌ No, cancelar", key="confirm_no2"):
                        st.session_state["confirm_borrar2"] = False
                        st.rerun()

    with st.expander("🗂️ Logs de ejecución"):
        if not lista_logs2_10:
            st.warning("No se encontraron archivos *.log en la ruta especificada.")
        else:
            # Nombres legibles para el usuario
            nombres_logs = [f.name for f in lista_logs2_10]
            # Selección
            log_seleccionado = st.selectbox("Selecciona un log para ver su contenido:", nombres_logs)

            # Ruta completa del log elegido
            ruta_completa = LOG_DIR2 / log_seleccionado

            # Lectura y visualización
            try:
                # Si tu log está en otra codificación, cambia el encoding
                with open(ruta_completa, "r", encoding="utf-8") as f:
                    contenido = f.read()
                st.code(contenido, language="text")
            except Exception as e:
                st.error(f"Error al leer el archivo: {e}")

    with st.expander("▶️ Panel de ejecución") as panel: 
        # Contenedor donde se escribirán los resultados
        resultado2 = st.container()
        # --- Configuración del Archivo SH ---
        SH_FILE2 = "/home/robot/Python/proy_py_bolsa_mx/BMV.sh" 
        col1, col3, col4 = st.columns(3)
        # Obtener parámetros del usuario
        with col1:
            st.selectbox(
                label="  **Día de ejecución:**",
                options=["0", "1", "2", "3", "4"],      # Valores disponibles
                index=0,                                # Valor por defecto (0 → "0")
                key="parametro_a2",                     # Identificador único
                help="Ejemplo: 0, 1, 2, 3...etc -- '0' indica el día de hoy, '1' el día de ayer, etc.. "
            )
            VAR1, VAR2 = fecha_de_proceso_seleccionado(st.session_state.parametro_a2)
            st.caption(f"Ejecución del: **{VAR1}**")
            st.caption(f"Con datos del: **{VAR2}**")
        with col3:
            st.selectbox(
                label="  **Entorno de ejecución:**",
                options=["PRO"],             # Valores disponibles
                index=0,                     # Valor por defecto (0 → "PRO")
                key="parametro_b2"           # Identificador único
            )
        with col4:
            st.text_input(" **Palabra de paso:**", "-----",key="parametro_c2",help="Por seguridad escriba EJECUTAR")
        st.write(" ")
        # Botón con callback
        st.button("**Ejecutar Proceso WebScraping BMV**", on_click=ejecutar_proceso_sh, args=(is_running2, resultado2, SH_FILE2, "BMV"))

    st.caption(f" ")

    # TABLA: ENVIO DE EMAIL ---------------------------------------------------------------------
    st.subheader("📧 - Envió de Email")

    is_running3 = ""
    if bool(os.popen('ps aux | grep BOLSAS.sh | grep -v grep').read().strip()):
        is_running3 = "ℹ️ Proceso en ejecución"

    with st.expander("▶️ Panel de envió") as panel: 
        # Contenedor donde se escribirán los resultados
        resultado3 = st.container()
        # --- Configuración del Archivo SH ---
        SH_FILE3 = "/home/robot/Python/proy_py_bolsa_mx/BOLSAS.sh" 
        col1, col3, col4 = st.columns(3)
        # Obtener parámetros del usuario
        with col1:
            st.selectbox(
                label="  **Día de ejecución:**",
                options=["0", "1", "2", "3", "4"],      # Valores disponibles
                index=0,                                # Valor por defecto (0 → "0")
                key="parametro_a3",                     # Identificador único
                help="Ejemplo: 0, 1, 2, 3...etc -- '0' indica el día de hoy, '1' el día de ayer, etc.. "
            )
            VAR1, VAR2 = fecha_de_proceso_seleccionado(st.session_state.parametro_a3)
            st.caption(f"Ejecución del: **{VAR1}**")
            st.caption(f"Con datos del: **{VAR2}**")
        with col3:
            st.selectbox(
                label="  **Entorno de ejecución:**",
                options=["DEV", "PRO"],      # Valores disponibles
                index=0,                     # Valor por defecto (0 → "DEV")
                key="parametro_b3"           # Identificador único
            )
        with col4:
            st.text_input("  **Palabra de paso:**", "-----",key="parametro_c3",help="Por seguridad escriba EJECUTAR")


        # Valida si existe el excel con ese día de procesarmiento.
        res_excel1, res_excel2, se_manda_email, ruta1, ruta2 = comprobar_excel_email(st.session_state.parametro_a3)

        st.write(" ")

        # Botón con callback
        if se_manda_email == "SI":
            col_email1, col_email2 = st.columns(2)
            with col_email1:
                df_excel1 = pd.read_excel(ruta1)
                df_excel1.index = df_excel1.index + 1
                st.write(f"{res_excel1}: ({len(df_excel1)} registros)")
                columna_excel1 = ['FECHA', 'CLAVE', 'ASUNTO']
                st.dataframe(df_excel1[columna_excel1])

            with col_email2:
                df_excel2 = pd.read_excel(ruta2)
                df_excel2.index = df_excel2.index + 1
                st.write(f"{res_excel2}: ({len(df_excel2)} registros)")
                columna_excel2 = ['FECHA', 'CLAVE', 'ASUNTO']
                st.dataframe(df_excel2[columna_excel2])
            # Botón: Envio de email
            st.button("**Enviar Email con los Eventos Relevantes**", on_click=ejecutar_proceso_sh, args=(is_running3, resultado3, SH_FILE3, "BOLSAS"))
        else:
            st.write("No se puede mandar el email, es necesario que BIVA y BMV tengan datos.")



    st.caption(f" ")

    # TABLA: ORACLE ---------------------------------------------------------------------
    st.subheader("🗄️ - Almacenar en Histórico ORACLE")







    # PIE DE PAGINA DEL SIDEBAR -----------------------------------------------------------------
    st.sidebar.caption("---")
    # Botón refrescar
    if st.sidebar.button("🔄 Refrescar"):
        st.rerun()
    # Aviso informativo
    st.sidebar.caption(
    """
    <div style="font-size:1rem;"><br><br><b>Importante:</b><br>
    La ejecución del proceso WebScraping debe estar justificado.<br>
    - Antes de ejecutarlo, verifica el <b>'día de procesamiento'</b>.<br>
    - Verificar que los servidores de: 
        <a href="https://www.biva.mx/empresas/emisoras_inscritas/emisoras_inscritas" target="_blank" style="color:#1f77b4;">BIVA</a> y 
        <a href="https://www.bmv.com.mx/es/emisoras/informacion-de-emisoras" target="_blank" style="color:#1f77b4;">BMV</a> estén UP.<br>
    - Intentar no ejecutarlo en horario de planificación 8-10h para evitar solapamientos.
    </div>
    """,
    unsafe_allow_html=True)


if __name__ == "__main__":

    main()

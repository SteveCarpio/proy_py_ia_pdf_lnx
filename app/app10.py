import streamlit as st
import sqlite3
import pandas as pd
import pathlib
import datetime
import os

# --------------------------
# CONFIGURACIÓN GENERAL
# --------------------------
os.makedirs("data", exist_ok=True)  
DB_FILE1 = "data/app10_config_BIVA.db"
DB_FILE2 = "data/app10_config_BMV.db"
LOG_DIR1 = pathlib.Path("/srv/apps/MisCompilados/PROY_BOLSA_MX/BIVA/LOG")
LOG_DIR2 = pathlib.Path("/srv/apps/MisCompilados/PROY_BOLSA_MX/BMV/LOG")

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
            GRUPO TEXT,
            TO_EMAIL TEXT DEFAULT 'stv.madrid@gmail.com',
            CC_EMAIL TEXT DEFAULT 'paco@gmail.com',
            C3 TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_data(DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    try:
        df = pd.read_sql_query("SELECT * FROM configuracion ORDER BY CLAVE ASC", conn)
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

# --------------------------
# INTERFAZ PRINCIPAL
# --------------------------
def main():
    st.title("🌐 WebScraping: Eventos Relevantes")
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
    for col in ["C3", "FILTRO"]:
        if col in df1.columns:
            df1 = df1.drop(columns=[col])
    for col in ["C3", "FILTRO"]:
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
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.subheader(f"{var_ESTADO1} - BIVA ")
    with c2:
        st.subheader(is_running1)
    with c4:
        st.subheader(f"{var_FECHA1} ")
    
    # Mensaje de ayuda    
    st.caption(f"{var_MENSAJE1}")

    # Bloque de los Expanders ---------------
    with st.expander(f"📗 Listado de Emisores: (Número de Emisores: {len(df1)} - Activos: {(df1['ESTADO'] == "S").sum()})", expanded=False):
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
                "GRUPO":    st.column_config.TextColumn("GRUPO", default="M", help="M = Mónica "),
                "CODIGO":   st.column_config.NumberColumn("CODIGO", help="Debe ser número entero"),
                "TO_EMAIL": st.column_config.TextColumn("TO", default="stv.madrid@gmail.com"),
                "CC_EMAIL": st.column_config.TextColumn("CC", default="paco@gmail.com"),
                "Seleccionar": st.column_config.CheckboxColumn("Seleccionar")
            }
        )
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
    with st.expander("📊 Distribución Global"):
        st.write("🚧 En construcción 🚧")

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
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.subheader(f"{var_ESTADO2} - BMV ")
    with c2:
        st.subheader(is_running2)
    with c4:
        st.subheader(f"{var_FECHA2} ")
    
    # Mensaje de ayuda    
    st.caption(f"{var_MENSAJE2}")

    # Bloque de los Expanders ---------------
    with st.expander(f"📗 Listado de Emisores: (Número de Emisores: {len(df2)} - Activos: {(df1['ESTADO'] == "S").sum()})", expanded=False):
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
                "GRUPO":    st.column_config.TextColumn("GRUPO", default="M", help="M = Mónica "),
                "CODIGO":   st.column_config.NumberColumn("CODIGO", help="Debe ser número entero"),
                "TO_EMAIL": st.column_config.TextColumn("TO", default="stv.madrid@gmail.com"),
                "CC_EMAIL": st.column_config.TextColumn("CC", default="paco@gmail.com"),
                "Seleccionar": st.column_config.CheckboxColumn("Seleccionar")
            }
        )
 
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

    with st.expander("📊 Distribución Global"):
        st.write("🚧 En construcción 🚧")

    st.sidebar.caption("---")

    # ------------------------------------------------------------------------------------------------------------------------------------
    # SECCION BOTONES GUARDAR Y ELIMINAR
    # ------------------------------------------------------------------------------------------------------------------------------------

    # Sección GUARDAR REGISTROS -------------------------------------------------------------
    st.sidebar.write("**BIVA:** Guardar o Eliminar Registros")
    col1, col3, col111, col333 = st.sidebar.columns(4)
    
    # 1️⃣ BOTÓN: Guardar cambios BIVA
    if col1.button("💾 "):
        # eliminamos columna de selección antes de guardar
        if "Seleccionar" in edited_df1.columns:
            edited_df1 = edited_df1.drop(columns=["Seleccionar"])
        update_data(edited_df1, DB_FILE1)
        st.toast("Cambios guardados correctamente en la tabla BIVA", icon="✅")

    # 3️⃣ BOTÓN: Borrar Registros BIVA
    if col3.button("🗑️ "):
        # Guardamos en el estado que se ha pulsado el botón
        st.session_state["confirm_borrar1"] = True
    # Si el usuario ya pulsó el botón, mostramos la ventana de confirmación
    if st.session_state.get("confirm_borrar1", False):
        # Creamos un contenedor con dos botones
        with st.sidebar.container():
            st.warning("⚠️ ¿Borrar Registro de BIVA?")
            col31, col32 = st.columns(2)
            with col31:
                if st.button("✅ Sí, borrar", key="confirm_si1"):
                    rows_to_delete = edited_df1[edited_df1["Seleccionar"] == True]
                    for _, row in rows_to_delete.iterrows():
                        delete_record(row["CLAVE"], DB_FILE1)
                    st.sidebar.success(f"✅ {len(rows_to_delete)} registro(s) eliminado(s).")
                    # Reiniciamos la flag para evitar que se repita la confirmación
                    st.session_state["confirm_borrar1"] = False
                    st.rerun()        
            with col32:
                if st.button("❌ No, cancelar", key="confirm_no1"):
                    st.session_state["confirm_borrar1"] = False
                    st.rerun()

    # Sección BORRAR REGISTROS -------------------------------------------------------------
    st.sidebar.write("**BMV:** Guardar o Eliminar Registros")
    col2, col4, col222, col444 = st.sidebar.columns(4)

    # 2️⃣ BOTÓN: Guardar cambios BMV
    if col2.button(" 💾 "):
        # eliminamos columna de selección antes de guardar
        if "Seleccionar" in edited_df2.columns:
            edited_df2 = edited_df2.drop(columns=["Seleccionar"])
        update_data(edited_df2, DB_FILE2)
        st.toast("Cambios guardados correctamente en la tabla BMV", icon="✅")

    # 4️⃣ BOTÓN: Borrar Registros BMV
    if col4.button(" 🗑️ "):
        # Guardamos en el estado que se ha pulsado el botón
        st.session_state["confirm_borrar2"] = True
    # Si el usuario ya pulsó el botón, mostramos la ventana de confirmación
    if st.session_state.get("confirm_borrar2", False):
        # Creamos un contenedor con dos botones
        with st.sidebar.container():
            st.warning("⚠️ ¿Borrar Registro de BMV?")
            col41, col42 = st.columns(2)
            with col41:
                if st.button("✅ Sí, borrar", key="confirm_si2"):
                    rows_to_delete = edited_df2[edited_df2["Seleccionar"] == True]
                    for _, row in rows_to_delete.iterrows():
                        delete_record(row["CLAVE"], DB_FILE2)
                    st.sidebar.success(f"✅ {len(rows_to_delete)} registro(s) eliminado(s).")
                    # Reiniciamos la flag para evitar que se repita la confirmación
                    st.session_state["confirm_borrar2"] = False
                    st.rerun()      
            with col42:
                if st.button("❌ No, cancelar", key="confirm_no2"):
                    st.session_state["confirm_borrar2"] = False
                    st.rerun()

    st.sidebar.caption("---")
    if st.sidebar.button("🔄 Refrescar"):
        st.rerun()


if __name__ == "__main__":

    main()

import streamlit as st
import sqlite3
import pandas as pd
import os

# --------------------------
# CONFIGURACIÓN GENERAL
# --------------------------
os.makedirs("data", exist_ok=True)  
DB_FILE1 = "data/app10_config_BIVA.db"
DB_FILE2 = "data/app10_config_BMV.db"

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
    st.sidebar.subheader("🔐 Control de Acceso")

    # ------------------------------------------------------------------
    # INICIO: Login
    # ------------------------------------------------------------------
    # ── 1. Definir las claves de los "widgets" 
    USER_KEY = "usuario_input"
    PASS_KEY = "contraseña_input"
    # ── 2. Botón “Cerrar Sesión” (sTv: se debe poner al principio el botón) 
    if st.sidebar.button("❌ Cerrar Sesión"):
        st.session_state[USER_KEY] = ""
        st.session_state[PASS_KEY] = ""
        st.session_state.pop("usuario", None)
        st.session_state.pop("rol", None)
        st.rerun()          # opcional: si quere,os refrescar inmediatamente
    # ── 3. Widget de login usamos "text_input"
    username = st.sidebar.text_input("Usuario", key=USER_KEY)
    password = st.sidebar.text_input("Contraseña", type="password", key=PASS_KEY)
    if st.sidebar.button("🌐 Acceder"):
        if username == "admin" and password == "admin1234":
            st.session_state["usuario"] = "admin"
            st.session_state["rol"]     = "admin1234"
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

    # Ocultar columnas innecesarios del DataFrame
    for col in ["C3", "FILTRO"]:
        if col in df1.columns:
            df1 = df1.drop(columns=[col])
    for col in ["C3", "FILTRO"]:
        if col in df2.columns:
            df2 = df2.drop(columns=[col])

    # TABLA: BIVA ---------------------------------------------------------------------
    with st.expander("🗂️ Emisores Activos de: BIVA", expanded=False):
        # Añadimos columna de selección
        df1["Seleccionar"] = False
        # Editor de datos interactivo
        edited_df1 = st.data_editor(
            df1,
            num_rows="dynamic",
            use_container_width=True,
            key="data_editor1",
            column_config={
                "CLAVE":    st.column_config.TextColumn("CLAVE_", help="Nombre del Emisor"),
                "ESTADO":   st.column_config.SelectboxColumn("ESTADO", options=["S", "N"], help="S = Envió de Email"),
                "GRUPO":    st.column_config.TextColumn("GRUPO", default="M", help="M = Mónica "),
                "CODIGO":   st.column_config.NumberColumn("CODIGO", help="Debe ser número entero"),
                "TO_EMAIL": st.column_config.TextColumn("TO", default="stv.madrid@gmail.com"),
                "CC_EMAIL": st.column_config.TextColumn("CC", default="paco@gmail.com"),
                "Seleccionar": st.column_config.CheckboxColumn("Seleccionar")
            }
        )

    # TABLA: BMV ---------------------------------------------------------------------
    with st.expander("🗂️ Emisores Activos de: BMV", expanded=False):
        # Añadimos columna de selección
        df2["Seleccionar"] = False
        # Editor de datos interactivo
        edited_df2 = st.data_editor(
            df2,
            num_rows="dynamic",
            use_container_width=True,
            key="data_editor2",
            column_config={
                "CLAVE":    st.column_config.TextColumn("CLAVE_", help="Nombre del Emisor"),
                "ESTADO":   st.column_config.SelectboxColumn("ESTADO", options=["S", "N"], help="S = Envió de Email"),
                "GRUPO":    st.column_config.TextColumn("GRUPO", default="M", help="M = Mónica "),
                "CODIGO":   st.column_config.NumberColumn("CODIGO", help="Debe ser número entero"),
                "TO_EMAIL": st.column_config.TextColumn("TO", default="stv.madrid@gmail.com"),
                "CC_EMAIL": st.column_config.TextColumn("CC", default="paco@gmail.com"),
                "Seleccionar": st.column_config.CheckboxColumn("Seleccionar")
            }
        )
 
    # ---------------------------------------------------------------------------------------
    # SECCION BOTONES GUARDAR Y ELIMINAR
    # ---------------------------------------------------------------------------------------
    st.sidebar.caption("---")

    # Sección GUARDAR REGISTROS -------------------------------------------------------------
    st.sidebar.caption("Guardar Datos BIVA/BMV")
    col1, col2 = st.sidebar.columns(2)
    
    # 1️⃣ BOTÓN: Guardar cambios BIVA
    if col1.button("💾 BIVA"):
        # eliminamos columna de selección antes de guardar
        if "Seleccionar" in edited_df1.columns:
            edited_df1 = edited_df1.drop(columns=["Seleccionar"])
        update_data(edited_df1, DB_FILE1)
        st.success("✅ Cambios guardados correctamente en la tabla BIVA")

    # 2️⃣ BOTÓN: Guardar cambios BMV
    if col2.button("💾 BMV"):
        # eliminamos columna de selección antes de guardar
        if "Seleccionar" in edited_df2.columns:
            edited_df2 = edited_df2.drop(columns=["Seleccionar"])
        update_data(edited_df2, DB_FILE2)
        st.success("✅ Cambios guardados correctamente en la tabla BMV")

    # Sección BORRAR REGISTROS -------------------------------------------------------------
    st.sidebar.caption("Eliminar Registros BIVA/BMV")
    col3, col4 = st.sidebar.columns(2)

    # 3️⃣ BOTÓN: Borrar Registros BIVA
    if col3.button("🗑️ BIVA"):
        # Guardamos en el estado que se ha pulsado el botón
        st.session_state["confirm_borrar1"] = True
    # Si el usuario ya pulsó el botón, mostramos la ventana de confirmación
    if st.session_state.get("confirm_borrar1", False):
        # Creamos un contenedor con dos botones
        with st.container():
            st.warning("⚠️ ¿Estás seguro de borrar los registros seleccionados de la tabla BIVA?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Sí, borrar", key="confirm_si1"):
                    rows_to_delete = edited_df1[edited_df1["Seleccionar"] == True]
                    for _, row in rows_to_delete.iterrows():
                        delete_record(row["CLAVE"], DB_FILE1)
                    st.sidebar.success(f"✅ {len(rows_to_delete)} registro(s) eliminado(s).")
                    # Reiniciamos la flag para evitar que se repita la confirmación
                    st.session_state["confirm_borrar1"] = False
                    st.rerun()        
            with col2:
                if st.button("❌ No, cancelar", key="confirm_no1"):
                    st.session_state["confirm_borrar1"] = False
                    st.sidebar.info("✅ Operación cancelada.")

    # 4️⃣ BOTÓN: Borrar Registros BMV
    if col4.button("🗑️ BMV"):
        # Guardamos en el estado que se ha pulsado el botón
        st.session_state["confirm_borrar2"] = True
    # Si el usuario ya pulsó el botón, mostramos la ventana de confirmación
    if st.session_state.get("confirm_borrar2", False):
        # Creamos un contenedor con dos botones
        with st.container():
            st.warning("⚠️ ¿Estás seguro de borrar los registros seleccionados de la tabla BMV?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Sí, borrar", key="confirm_si2"):
                    rows_to_delete = edited_df2[edited_df2["Seleccionar"] == True]
                    for _, row in rows_to_delete.iterrows():
                        delete_record(row["CLAVE"], DB_FILE2)
                    st.sidebar.success(f"✅ {len(rows_to_delete)} registro(s) eliminado(s).")
                    # Reiniciamos la flag para evitar que se repita la confirmación
                    st.session_state["confirm_borrar2"] = False
                    st.rerun()      
            with col2:
                if st.button("❌ No, cancelar", key="confirm_no2"):
                    st.session_state["confirm_borrar2"] = False
                    st.sidebar.info("✅ Operación cancelada.")
if __name__ == "__main__":

    main()

import streamlit as st
import sqlite3
import pandas as pd
import os

# --------------------------
# CONFIGURACIÓN GENERAL
# --------------------------
os.makedirs("data", exist_ok=True)  
DB_FILE = "data/configuracion_BIVA.db"

# --------------------------
# BASE DE DATOS
# --------------------------
def init_db():
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

def get_data():
    conn = sqlite3.connect(DB_FILE)
    try:
        df = pd.read_sql_query("SELECT * FROM configuracion ORDER BY CLAVE ASC", conn)
    except Exception:
        init_db()
        df = pd.DataFrame(columns=[
            "CLAVE", "CODIGO", "FILTRO", "ESTADO", "GRUPO",
            "TO_EMAIL", "CC_EMAIL", "C3"
        ])
    conn.close()
    return df

def update_data(df):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("DELETE FROM configuracion")
    df.to_sql("configuracion", conn, if_exists="append", index=False)
    conn.close()

def delete_record(clave):
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
    df = get_data()

    # Ocultar columnas innecesarios del DataFrame
    for col in ["C3", "FILTRO"]:
        if col in df.columns:
            df = df.drop(columns=[col])

    # Titulo para el apartado de BIVA
    st.subheader("Emisores Activos de: BIVA")

    # Añadimos columna de selección
    df["Seleccionar"] = False

    # Editor de datos interactivo
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        key="data_editor",
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

    # BOTÓN: Guardar cambios
    #st.sidebar.info("ℹ️ Después de cualquier cambio muy importante darle al botón Guardar Cambios")
    if st.sidebar.button("💾 Guardar cambios"):
        # eliminamos columna de selección antes de guardar
        if "Seleccionar" in edited_df.columns:
            edited_df = edited_df.drop(columns=["Seleccionar"])
        update_data(edited_df)
        st.success("✅ Cambios guardados correctamente")

    # BOTÓN: Borrar Registros seleccionados
    #st.sidebar.warning("⚠️ Puede seleccione uno o varios registros para eliminarlo, 🚨 cuidado esta acción será permanente.")
    if st.sidebar.button("🗑️ Eliminar registro"):
        rows_to_delete = edited_df[edited_df["Seleccionar"] == True]
        for _, row in rows_to_delete.iterrows():
            delete_record(row["CLAVE"])
        st.success(f"✅ {len(rows_to_delete)} registro(s) eliminado(s).")
        st.rerun() 


if __name__ == "__main__":

    main()

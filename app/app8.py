import streamlit as st
from datetime import datetime
from app import db
import pandas as pd
from io import BytesIO

# Constantes
ESTADOS = ["En ejecución", "Terminado", "Bloqueado", "En revisión", "Pendiente"]
PRIORIDADES = ["Alta", "Media", "Baja"]

def main():
    st.title("📁 Gestor de Proyectos")
  
    st.caption("...")
    st.sidebar.title("🔐 Acceso")
    password = st.sidebar.text_input("Contraseña", type="password")

    if password != "admin123":
        st.sidebar.warning("Introduce la contraseña correcta para continuar.")
        st.stop()

    db.crear_tabla()

    agrupamiento = st.sidebar.radio("Agrupar por:", ["Prioridad", "Estado"], horizontal=True)


    # Exportar a Excel con filtros
    st.sidebar.title("📤 Exportar proyectos")
    filtro_estado = st.sidebar.selectbox("Filtrar por estado", ["Todos"] + ESTADOS)
    filtro_prioridad = st.sidebar.selectbox("Filtrar por prioridad", ["Todos"] + PRIORIDADES)

    if st.sidebar.button("Exportar a Excel"):
        proyectos = db.obtener_proyectos()
        data = []
        for row in proyectos:
            proyecto = {
                "ID": row[0],
                "Nombre": row[1],
                "Descripción": row[2],
                "Responsable": row[3],
                "Estado": row[4],
                "Prioridad": row[5],
                "Inicio": row[6],
                "Fin": row[7],
            }
            if (filtro_estado == "Todos" or proyecto["Estado"] == filtro_estado) and \
               (filtro_prioridad == "Todos" or proyecto["Prioridad"] == filtro_prioridad):
                data.append(proyecto)

        df = pd.DataFrame(data)
        if df.empty:
            st.sidebar.warning("No hay datos que exportar con los filtros seleccionados.")
        else:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name="Proyectos")
            output.seek(0)

            st.sidebar.download_button(
                label="📥 Descargar Excel",
                data=output,
                file_name="proyectos_filtrados.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    #agrupamiento = st.sidebar.radio("Agrupar por:", ["Prioridad", "Estado"], horizontal=True)

    proyectos_raw = db.obtener_proyectos()
    proyectos = []
    for row in proyectos_raw:
        proyectos.append({
            "id": row[0],
            "nombre": row[1],
            "descripcion": row[2],
            "responsable": row[3],
            "estado": row[4],
            "prioridad": row[5],
            "fecha_inicio": row[6],
            "fecha_fin": row[7]
        })

    claves = PRIORIDADES if agrupamiento == "Prioridad" else ESTADOS
    clave_field = "prioridad" if agrupamiento == "Prioridad" else "estado"

    for grupo in claves:
        grupo_proyectos = [p for p in proyectos if p[clave_field] == grupo]
        if not grupo_proyectos:
            continue
        st.subheader(f"📂 {grupo}")
        for proyecto in grupo_proyectos:
            with st.expander(f"🔹 {proyecto['nombre']} ({proyecto['estado']} - {proyecto['prioridad']})"):
                st.markdown(f"**Descripción:** {proyecto['descripcion']}")
                st.markdown(f"**Responsable:** {proyecto['responsable']}")
                st.markdown(f"**Fechas:** {proyecto['fecha_inicio']} → {proyecto['fecha_fin']}")

                # Actualizar estado
                nuevo_estado = st.selectbox(
                    "Actualizar estado",
                    ESTADOS,
                    index=ESTADOS.index(proyecto["estado"]),
                    key=f"estado_{proyecto['id']}"
                )
                if nuevo_estado != proyecto["estado"]:
                    db.actualizar_estado(proyecto["id"], nuevo_estado)
                    st.success("✅ Estado actualizado")
                    st.rerun()

                # Comentarios
                st.markdown("**Comentarios:**")
                comentarios = db.obtener_comentarios(proyecto["id"])
                for autor, texto, fecha in comentarios:
                    st.markdown(f"- {fecha} [{autor}]: {texto}")

                with st.form(f"form_comentario_{proyecto['id']}"):
                    autor = st.text_input("Tu nombre", key=f"autor_{proyecto['id']}")
                    texto = st.text_area("Comentario", key=f"texto_{proyecto['id']}")
                    enviar = st.form_submit_button("Añadir comentario")
                    if enviar and autor and texto:
                        db.agregar_comentario(proyecto["id"], autor, texto, datetime.now().strftime("%Y-%m-%d"))
                        st.success("💬 Comentario guardado")
                        st.rerun()

                # Confirmación de eliminación
                if f"confirm_delete_{proyecto['id']}" not in st.session_state:
                    st.session_state[f"confirm_delete_{proyecto['id']}"] = False

                if not st.session_state[f"confirm_delete_{proyecto['id']}"]:
                    if st.button("🗑️ Eliminar proyecto", key=f"delbtn_{proyecto['id']}"):
                        st.session_state[f"confirm_delete_{proyecto['id']}"] = True
                else:
                    st.warning("¿Estás seguro de eliminar este proyecto?")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Sí, eliminar", key=f"confirm_yes_{proyecto['id']}"):
                            db.eliminar_proyecto(proyecto["id"])
                            st.success("✅ Proyecto eliminado.")
                            st.rerun()
                    with col2:
                        if st.button("❌ Cancelar", key=f"cancel_del_{proyecto['id']}"):
                            st.session_state[f"confirm_delete_{proyecto['id']}"] = False

    # Expander para nuevo proyecto
    with st.expander("➕ Añadir nuevo proyecto"):
        with st.form("nuevo_proyecto_form"):
            nombre = st.text_input("Nombre del proyecto")
            descripcion = st.text_area("Descripción")
            responsable = st.text_input("Responsable")
            estado = st.selectbox("Estado", ESTADOS)
            prioridad = st.selectbox("Prioridad", PRIORIDADES)
            fecha_inicio = st.date_input("Fecha de inicio")
            fecha_fin = st.date_input("Fecha de fin")
            guardar = st.form_submit_button("Guardar proyecto")

            if guardar:
                if not nombre or not descripcion or not responsable:
                    st.error("❌ Debes completar todos los campos obligatorios: nombre, descripción y responsable.")
                else:
                    db.agregar_proyecto(
                        nombre, descripcion, responsable, estado, prioridad,
                        fecha_inicio.strftime("%Y-%m-%d"),
                        fecha_fin.strftime("%Y-%m-%d")
                    )
                    st.success("✅ Proyecto guardado")
                    st.rerun()



if __name__ == "__main__":
    main()
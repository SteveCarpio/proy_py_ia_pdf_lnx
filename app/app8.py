import streamlit as st
from datetime import datetime
from app import db
import pandas as pd
from io import BytesIO

ESTADOS = ["En ejecución", "Terminado", "Bloqueado", "En revisión", "Pendiente"]
PRIORIDADES = ["Alta", "Media", "Baja"]

def main():
    db.crear_tablas()
    st.set_page_config(page_title="Gestor de Proyectos", layout="wide")
    st.sidebar.title("🔐 Iniciar sesión")

    username = st.sidebar.text_input("Usuario")
    password = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Acceder"):
        rol = db.validar_usuario(username, password)
        if rol:
            st.session_state["usuario"] = username
            st.session_state["rol"] = rol
            st.rerun()
        else:
            st.sidebar.error("❌ Credenciales inválidas")

    if "usuario" not in st.session_state:
        st.stop()

    usuario = st.session_state["usuario"]
    rol = st.session_state["rol"]
    st.sidebar.markdown(f"👤 Usuario: `{usuario}` | Rol: `{rol}`")

    # ===============================
    # 📤 Exportar proyectos a Excel
    # ===============================
    st.sidebar.title("📤 Exportar proyectos")
    filtro_estado = st.sidebar.selectbox("Filtrar por estado", ["Todos"] + ESTADOS)
    filtro_prioridad = st.sidebar.selectbox("Filtrar por prioridad", ["Todos"] + PRIORIDADES)

    filtro_usuario = None
    usuarios_disponibles = []
    if rol == "admin":
        usuarios_disponibles = db.obtener_usuarios()
        filtro_usuario = st.sidebar.selectbox("Filtrar por usuario", ["Todos"] + usuarios_disponibles)

    if st.sidebar.button("Exportar a Excel"):
        proyectos_raw = db.obtener_proyectos(
            usuario if filtro_usuario in [None, "Todos"] else filtro_usuario,
            rol if filtro_usuario in [None, "Todos"] else "user"
        )
        comentarios = db.obtener_todos_comentarios(
            usuario if filtro_usuario in [None, "Todos"] else filtro_usuario,
            rol if filtro_usuario in [None, "Todos"] else "user",
            incluir_nombre=True
        )

        proyectos_filtrados = []
        for row in proyectos_raw:
            if (filtro_estado == "Todos" or row[4] == filtro_estado) and \
               (filtro_prioridad == "Todos" or row[5] == filtro_prioridad):
                proyectos_filtrados.append({
                    "ID": row[0], "Nombre": row[1], "Descripción": row[2], "Responsable": row[3],
                    "Estado": row[4], "Prioridad": row[5], "Inicio": row[6], "Fin": row[7], "Creado por": row[8]
                })

        df_proyectos = pd.DataFrame(proyectos_filtrados)
        df_comentarios = pd.DataFrame(comentarios, columns=["Proyecto ID", "Nombre Proyecto", "Autor", "Comentario", "Fecha"])

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_proyectos.to_excel(writer, index=False, sheet_name="Proyectos")
            df_comentarios.to_excel(writer, index=False, sheet_name="Comentarios")
        output.seek(0)

        st.sidebar.download_button(
            label="📥 Descargar Excel",
            data=output,
            file_name="proyectos_exportados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # ===============================
    # 📁 Listado principal
    # ===============================
    st.title(f"📁 Gestor de Proyectos: [{username}]")
    agrupamiento = st.radio("Agrupar por:", ["Prioridad", "Estado"], horizontal=True)

    proyectos_raw = db.obtener_proyectos(usuario, rol)
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
            "fecha_fin": row[7],
            "asignado_a": row[8]
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
                st.markdown(f"**Asignado a:** `{proyecto['asignado_a']}`")

                # ======= Actualizar estado =======
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

                # ======= Editar proyecto =======
                with st.expander(f"✏️ Editar proyecto {proyecto['nombre']}", expanded=False):
                    nuevo_nombre = st.text_input("Nombre", value=proyecto["nombre"], key=f"edit_nombre_{proyecto['id']}")
                    nueva_descripcion = st.text_area("Descripción", value=proyecto["descripcion"], key=f"edit_desc_{proyecto['id']}")
                    nuevo_responsable = st.text_input("Responsable", value=proyecto["responsable"], key=f"edit_resp_{proyecto['id']}")
                    nueva_prioridad = st.selectbox("Prioridad", PRIORIDADES, index=PRIORIDADES.index(proyecto["prioridad"]), key=f"edit_prio_{proyecto['id']}")
                    nueva_fecha_inicio = st.date_input("Inicio", pd.to_datetime(proyecto["fecha_inicio"]), key=f"edit_ini_{proyecto['id']}")
                    nueva_fecha_fin = st.date_input("Fin", pd.to_datetime(proyecto["fecha_fin"]), key=f"edit_fin_{proyecto['id']}")

                    if st.button("💾 Guardar cambios", key=f"save_edit_{proyecto['id']}"):
                        db.actualizar_proyecto(
                            proyecto["id"],
                            nuevo_nombre,
                            nueva_descripcion,
                            nuevo_responsable,
                            nuevo_estado,  # conserva el valor actualizado
                            nueva_prioridad,
                            nueva_fecha_inicio.strftime("%Y-%m-%d"),
                            nueva_fecha_fin.strftime("%Y-%m-%d")
                        )
                        st.success("✅ Proyecto actualizado.")
                        st.rerun()

                # ======= Comentarios =======
                st.markdown("**Comentarios:**")
                comentarios = db.obtener_comentarios(proyecto["id"])
                for autor, texto, fecha in comentarios:
                    st.markdown(f"- {fecha} [{autor}]: {texto}")

                with st.form(f"form_comentario_{proyecto['id']}"):
                    autor = st.text_input("Tu nombre", value=usuario, key=f"autor_{proyecto['id']}")
                    texto = st.text_area("Comentario", key=f"texto_{proyecto['id']}")
                    enviar = st.form_submit_button("Añadir comentario")
                    if enviar and autor and texto:
                        db.agregar_comentario(proyecto["id"], autor, texto, datetime.now().strftime("%Y-%m-%d"))
                        st.success("💬 Comentario guardado")
                        st.rerun()

                # ======= Eliminar proyecto =======
                if rol == "admin":
                    del_key = f"del_{proyecto['id']}"

                    if st.button("🗑️ Eliminar proyecto", key=f"delbtn_{proyecto['id']}"):
                        st.session_state["confirmar_eliminacion"] = proyecto["id"]
                        st.warning(f"⚠️ Confirma la eliminación del proyecto: '{proyecto['nombre']}'")

                    if st.session_state.get("confirmar_eliminacion") == proyecto["id"]:
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("✅ Confirmar eliminación", key=f"confirmar_{proyecto['id']}"):
                                db.eliminar_proyecto(proyecto["id"])
                                st.success("✅ Proyecto eliminado.")
                                st.session_state["confirmar_eliminacion"] = None
                                st.rerun()
                        with col2:
                            if st.button("❌ Cancelar", key=f"cancelar_{proyecto['id']}"):
                                st.session_state["confirmar_eliminacion"] = None
                                st.info("❎ Eliminación cancelada.")
                                st.rerun()

  

    # ===============================
    # ➕ Añadir nuevo proyecto
    # ===============================
    with st.expander("➕ Añadir nuevo proyecto"):
        with st.form("nuevo_proyecto_form"):
            nombre = st.text_input("Nombre del proyecto")
            descripcion = st.text_area("Descripción")
            responsable = st.text_input("Responsable")
            estado = st.selectbox("Estado", ESTADOS)
            prioridad = st.selectbox("Prioridad", PRIORIDADES)
            fecha_inicio = st.date_input("Fecha de inicio")
            fecha_fin = st.date_input("Fecha de fin")

            if rol == "admin":
                usuarios_disponibles = db.obtener_usuarios()
                creado_por = st.selectbox("Asignar a usuario", usuarios_disponibles)
            else:
                creado_por = usuario

            guardar = st.form_submit_button("Guardar proyecto")

            if guardar:
                if not nombre or not descripcion or not responsable:
                    st.error("❌ Completa todos los campos obligatorios.")
                else:
                    db.agregar_proyecto(
                        nombre, descripcion, responsable, estado, prioridad,
                        fecha_inicio.strftime("%Y-%m-%d"),
                        fecha_fin.strftime("%Y-%m-%d"),
                        creado_por
                    )
                    st.success("✅ Proyecto creado")
                    st.rerun()

    # ===============================
    # 📊 Tabla general de proyectos
    # ===============================
    with st.expander("📊 Ver todos los proyectos"):
        estado_tabla = st.selectbox("Estado", ["Todos"] + ESTADOS, key="estado_tabla")
        prioridad_tabla = st.selectbox("Prioridad", ["Todos"] + PRIORIDADES, key="prioridad_tabla")

        usuario_tabla = usuario
        if rol == "admin":
            usuario_tabla = st.selectbox("Usuario", ["Todos"] + usuarios_disponibles, key="usuario_tabla")

        tabla_proyectos = db.obtener_proyectos(
            usuario if usuario_tabla == "Todos" else usuario_tabla,
            rol if usuario_tabla == "Todos" else "user"
        )

        proyectos_tabla = []
        for row in tabla_proyectos:
            p = {
                "ID": row[0], "Nombre": row[1], "Descripción": row[2], "Responsable": row[3],
                "Estado": row[4], "Prioridad": row[5], "Inicio": row[6], "Fin": row[7], "Creado por": row[8]
            }
            if (estado_tabla == "Todos" or p["Estado"] == estado_tabla) and \
               (prioridad_tabla == "Todos" or p["Prioridad"] == prioridad_tabla):
                proyectos_tabla.append(p)

        df = pd.DataFrame(proyectos_tabla)
        if not df.empty:
            st.dataframe(df.drop(columns=["ID"]), use_container_width=True)
        else:
            st.info("No hay proyectos con esos filtros.")


if __name__ == "__main__":
    main()

import streamlit as st
from datetime import datetime
from app import db
import pandas as pd
from io import BytesIO
import plotly.express as px

# ---------------------------------
# Constantes de Estados y Prioridades
# ---------------------------------
ESTADOS = ["En ejecución", "Terminado", "Bloqueado", "En revisión", "Pendiente"]
PRIORIDADES = ["Alta", "Media", "Baja"]

def main():

    # ---------------------------------
    # Inicializar session_state seguro
    # ---------------------------------
    if "rol" not in st.session_state:
        st.session_state["rol"] = None

    if "usuario" not in st.session_state:
        st.session_state["usuario"] = None

    # ---------------------------------
    # Inicializar base de datos y página
    # ---------------------------------
    db.crear_tablas()

    # ---------------------------------
    # Sidebar: Login
    # ---------------------------------
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

    
    if st.session_state["usuario"] is None:
        st.stop()

    # ---------------------------------
    # Variables globales de usuario
    # ---------------------------------
    usuario = st.session_state["usuario"]
    rol = st.session_state["rol"]
    usuarios_disponibles = db.obtener_usuarios() if rol == "admin" else []

    st.sidebar.markdown(f"👤 Usuario: `{usuario}` | Rol: `{rol}`")

    # ---------------------------------
    # Sidebar: Exportar proyectos a Excel
    # ---------------------------------
    st.sidebar.title("📤 Exportar proyectos")
    filtro_estado = st.sidebar.selectbox("Filtrar por estado", ["Todos"] + ESTADOS)
    filtro_prioridad = st.sidebar.selectbox("Filtrar por prioridad", ["Todos"] + PRIORIDADES)

    filtro_usuario = None
    if rol == "admin":
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

        # Filtrar proyectos según estado y prioridad
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

        # Crear archivo Excel en memoria
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

    # ---------------------------------
    # Título principal
    # ---------------------------------
    st.title(f"📁 Gestor de Proyectos: [{usuario}]")

    # ---------------------------------
    # Tabla con todos los proyectos (ahora justo debajo del título)
    # ---------------------------------
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

            # Gráfico de Barras
            df_agg = df.groupby(['Estado', 'Prioridad']).size().reset_index(name='Número de Proyectos')
            fig3 = px.bar(
                df_agg,
                x='Estado',
                y='Número de Proyectos',
                color='Prioridad',
                barmode='stack',
                title='Número de Proyectos (Prioridad vs Estado)'
            )
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("No hay proyectos con esos filtros.")

    st.markdown("---")

    # ---------------------------------
    # Visualización de proyectos agrupados
    # ---------------------------------
    agrupamiento = st.radio("Agrupar por:", ["Prioridad", "Estado"], horizontal=True)

    proyectos_raw = db.obtener_proyectos(usuario, rol)
    proyectos = [{
        "id": row[0],
        "nombre": row[1],
        "descripcion": row[2],
        "responsable": row[3],
        "estado": row[4],
        "prioridad": row[5],
        "fecha_inicio": row[6],
        "fecha_fin": row[7],
        "asignado_a": row[8]
    } for row in proyectos_raw]

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

                # ---------------------------------
                # Expander para editar proyecto
                # ---------------------------------
                with st.expander(f"✏️ Editar proyecto IA: {proyecto['nombre']}"):
                    nuevo_nombre = st.text_input("Nombre", value=proyecto["nombre"], key=f"edit_nombre_{proyecto['id']}")
                    nueva_desc = st.text_area("Descripción", value=proyecto["descripcion"], key=f"edit_desc_{proyecto['id']}")
                    nuevo_resp = st.text_input("Responsable", value=proyecto["responsable"], key=f"edit_resp_{proyecto['id']}")
                    nueva_prio = st.selectbox("Prioridad", PRIORIDADES, index=PRIORIDADES.index(proyecto["prioridad"]), key=f"edit_prio_{proyecto['id']}")
                    nueva_ini = st.date_input("Inicio", pd.to_datetime(proyecto["fecha_inicio"]), key=f"edit_ini_{proyecto['id']}")
                    nueva_fin = st.date_input("Fin", pd.to_datetime(proyecto["fecha_fin"]), key=f"edit_fin_{proyecto['id']}")
                    nueva_estado = st.selectbox("Estado", ESTADOS, index=ESTADOS.index(proyecto["estado"]), key=f"edit_estado_{proyecto['id']}")

                    if st.button("💾 Guardar cambios", key=f"save_edit_{proyecto['id']}"):
                        db.actualizar_proyecto(
                            proyecto["id"],
                            nuevo_nombre,
                            nueva_desc,
                            nuevo_resp,
                            nueva_estado,
                            nueva_prio,
                            nueva_ini.strftime("%Y-%m-%d"),
                            nueva_fin.strftime("%Y-%m-%d")
                        )
                        st.success("✅ Proyecto actualizado.")
                        st.rerun()

                # ---------------------------------
                # Comentarios del proyecto
                # ---------------------------------
                st.markdown("**Comentarios:**")
                comentarios = db.obtener_comentarios(proyecto["id"])
                for autor, texto, fecha, cid in comentarios:
                    cols = st.columns([8, 1])
                    with cols[0]:
                        st.markdown(f"- {fecha} [{autor}]: {texto}")
                    if rol == "admin":
                        with cols[1]:
                            if st.button("🗑️", key=f"delcom_{cid}", help="Eliminar comentario"):
                                st.session_state["confirmar_eliminacion_comentario"] = cid

                        if st.session_state.get("confirmar_eliminacion_comentario") == cid:
                            st.warning(f"⚠️ ¿Eliminar comentario de **{autor}** ({fecha})?\n\n> {texto}")
                            c1, c2 = st.columns(2)
                            with c1:
                                if st.button("✅ Confirmar", key=f"conf_com_{cid}"):
                                    db.eliminar_comentario(cid)
                                    st.success("🗑️ Comentario eliminado.")
                                    st.session_state["confirmar_eliminacion_comentario"] = None
                                    st.rerun()
                            with c2:
                                if st.button("❌ Cancelar", key=f"cancel_com_{cid}"):
                                    st.session_state["confirmar_eliminacion_comentario"] = None
                                    st.rerun()

                # ---------------------------------
                # Formulario para agregar comentario
                # ---------------------------------
                with st.form(f"form_comentario_{proyecto['id']}"):
                    autor = st.text_input("Tu nombre", value=usuario, key=f"autor_{proyecto['id']}")
                    texto = st.text_area("Comentario", key=f"texto_{proyecto['id']}")
                    enviar = st.form_submit_button("Añadir comentario")
                    if enviar and autor and texto:
                        db.agregar_comentario(proyecto["id"], autor, texto, datetime.now().strftime("%Y-%m-%d"))
                        st.success("💬 Comentario guardado")
                        st.session_state.pop(f"autor_{proyecto['id']}", None)
                        st.session_state.pop(f"texto_{proyecto['id']}", None)
                        st.rerun()

                # ---------------------------------
                # Botón para eliminar proyecto (admin)
                # ---------------------------------
                if rol == "admin":
                    if st.button("🗑️ Eliminar proyecto", key=f"delbtn_{proyecto['id']}"):
                        st.session_state["confirmar_eliminacion"] = proyecto["id"]

                    if st.session_state.get("confirmar_eliminacion") == proyecto["id"]:
                        st.warning(f"⚠️ Confirma la eliminación de '{proyecto['nombre']}'")
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("✅ Confirmar", key=f"conf_{proyecto['id']}"):
                                db.eliminar_proyecto(proyecto["id"])
                                st.success("✅ Proyecto eliminado.")
                                st.session_state["confirmar_eliminacion"] = None
                                st.rerun()
                        with col2:
                            if st.button("❌ Cancelar", key=f"canc_{proyecto['id']}"):
                                st.session_state["confirmar_eliminacion"] = None
                                st.rerun()

    # ---------------------------------
    # Formulario para añadir nuevo proyecto
    # ---------------------------------
    st.markdown("---")
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


if __name__ == "__main__":
    main()

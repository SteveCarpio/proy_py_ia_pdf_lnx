import sqlite3

DB_PATH = "data/proyectos.db"

def conectar():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    # Tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            rol TEXT
        )
    ''')

    # Tabla de proyectos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proyectos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            descripcion TEXT,
            responsable TEXT,
            estado TEXT,
            prioridad TEXT,
            fecha_inicio TEXT,
            fecha_fin TEXT,
            creado_por TEXT
        )
    ''')

    # Tabla de comentarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comentarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proyecto_id INTEGER,
            autor TEXT,
            texto TEXT,
            fecha TEXT,
            FOREIGN KEY (proyecto_id) REFERENCES proyectos(id)
        )
    ''')

    conn.commit()
    conn.close()
    crear_usuarios_por_defecto()

def crear_usuarios_por_defecto():
    if not obtener_usuario("admin"):
        crear_usuario("admin", "admin123", "admin")
    if not obtener_usuario("Steve"):
        crear_usuario("Steve", "user123", "user")
    if not obtener_usuario("LuisRF"):
        crear_usuario("LuisRF", "user123", "user")

def crear_usuario(username, password, rol="user"):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)", (username, password, rol))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # usuario ya existe
    conn.close()

def validar_usuario(username, password):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT rol FROM usuarios WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        return user[0]  # rol
    return None

def obtener_usuario(username):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# Proyectos
def agregar_proyecto(nombre, descripcion, responsable, estado, prioridad, fecha_inicio, fecha_fin, creado_por):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO proyectos (nombre, descripcion, responsable, estado, prioridad, fecha_inicio, fecha_fin, creado_por)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nombre, descripcion, responsable, estado, prioridad, fecha_inicio, fecha_fin, creado_por))
    conn.commit()
    conn.close()

def obtener_proyectos(usuario, rol):
    conn = conectar()
    cursor = conn.cursor()
    if rol == "admin":
        cursor.execute("SELECT * FROM proyectos")
    else:
        cursor.execute("SELECT * FROM proyectos WHERE creado_por = ?", (usuario,))
    proyectos = cursor.fetchall()
    conn.close()
    return proyectos

def actualizar_estado(proyecto_id, nuevo_estado):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE proyectos SET estado = ? WHERE id = ?", (nuevo_estado, proyecto_id))
    conn.commit()
    conn.close()

def eliminar_proyecto(proyecto_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM proyectos WHERE id = ?", (proyecto_id,))
    conn.commit()
    conn.close()

# Comentarios
def agregar_comentario(proyecto_id, autor, texto, fecha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO comentarios (proyecto_id, autor, texto, fecha)
        VALUES (?, ?, ?, ?)
    ''', (proyecto_id, autor, texto, fecha))
    conn.commit()
    conn.close()

def obtener_comentarios(proyecto_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT autor, texto, fecha FROM comentarios WHERE proyecto_id = ?", (proyecto_id,))
    comentarios = cursor.fetchall()
    conn.close()
    return comentarios

def obtener_todos_comentarios(usuario, rol):
    conn = conectar()
    cursor = conn.cursor()
    if rol == "admin":
        cursor.execute("SELECT proyecto_id, autor, texto, fecha FROM comentarios")
    else:
        cursor.execute("""
            SELECT c.proyecto_id, c.autor, c.texto, c.fecha
            FROM comentarios c
            JOIN proyectos p ON c.proyecto_id = p.id
            WHERE p.creado_por = ?
        """, (usuario,))
    comentarios = cursor.fetchall()
    conn.close()
    return comentarios


def obtener_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM usuarios")
    usuarios = [row[0] for row in cursor.fetchall()]
    conn.close()
    return usuarios

def obtener_todos_comentarios(usuario, rol, incluir_nombre=False):
    conn = conectar()
    cursor = conn.cursor()
    if rol == "admin":
        if incluir_nombre:
            cursor.execute("""
                SELECT c.proyecto_id, p.nombre, c.autor, c.texto, c.fecha
                FROM comentarios c
                JOIN proyectos p ON c.proyecto_id = p.id
            """)
        else:
            cursor.execute("SELECT proyecto_id, autor, texto, fecha FROM comentarios")
    else:
        if incluir_nombre:
            cursor.execute("""
                SELECT c.proyecto_id, p.nombre, c.autor, c.texto, c.fecha
                FROM comentarios c
                JOIN proyectos p ON c.proyecto_id = p.id
                WHERE p.creado_por = ?
            """, (usuario,))
        else:
            cursor.execute("""
                SELECT c.proyecto_id, c.autor, c.texto, c.fecha
                FROM comentarios c
                JOIN proyectos p ON c.proyecto_id = p.id
                WHERE p.creado_por = ?
            """, (usuario,))
    comentarios = cursor.fetchall()
    conn.close()
    return comentarios

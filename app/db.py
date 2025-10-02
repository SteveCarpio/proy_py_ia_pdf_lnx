import sqlite3
from pathlib import Path

DB_PATH = Path("data/proyectos.db")

def crear_tabla():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS proyectos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        descripcion TEXT,
        responsable TEXT,
        estado TEXT,
        prioridad TEXT,
        fecha_inicio TEXT,
        fecha_fin TEXT
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS comentarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        proyecto_id INTEGER,
        autor TEXT,
        texto TEXT,
        fecha TEXT,
        FOREIGN KEY(proyecto_id) REFERENCES proyectos(id)
    )
    """)
    conn.commit()
    conn.close()

def obtener_proyectos():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM proyectos")
    rows = c.fetchall()
    conn.close()
    return rows

def obtener_comentarios(proyecto_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT autor, texto, fecha FROM comentarios WHERE proyecto_id = ?", (proyecto_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def agregar_proyecto(nombre, descripcion, responsable, estado, prioridad, fecha_inicio, fecha_fin):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    INSERT INTO proyectos (nombre, descripcion, responsable, estado, prioridad, fecha_inicio, fecha_fin)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (nombre, descripcion, responsable, estado, prioridad, fecha_inicio, fecha_fin))
    conn.commit()
    conn.close()

def actualizar_estado(proyecto_id, nuevo_estado):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE proyectos SET estado = ? WHERE id = ?", (nuevo_estado, proyecto_id))
    conn.commit()
    conn.close()

def agregar_comentario(proyecto_id, autor, texto, fecha):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    INSERT INTO comentarios (proyecto_id, autor, texto, fecha)
    VALUES (?, ?, ?, ?)
    """, (proyecto_id, autor, texto, fecha))
    conn.commit()
    conn.close()

def eliminar_proyecto(proyecto_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM comentarios WHERE proyecto_id = ?", (proyecto_id,))
    c.execute("DELETE FROM proyectos WHERE id = ?", (proyecto_id,))
    conn.commit()
    conn.close()

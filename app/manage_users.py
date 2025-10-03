# Crear un nuevo usuario
# python manage_users.py crear Steve user123 user

# Cambiar contraseña
# python manage_users.py cambiar_pass Steve nueva_clave

# Eliminar usuario
# python manage_users.py eliminar Steve

# Ver usuarios
# python manage_users.py listar



import sqlite3
import argparse
import os

DB_PATH = os.path.join("data", "proyectos.db")

def conectar():
    return sqlite3.connect(DB_PATH)

def crear_tabla_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            rol TEXT CHECK(rol IN ('admin', 'user')) NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def agregar_usuario(username, password, rol):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)", (username, password, rol))
        conn.commit()
        print(f"✅ Usuario '{username}' creado con rol '{rol}'.")
    except sqlite3.IntegrityError:
        print(f"❌ El usuario '{username}' ya existe.")
    conn.close()

def eliminar_usuario(username):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE username = ?", (username,))
    if cursor.rowcount == 0:
        print(f"⚠️ Usuario '{username}' no encontrado.")
    else:
        print(f"🗑️ Usuario '{username}' eliminado.")
    conn.commit()
    conn.close()

def cambiar_password(username, nueva_password):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET password = ? WHERE username = ?", (nueva_password, username))
    if cursor.rowcount == 0:
        print(f"⚠️ Usuario '{username}' no encontrado.")
    else:
        print(f"🔐 Contraseña actualizada para '{username}'.")
    conn.commit()
    conn.close()

def listar_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT username, rol FROM usuarios")
    rows = cursor.fetchall()
    if not rows:
        print("⚠️ No hay usuarios registrados.")
    else:
        print("👥 Usuarios registrados:")
        for username, rol in rows:
            print(f"  - {username} ({rol})")
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gestión de usuarios (proyectos.db)")
    subparsers = parser.add_subparsers(dest="comando")

    agregar = subparsers.add_parser("crear")
    agregar.add_argument("username")
    agregar.add_argument("password")
    agregar.add_argument("rol", choices=["admin", "user"])

    eliminar = subparsers.add_parser("eliminar")
    eliminar.add_argument("username")

    cambiar = subparsers.add_parser("cambiar_pass")
    cambiar.add_argument("username")
    cambiar.add_argument("nueva_password")

    listar = subparsers.add_parser("listar", help="Listar todos los usuarios")

    args = parser.parse_args()
    crear_tabla_usuarios()

    if args.comando == "crear":
        agregar_usuario(args.username, args.password, args.rol)
    elif args.comando == "eliminar":
        eliminar_usuario(args.username)
    elif args.comando == "cambiar_pass":
        cambiar_password(args.username, args.nueva_password)
    elif args.comando == "listar":
        listar_usuarios()
    else:
        parser.print_help()

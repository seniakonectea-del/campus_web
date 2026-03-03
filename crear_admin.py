"""
Script para crear el usuario administrador inicial.
Ejecutar UNA SOLA VEZ después de configurar la base de datos:

    python crear_admin.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from db import init_db, get_connection
from werkzeug.security import generate_password_hash

def crear_admin(nombre, email, password):
    init_db()  # Asegura que las tablas existen
    conn = get_connection()
    cur  = conn.cursor()
    hash_pw = generate_password_hash(password)
    try:
        cur.execute(
            """INSERT INTO usuarios (nombre, email, password, rol)
               VALUES (%s, %s, %s, 'admin')
               ON CONFLICT (email) DO NOTHING""",
            (nombre, email, hash_pw)
        )
        conn.commit()
        print(f"✅ Admin creado: {email}")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    crear_admin(
        nombre="Administrador",
        email="admin@campus.com",
        password="admin123"
    )

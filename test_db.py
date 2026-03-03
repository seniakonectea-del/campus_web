#!/usr/bin/env python
"""Script para probar la conexión y estructura de la BD."""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from db import init_db, get_connection
from models.usuario import Usuario

def test_database():
    print("1️⃣  Inicializando base de datos...")
    try:
        init_db()
        print("   ✅ Base de datos inicializada")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return

    print("\n2️⃣  Probando crear usuario...")
    try:
        usuario = Usuario.crear(
            nombre="Test User",
            email="test@example.com",
            password_plano="password123"
        )
        print(f"   ✅ Usuario creado: {usuario.nombre} ({usuario.email})")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return

    print("\n3️⃣  Probando buscar usuario...")
    try:
        found = Usuario.buscar_por_email("test@example.com")
        if found:
            print(f"   ✅ Usuario encontrado: {found.nombre}")
        else:
            print("   ❌ Usuario no encontrado")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return

    print("\n✅ Todas las pruebas pasaron correctamente!")

if __name__ == "__main__":
    test_database()

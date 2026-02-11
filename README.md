# campus_web

Proyecto de formación: aplicación web básica para gestión de usuarios usada como ejemplo didáctico.

**Descripción**

`campus_web` es un proyecto de formación que muestra una aplicación en Flask con vistas en HTML/CSS y persistencia en PostgreSQL. Está pensado para aprender a construir una app web completa (servidor, plantillas, gestión de sesiones y base de datos).

**Tecnologías implicadas**

- HTML, CSS
- Python
- Flask
- PostgreSQL
- psycopg2 (conector PostgreSQL para Python)
- python-dotenv (gestión de variables de entorno)

**Requisitos previos**

- Python 3.10+ instalado
- Git
- PostgreSQL (servidor instalado y `psql` disponible)

**Clonar el repositorio**

```bash
git clone https://github.com/seniakonectea-del/campus_web.git
cd campus_web
```

**Crear y activar entorno virtual**

- PowerShell:
```powershell
python -m venv .venv
& .venv\Scripts\Activate.ps1
```
- CMD:
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```
- Bash/WSL:
```bash
python -m venv .venv
source .venv/bin/activate
```

**Instalar dependencias**

```bash
pip install -r requirements.txt
```

**Variables de entorno (.env)**

Cree un archivo `.env` en la raíz del proyecto con las credenciales de la base de datos y, opcionalmente, la clave secreta de Flask. Ejemplo:

```
DB_host=localhost
DB_NAME=campusdb
DB_user=campus_user
DB_password=tu_password_segura
FLASK_SECRET=un_valor_secreto
```

En `app.py` el proyecto lee `DB_host`, `DB_NAME`, `DB_user` y `DB_password`.

**Crear la base de datos (PostgreSQL)**

Ejemplos de comandos con `psql` (ejecutar como usuario administrador de postgres o con permisos):

1) Crear usuario y base de datos:

```sql
-- En psql:
CREATE USER campus_user WITH PASSWORD 'tu_password_segura';
CREATE DATABASE campusdb OWNER campus_user;
```

2) Conectar a la base de datos y crear la tabla `Usuarios` requerida por la app:

```sql
-- Conectarse:
\c campusdb
-- Crear tabla (nombre con mayúsculas como usa la app):
CREATE TABLE "Usuarios" (
  id SERIAL PRIMARY KEY,
  usuario VARCHAR(255) UNIQUE NOT NULL,
  usuario_mail VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL
);
```

Si prefieres hacerlo todo desde la línea de comandos (Windows PowerShell / Bash):

```bash
# Crear usuario y DB (ejecutar como postgres o usando psql con un superusuario)
psql -U postgres -c "CREATE USER campus_user WITH PASSWORD 'tu_password_segura';"
psql -U postgres -c "CREATE DATABASE campusdb OWNER campus_user;"
psql -U campus_user -d campusdb -c "CREATE TABLE \"Usuarios\" (id SERIAL PRIMARY KEY, usuario VARCHAR(255) UNIQUE NOT NULL, usuario_mail VARCHAR(255) UNIQUE NOT NULL, password VARCHAR(255) NOT NULL);"
```

**Ejecutar la aplicación**

Con el entorno virtual activado y el `.env` creado:

```bash
python app.py
```

La app por defecto corre en `http://127.0.0.1:5000`.

**Notas y recomendaciones**

- El archivo `requirements.txt` incluye las dependencias con versiones fijadas. Puedes eliminar `psycopg2` y mantener solo `psycopg2-binary` si prefieres evitar compilar extensiones nativas.
- Cambia `app.secret_key` por la variable de entorno `FLASK_SECRET` o similar para producción.
- Para despliegues y reproducibilidad, considera usar `docker-compose` con un servicio `postgres` o herramientas como `pip-tools` / `poetry`.

Si quieres, puedo:
- Generar un `docker-compose.yml` para levantar la app + PostgreSQL rápidamente.
- Simplificar `requirements.txt` quitando duplicados.

<a href="https://github.com/seniakonectea-del/campus_web">Campus_web</a> © 2026 by 
<a href="https://ejemplo.com">Senia Rasel</a> is licensed under 
<a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>
<img src="https://mirrors.creativecommons.org/presskit/icons/cc.svg" alt="" style="max-width: 1em;max-height:1em;margin-left: .2em;">
<img src="https://mirrors.creativecommons.org/presskit/icons/by.svg" alt="" style="max-width: 1em;max-height:1em;margin-left: .2em;">
<img src="https://mirrors.creativecommons.org/presskit/icons/sa.svg" alt="" style="max-width: 1em;max-height:1em;margin-left: .2em;">
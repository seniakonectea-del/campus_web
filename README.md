# 🎓 Campus Web

Aplicación web para la gestión de usuarios y eventos académicos, desarrollada con **Python + Flask** y **PostgreSQL**.

🔗 **Despliegue en Railway:** `[AÑADIR URL AQUÍ TRAS EL DESPLIEGUE]`  
📦 **Repositorio:** https://github.com/seniakonectea-del/campus_web

---

## 📋 Descripción del proyecto

Campus Web es una plataforma académica que permite gestionar usuarios con diferentes niveles de acceso (administrador, profesor y alumno) y un calendario de eventos del campus con filtros avanzados por fecha.

---

## 🗂️ Estructura del proyecto

```
campus_web/
├── app.py                  # Entry point: crea la app Flask y registra blueprints
├── config.py               # Configuración centralizada (variables de entorno)
├── db.py                   # Conexión a PostgreSQL e inicialización de tablas
├── crear_admin.py          # Script para crear el usuario admin inicial
├── schema.sql              # Script SQL de la base de datos
│
├── models/
│   ├── __init__.py
│   ├── usuario.py          # Clase Usuario (POO + CRUD)
│   └── evento.py           # Clase Evento (POO + CRUD + filtros)
│
├── controllers/
│   ├── __init__.py
│   ├── auth.py             # Login, registro, logout
│   ├── auth_utils.py       # Decoradores: login_required, rol_requerido
│   ├── dashboard.py        # Dashboard por rol
│   ├── eventos.py          # CRUD de eventos + filtros por fecha
│   └── admin.py            # Gestión de usuarios (solo admin)
│
├── templates/
│   ├── base.html           # Layout base con navbar dinámica por rol
│   ├── auth/               # Login y registro
│   ├── dashboard/          # Vistas por rol (admin, profesor, alumno)
│   ├── eventos/            # Lista con filtros + formulario
│   └── admin/              # Gestión de usuarios
│
├── static/
│   └── css/style.css       # Estilos globales responsive
│
├── requirements.txt
├── Procfile                # Configuración gunicorn para Railway
├── runtime.txt
├── .env.example            # Plantilla de variables de entorno
└── .gitignore
```

---

## 🧱 Aplicación de Programación Orientada a Objetos (POO)

El proyecto aplica POO de forma explícita y estructurada:

### Clase `Usuario` (`models/usuario.py`)
Encapsula toda la lógica de un usuario del sistema:
- **Atributos:** `id`, `nombre`, `email`, `password`, `rol`, `creado`
- **Propiedades:** `es_admin`, `es_profesor`, `es_alumno` (getters limpios)
- **Métodos de clase (factory):** `crear()`, `buscar_por_email()`, `buscar_por_id()`, `listar_todos()`
- **Métodos de instancia:** `actualizar()`, `eliminar()`, `verificar_password()`, `to_dict()`

### Clase `Evento` (`models/evento.py`)
Encapsula la lógica de eventos académicos:
- **Atributos:** `id`, `titulo`, `descripcion`, `fecha_inicio`, `fecha_fin`, `creado_por`, `visible_para`
- **Métodos de clase:** `crear()`, `buscar_por_id()`, `listar_todos()`, `listar_para_rol()`, `filtrar_por_fechas()`
- **Métodos de instancia:** `actualizar()`, `eliminar()`, `to_dict()`

### Separación de responsabilidades
| Capa | Responsabilidad |
|---|---|
| `models/` | Lógica de negocio y acceso a datos |
| `controllers/` | Rutas HTTP y lógica de presentación |
| `templates/` | Renderizado HTML (Jinja2) |
| `db.py` | Conexión y gestión de la BD |
| `config.py` | Configuración centralizada |

---

## 🗄️ Base de datos (PostgreSQL)

### Tabla `usuarios`
| Campo | Tipo | Descripción |
|---|---|---|
| `id` | SERIAL PK | Identificador único |
| `nombre` | VARCHAR(100) | Nombre completo |
| `email` | VARCHAR(255) UNIQUE | Email de acceso |
| `password` | VARCHAR(255) | Hash werkzeug |
| `rol` | VARCHAR(20) | `admin`, `profesor` o `alumno` |
| `creado` | TIMESTAMP | Fecha de registro |

### Tabla `eventos`
| Campo | Tipo | Descripción |
|---|---|---|
| `id` | SERIAL PK | Identificador único |
| `titulo` | VARCHAR(200) | Nombre del evento |
| `descripcion` | TEXT | Descripción opcional |
| `fecha_inicio` | TIMESTAMP | Inicio del evento |
| `fecha_fin` | TIMESTAMP | Fin del evento (opcional) |
| `creado_por` | INTEGER FK → `usuarios.id` | Quién creó el evento |
| `visible_para` | VARCHAR(20) | `todos`, `profesor` o `alumno` |
| `creado` | TIMESTAMP | Fecha de creación |

**Relación:** `eventos.creado_por` → `usuarios.id` (clave foránea con `ON DELETE SET NULL`)

---

## 👥 Roles y permisos

| Acción | Alumno | Profesor | Admin |
|---|:---:|:---:|:---:|
| Ver eventos | ✅ | ✅ | ✅ |
| Crear eventos | ❌ | ✅ | ✅ |
| Editar eventos | ❌ | ❌ | ✅ |
| Eliminar eventos | ❌ | ❌ | ✅ |
| Ver panel de usuarios | ❌ | ❌ | ✅ |
| Editar usuarios | ❌ | ❌ | ✅ |
| Filtrar eventos por fecha | ✅ | ✅ | ✅ |

La restricción de acceso se implementa con decoradores reutilizables en `controllers/auth_utils.py`:
- `@login_required` — redirige al login si no hay sesión
- `@rol_requerido("admin", "profesor")` — restringe por rol

---

## ✨ Mejora personal: Filtros avanzados por fecha

Se ha implementado un sistema de **filtrado de eventos por rango de fechas** como mejora personal:

- Ubicación: `controllers/eventos.py` → método `lista()` y `models/evento.py` → `filtrar_por_fechas()`
- Interfaz: barra de filtros en `templates/eventos/lista.html`
- Funcionalidad: el usuario puede filtrar eventos indicando una fecha de inicio (`desde`) y/o una fecha de fin (`hasta`)
- La consulta SQL se construye dinámicamente añadiendo cláusulas `WHERE` solo cuando se proporcionan fechas
- Compatible con todos los roles (respeta la visibilidad del evento según el rol del usuario)

---

## 🚀 Instalación local

```bash
# 1. Clonar el repositorio
git clone https://github.com/seniakonectea-del/campus_web.git
cd campus_web

# 2. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
# .venv\Scripts\activate.bat     # Windows CMD

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Edita .env con tus credenciales de PostgreSQL

# 5. Crear usuario admin inicial
python crear_admin.py

# 6. Arrancar la aplicación
python app.py
```

La app estará disponible en `http://127.0.0.1:5000`

**Credenciales admin por defecto:**
- Email: `admin@campus.com`
- Password: `admin123`

---

## ☁️ Despliegue en Railway

1. Haz push del proyecto a GitHub
2. En [railway.app](https://railway.app), crea un nuevo proyecto → *Deploy from GitHub repo*
3. Añade un servicio **PostgreSQL** desde el dashboard de Railway
4. En las variables de entorno del servicio web, configura:
   - `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_PORT` (valores del servicio PostgreSQL de Railway)
   - `FLASK_SECRET` → un valor secreto largo y aleatorio
5. Railway usará el `Procfile` para arrancar con `gunicorn`
6. Las tablas se crean automáticamente al arrancar (`init_db()` en `app.py`)
7. Ejecuta `python crear_admin.py` desde Railway Shell para crear el admin

---

## 🛠️ Tecnologías

- **Python 3.11** + **Flask 3.0**
- **PostgreSQL** + **psycopg2-binary**
- **Werkzeug** (hashing de contraseñas)
- **Jinja2** (templates)
- **Gunicorn** (servidor WSGI para producción)
- **Railway** (despliegue en la nube)

---

Campus Web © 2026 · Senia Rasel · [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

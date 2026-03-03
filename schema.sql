-- =============================================
-- campus_web – Script de inicialización de BD
-- Ejecutar con: psql -U usuario -d campusdb -f schema.sql
-- =============================================

-- Tabla de usuarios (con roles)
CREATE TABLE IF NOT EXISTS usuarios (
    id       SERIAL PRIMARY KEY,
    nombre   VARCHAR(100) NOT NULL,
    email    VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    rol      VARCHAR(20)  NOT NULL DEFAULT 'alumno'
             CHECK (rol IN ('admin', 'profesor', 'alumno')),
    creado   TIMESTAMP DEFAULT NOW()
);

-- Tabla de eventos académicos
CREATE TABLE IF NOT EXISTS eventos (
    id           SERIAL PRIMARY KEY,
    titulo       VARCHAR(200) NOT NULL,
    descripcion  TEXT,
    fecha_inicio TIMESTAMP NOT NULL,
    fecha_fin    TIMESTAMP,
    creado_por   INTEGER REFERENCES usuarios(id) ON DELETE SET NULL,
    visible_para VARCHAR(20) DEFAULT 'todos'
                 CHECK (visible_para IN ('todos', 'profesor', 'alumno')),
    creado       TIMESTAMP DEFAULT NOW()
);

-- Usuario admin por defecto (password: admin123)
-- Hash generado con werkzeug.security.generate_password_hash('admin123')
INSERT INTO usuarios (nombre, email, password, rol)
VALUES (
    'Administrador',
    'admin@campus.com',
    'scrypt:32768:8:1$salt$hash_placeholder',
    'admin'
) ON CONFLICT (email) DO NOTHING;

-- Nota: reemplaza el hash anterior ejecutando en Python:
-- from werkzeug.security import generate_password_hash
-- print(generate_password_hash('admin123'))

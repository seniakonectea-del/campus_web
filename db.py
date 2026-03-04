import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config


def get_connection():
    """Devuelve una conexión a la base de datos PostgreSQL."""
    return psycopg2.connect(
        host=Config.DB_HOST,
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        port=Config.DB_PORT,
        cursor_factory=RealDictCursor
    )


def init_db():
    """Crea las tablas necesarias si no existen."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id       SERIAL PRIMARY KEY,
            nombre   VARCHAR(100) NOT NULL,
            email    VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            rol      VARCHAR(20)  NOT NULL DEFAULT 'alumno'
                     CHECK (rol IN ('administrador', 'profesor', 'alumno')),
            creado   TIMESTAMP DEFAULT NOW()
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS eventos (
            id          SERIAL PRIMARY KEY,
            titulo      VARCHAR(200) NOT NULL,
            descripcion TEXT,
            fecha_inicio TIMESTAMP NOT NULL,
            fecha_fin    TIMESTAMP,
            creado_por   INTEGER REFERENCES usuarios(id) ON DELETE SET NULL,
            visible_para VARCHAR(20) DEFAULT 'todos'
                         CHECK (visible_para IN ('todos', 'profesor', 'alumno')),
            creado       TIMESTAMP DEFAULT NOW()
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

from db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario:
    """Representa un usuario del sistema con sus operaciones CRUD."""

    def __init__(self, id, nombre, email, password, rol, creado=None):
        self.id       = id
        self.nombre   = nombre
        self.email    = email
        self.password = password
        self.rol      = rol
        self.creado   = creado

    # ── Propiedades de rol ──────────────────────────────────────────────────
    @property
    def es_admin(self):
        return self.rol == "admin"

    @property
    def es_profesor(self):
        return self.rol == "profesor"

    @property
    def es_alumno(self):
        return self.rol == "alumno"

    # ── Métodos de clase (factory / consultas) ──────────────────────────────
    @classmethod
    def crear(cls, nombre, email, password_plano, rol="alumno"):
        """Inserta un nuevo usuario y devuelve la instancia creada."""
        hash_pw = generate_password_hash(password_plano)
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(
            """INSERT INTO usuarios (nombre, email, password, rol)
               VALUES (%s, %s, %s, %s) RETURNING *""",
            (nombre, email, hash_pw, rol)
        )
        row = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return cls(**row)

    @classmethod
    def buscar_por_email(cls, email):
        """Devuelve un Usuario o None si no existe."""
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return cls(**row) if row else None

    @classmethod
    def buscar_por_id(cls, user_id):
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return cls(**row) if row else None

    @classmethod
    def listar_todos(cls):
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("SELECT * FROM usuarios ORDER BY creado DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [cls(**r) for r in rows]

    def actualizar(self, nombre=None, email=None, rol=None, password_plano=None):
        """Actualiza los campos indicados."""
        conn = get_connection()
        cur  = conn.cursor()
        if nombre:
            self.nombre = nombre
        if email:
            self.email = email
        if rol:
            self.rol = rol
        if password_plano:
            self.password = generate_password_hash(password_plano)

        cur.execute(
            """UPDATE usuarios SET nombre=%s, email=%s, rol=%s, password=%s
               WHERE id=%s""",
            (self.nombre, self.email, self.rol, self.password, self.id)
        )
        conn.commit()
        cur.close()
        conn.close()

    def eliminar(self):
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("DELETE FROM usuarios WHERE id = %s", (self.id,))
        conn.commit()
        cur.close()
        conn.close()

    def verificar_password(self, password_plano):
        return check_password_hash(self.password, password_plano)

    def to_dict(self):
        return {
            "id":     self.id,
            "nombre": self.nombre,
            "email":  self.email,
            "rol":    self.rol
        }

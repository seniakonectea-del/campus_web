from db import get_connection
from datetime import datetime


class Evento:
    """Representa un evento académico del calendario."""

    def __init__(self, id, titulo, descripcion, fecha_inicio,
                 fecha_fin=None, creado_por=None, visible_para="todos", creado=None):
        self.id           = id
        self.titulo       = titulo
        self.descripcion  = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin    = fecha_fin
        self.creado_por   = creado_por
        self.visible_para = visible_para
        self.creado       = creado

    # ── Métodos de clase ────────────────────────────────────────────────────
    @classmethod
    def crear(cls, titulo, descripcion, fecha_inicio, fecha_fin=None,
              creado_por=None, visible_para="todos"):
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(
            """INSERT INTO eventos (titulo, descripcion, fecha_inicio, fecha_fin,
                                    creado_por, visible_para)
               VALUES (%s, %s, %s, %s, %s, %s) RETURNING *""",
            (titulo, descripcion, fecha_inicio, fecha_fin, creado_por, visible_para)
        )
        row = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return cls(**row)

    @classmethod
    def buscar_por_id(cls, evento_id):
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("SELECT * FROM eventos WHERE id = %s", (evento_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return cls(**row) if row else None

    @classmethod
    def listar_todos(cls):
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("SELECT * FROM eventos ORDER BY fecha_inicio ASC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [cls(**r) for r in rows]
    

    @classmethod
    def listar_para_rol(cls, rol):
        """Devuelve eventos visibles para el rol dado."""
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(
            """SELECT * FROM eventos
               WHERE visible_para = 'todos' OR visible_para = %s
               ORDER BY fecha_inicio ASC""",
            (rol,)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [cls(**r) for r in rows]

    @classmethod
    def filtrar_por_fechas(cls, rol, desde=None, hasta=None):
        """Filtra eventos por rango de fechas para un rol dado (mejora personal)."""
        conn = get_connection()
        cur  = conn.cursor()

        query  = """SELECT * FROM eventos
                    WHERE (visible_para = 'todos' OR visible_para = %s)"""
        params = [rol]

        if desde:
            query  += " AND fecha_inicio >= %s"
            params.append(desde)
        if hasta:
            query  += " AND fecha_inicio <= %s"
            params.append(hasta)

        query += " ORDER BY fecha_inicio ASC"
        cur.execute(query, params)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [cls(**r) for r in rows]

    def actualizar(self, titulo=None, descripcion=None, fecha_inicio=None,
                   fecha_fin=None, visible_para=None):
        conn = get_connection()
        cur  = conn.cursor()
        if titulo:
            self.titulo = titulo
        if descripcion is not None:
            self.descripcion = descripcion
        if fecha_inicio:
            self.fecha_inicio = fecha_inicio
        if fecha_fin is not None:
            self.fecha_fin = fecha_fin
        if visible_para:
            self.visible_para = visible_para

        cur.execute(
            """UPDATE eventos SET titulo=%s, descripcion=%s, fecha_inicio=%s,
                                  fecha_fin=%s, visible_para=%s
               WHERE id=%s""",
            (self.titulo, self.descripcion, self.fecha_inicio,
             self.fecha_fin, self.visible_para, self.id)
        )
        conn.commit()
        cur.close()
        conn.close()

    def eliminar(self):
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("DELETE FROM eventos WHERE id = %s", (self.id,))
        conn.commit()
        cur.close()
        conn.close()

    def to_dict(self):
        return {
            "id":           self.id,
            "titulo":       self.titulo,
            "descripcion":  self.descripcion,
            "fecha_inicio": str(self.fecha_inicio),
            "fecha_fin":    str(self.fecha_fin) if self.fecha_fin else None,
            "visible_para": self.visible_para
        }

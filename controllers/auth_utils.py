from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    """Redirige al login si no hay sesión activa."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión primero.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


def rol_requerido(*roles):
    """Permite el acceso solo a los roles indicados."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if "user_id" not in session:
                flash("Debes iniciar sesión primero.", "warning")
                return redirect(url_for("auth.login"))
            if session.get("user_rol") not in roles:
                flash("No tienes permisos para acceder a esta sección.", "danger")
                return redirect(url_for("dashboard.index"))
            return f(*args, **kwargs)
        return decorated
    return decorator

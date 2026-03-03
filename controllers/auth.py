from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.usuario import Usuario

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard.index"))
    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        usuario = Usuario.buscar_por_email(email)
        if usuario and usuario.verificar_password(password):
            session["user_id"]     = usuario.id
            session["user_nombre"] = usuario.nombre
            session["user_rol"]    = usuario.rol
            flash(f"Bienvenido, {usuario.nombre}.", "success")
            return redirect(url_for("dashboard.index"))
        else:
            flash("Email o contraseña incorrectos.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if "user_id" in session:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        nombre   = request.form.get("nombre", "").strip()
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm_password", "")

        # Validaciones básicas
        if not nombre or not email or not password:
            flash("Todos los campos son obligatorios.", "danger")
            return render_template("auth/registro.html")

        if password != confirm:
            flash("Las contraseñas no coinciden.", "danger")
            return render_template("auth/registro.html")

        if len(password) < 6:
            flash("La contraseña debe tener al menos 6 caracteres.", "danger")
            return render_template("auth/registro.html")

        if Usuario.buscar_por_email(email):
            flash("Ya existe una cuenta con ese email.", "danger")
            return render_template("auth/registro.html")

        try:
            usuario = Usuario.crear(nombre, email, password, rol="alumno")
            session["user_id"]     = usuario.id
            session["user_nombre"] = usuario.nombre
            session["user_rol"]    = usuario.rol
            flash("Cuenta creada correctamente. ¡Bienvenido!", "success")
            return redirect(url_for("dashboard.index"))
        except Exception as e:
            flash("Error al crear la cuenta. Inténtalo de nuevo.", "danger")

    return render_template("auth/registro.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("auth.login"))

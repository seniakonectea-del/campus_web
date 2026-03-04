from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.auth_utils import rol_requerido
from models.usuario import Usuario

admin_bp = Blueprint("administrador", __name__, url_prefix="/admin")


@admin_bp.route("/usuarios")
@rol_requerido("administrador")
def usuarios():
    lista = Usuario.listar_todos()
    return render_template("administrador/usuarios.html", usuarios=lista)


@admin_bp.route("/usuarios/<int:user_id>/editar", methods=["GET", "POST"])
@rol_requerido("administrador")
def editar_usuario(user_id):
    usuario = Usuario.buscar_por_id(user_id)
    if not usuario:
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for("administrador.usuarios"))

    if request.method == "POST":
        nombre   = request.form.get("nombre", "").strip()
        email    = request.form.get("email", "").strip().lower()
        rol      = request.form.get("rol", "alumno")
        password = request.form.get("password", "").strip() or None

        if rol not in ("administrador", "profesor", "alumno"):
            flash("Rol no válido.", "danger")
            return render_template("administrador/editar_usuario.html", usuario=usuario)

        try:
            usuario.actualizar(nombre=nombre, email=email, rol=rol,
                               password_plano=password)
            flash("Usuario actualizado correctamente.", "success")
            return redirect(url_for("administrador.usuarios"))
        except Exception as e:
            flash(f"Error al actualizar: {e}", "danger")

    return render_template("administrador/editar_usuario.html", usuario=usuario)


@admin_bp.route("/usuarios/<int:user_id>/eliminar", methods=["POST"])
@rol_requerido("administrador")
def eliminar_usuario(user_id):
    usuario = Usuario.buscar_por_id(user_id)
    if usuario:
        usuario.eliminar()
        flash("Usuario eliminado correctamente.", "success")
    else:
        flash("Usuario no encontrado.", "danger")
    return redirect(url_for("administrador.usuarios"))

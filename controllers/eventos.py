from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from controllers.auth_utils import login_required, rol_requerido
from models.evento import Evento
from datetime import datetime

eventos_bp = Blueprint("eventos", __name__, url_prefix="/eventos")


@eventos_bp.route("/")
@login_required
def lista():
    rol   = session.get("user_rol")
    desde = request.args.get("desde", "")
    hasta = request.args.get("hasta", "")

    # Mejora personal: filtros por rango de fechas
    desde_dt = None
    hasta_dt = None
    try:
        if desde:
            desde_dt = datetime.strptime(desde, "%Y-%m-%d")
        if hasta:
            hasta_dt = datetime.strptime(hasta, "%Y-%m-%d")
    except ValueError:
        flash("Formato de fecha inválido. Usa AAAA-MM-DD.", "warning")

    eventos = Evento.filtrar_por_fechas(rol, desde_dt, hasta_dt)
    return render_template("eventos/lista.html", eventos=eventos,
                           desde=desde, hasta=hasta)


@eventos_bp.route("/nuevo", methods=["GET", "POST"])
@rol_requerido("admin", "profesor")
def nuevo():
    if request.method == "POST":
        titulo       = request.form.get("titulo", "").strip()
        descripcion  = request.form.get("descripcion", "").strip()
        fecha_inicio = request.form.get("fecha_inicio", "")
        fecha_fin    = request.form.get("fecha_fin", "") or None
        visible_para = request.form.get("visible_para", "todos")

        if not titulo or not fecha_inicio:
            flash("El título y la fecha de inicio son obligatorios.", "danger")
            return render_template("eventos/form.html", accion="Crear", evento=None)

        try:
            fi = datetime.strptime(fecha_inicio, "%Y-%m-%dT%H:%M")
            ff = datetime.strptime(fecha_fin,    "%Y-%m-%dT%H:%M") if fecha_fin else None
            Evento.crear(titulo, descripcion, fi, ff,
                         creado_por=session["user_id"],
                         visible_para=visible_para)
            flash("Evento creado correctamente.", "success")
            return redirect(url_for("eventos.lista"))
        except Exception as e:
            flash(f"Error al crear el evento: {e}", "danger")

    return render_template("eventos/form.html", accion="Crear", evento=None)


@eventos_bp.route("/<int:evento_id>/editar", methods=["GET", "POST"])
@rol_requerido("admin")
def editar(evento_id):
    evento = Evento.buscar_por_id(evento_id)
    if not evento:
        flash("Evento no encontrado.", "danger")
        return redirect(url_for("eventos.lista"))

    if request.method == "POST":
        titulo       = request.form.get("titulo", "").strip()
        descripcion  = request.form.get("descripcion", "").strip()
        fecha_inicio = request.form.get("fecha_inicio", "")
        fecha_fin    = request.form.get("fecha_fin", "") or None
        visible_para = request.form.get("visible_para", "todos")

        try:
            fi = datetime.strptime(fecha_inicio, "%Y-%m-%dT%H:%M")
            ff = datetime.strptime(fecha_fin,    "%Y-%m-%dT%H:%M") if fecha_fin else None
            evento.actualizar(titulo, descripcion, fi, ff, visible_para)
            flash("Evento actualizado correctamente.", "success")
            return redirect(url_for("eventos.lista"))
        except Exception as e:
            flash(f"Error al actualizar el evento: {e}", "danger")

    return render_template("eventos/form.html", accion="Editar", evento=evento)


@eventos_bp.route("/<int:evento_id>/eliminar", methods=["POST"])
@rol_requerido("admin")
def eliminar(evento_id):
    evento = Evento.buscar_por_id(evento_id)
    if evento:
        evento.eliminar()
        flash("Evento eliminado correctamente.", "success")
    else:
        flash("Evento no encontrado.", "danger")
    return redirect(url_for("eventos.lista"))

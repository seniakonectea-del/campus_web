from flask import Blueprint, render_template, session, redirect, url_for
from controllers.auth_utils import login_required
from models.evento import Evento

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def index():
    rol     = session.get("user_rol")
    eventos = Evento.listar_para_rol(rol)

    if rol == "administrador":
        return render_template("dashboard/admin.html", eventos=eventos)
    elif rol == "profesor":
        return render_template("dashboard/profesor.html", eventos=eventos)
    else:
        return render_template("dashboard/alumno.html", eventos=eventos)

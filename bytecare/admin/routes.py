"""Restricted admin authentication and dashboard routes."""

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from bytecare.admin import service
from bytecare.common.auth import admin_required
from bytecare.common.database import mongo_ready
from bytecare.infrastructure.supabase_auth import authenticate_admin
from flask import current_app

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin/login", methods=["GET", "POST"])
def login():
    if admin_required():
        return redirect(url_for("admin.dashboard"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not email or not password:
            flash("Informe seu e-mail e sua senha.", "error")
        else:
            try:
                user = authenticate_admin(email, password)
                session.clear()
                session["admin_user_id"] = user.id
                session["admin_email"] = user.email or email
                return redirect(url_for("admin.dashboard"))
            except RuntimeError:
                flash("Configure SUPABASE_URL e SUPABASE_KEY para habilitar o acesso administrativo.", "error")
            except Exception:

                current_app.logger.warning("Falha na autenticação do painel administrativo.")
                flash("Não foi possível entrar. Confira suas credenciais e tente novamente.", "error")
    return render_template("admin_login.html")


@admin_bp.get("/admin")
def dashboard():
    if not admin_required():
        return redirect(url_for("admin.login"))
    if mongo_ready():
        services, orders, part_count, redis_online = service.dashboard_data()
    else:
        services, orders, part_count, redis_online = [], [], 0, False
    return render_template("admin.html", services=services, orders=orders,
                           part_count=part_count, redis_online=redis_online)


@admin_bp.post("/admin/servicos")
def save_service():
    if not admin_required():
        return redirect(url_for("admin.login"))
    try:
        service.save_service(request.form)
        flash("Serviço salvo no MongoDB.", "success")
    except service.AdminValidationError as error:
        flash(str(error), "error")
    return redirect(url_for("admin.dashboard") + "#catalogo")


@admin_bp.post("/admin/servicos/<sid>/excluir")
def delete_service(sid):
    if not admin_required():
        return redirect(url_for("admin.login"))
    try:
        service.delete_service(sid)
        flash("Serviço excluído.", "success")
    except service.AdminValidationError as error:
        flash(str(error), "error")
    return redirect(url_for("admin.dashboard") + "#catalogo")


@admin_bp.post("/admin/pedidos/<oid>/status")
def update_order_status(oid):
    if not admin_required():
        return redirect(url_for("admin.login"))
    try:
        service.update_order_status(oid, request.form.get("status", ""))
        flash("Status do pedido atualizado.", "success")
    except service.AdminValidationError as error:
        flash(str(error), "error")
    return redirect(url_for("admin.dashboard") + "#pedidos")


@admin_bp.post("/admin/sair")
def logout():
    session.clear()
    return redirect(url_for("storefront.home"))

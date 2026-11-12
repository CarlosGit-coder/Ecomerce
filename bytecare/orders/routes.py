"""Public order API and order tracking page."""

from flask import Blueprint, flash, jsonify, render_template, request

from bytecare.common.database import mongo_ready
from bytecare.orders import repository, service

orders_bp = Blueprint("orders", __name__)


@orders_bp.get("/api/cep/<cep>")
def quote_cep(cep):
    try:
        digits, address, fee = service.quote_cep(cep)
        return jsonify(cep=digits, address=address, pickup_fee=fee)
    except service.OrderValidationError as error:
        return jsonify(error=str(error)), error.status


@orders_bp.post("/api/pedidos")
def create_order():
    if not mongo_ready():
        return jsonify(error="Banco de dados indisponível. Confira a conexão com o MongoDB."), 503
    try:
        result = service.create_order(request.get_json(silent=True) or {})
        return jsonify(**result), 201
    except service.OrderValidationError as error:
        return jsonify(error=str(error)), error.status


@orders_bp.route("/acompanhar", methods=["GET", "POST"])
def track_order():
    result = None
    if request.method == "POST":
        code = request.form.get("code", "").strip().upper()
        result = repository.find_order_by_code(code) if mongo_ready() and code else None
        if not result:
            flash("Não encontramos um pedido com esse código.", "error")
    return render_template("track.html", order=result)

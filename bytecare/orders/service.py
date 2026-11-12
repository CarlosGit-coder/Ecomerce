"""Order creation, address lookup, shipping estimate, and WhatsApp message."""

import json
import re
import secrets
import urllib.parse
import urllib.request
from datetime import datetime, timezone

from bson import ObjectId
from flask import current_app

from bytecare.catalog import repository as catalog_repository
from bytecare.extensions import get_redis
from bytecare.orders import repository as order_repository


class OrderValidationError(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status


def pickup_fee_for_uf(uf):
    """Demo estimate from the ByteCare origin in Teresina, PI."""
    rates = {"PI": 14.90, "MA": 24.90, "CE": 24.90, "PE": 29.90,
             "AL": 34.90, "PB": 34.90, "RN": 34.90, "SE": 39.90, "BA": 39.90}
    return rates.get(str(uf).upper(), 59.90)


def lookup_cep(cep):
    digits = re.sub(r"\D", "", str(cep))
    if len(digits) != 8:
        raise OrderValidationError("Informe um CEP válido com 8 dígitos.")
    try:
        with urllib.request.urlopen(f"https://viacep.com.br/ws/{digits}/json/", timeout=4) as response:
            address = json.loads(response.read().decode())
    except Exception as error:
        raise OrderValidationError("Não foi possível consultar o CEP. Tente novamente.", 503) from error
    if address.get("erro"):
        raise OrderValidationError("CEP não encontrado.", 404)
    normalized = {key: address.get(key, "") for key in ("logradouro", "bairro", "localidade", "uf")}
    return digits, normalized


def quote_cep(cep):
    digits, address = lookup_cep(cep)
    return digits, address, round(pickup_fee_for_uf(address["uf"]), 2)


def _service_items(raw_items):
    if not isinstance(raw_items, list) or not raw_items or len(raw_items) > 20:
        raise OrderValidationError("Adicione ao menos um serviço ao carrinho (limite de 20).")
    quantities = {}
    try:
        for item in raw_items:
            service_id = str(item.get("id", ""))
            quantity = int(item.get("quantity", 0))
            ObjectId(service_id)
            if quantity < 1 or quantity > 20:
                raise ValueError
            quantities[service_id] = quantities.get(service_id, 0) + quantity
        if any(quantity > 20 for quantity in quantities.values()):
            raise ValueError
        found = catalog_repository.find_active_services([ObjectId(value) for value in quantities])
    except Exception as error:
        raise OrderValidationError("Revise os itens e quantidades do carrinho.") from error
    by_id = {str(item["_id"]): item for item in found}
    if len(by_id) != len(quantities):
        raise OrderValidationError("Um serviço do carrinho não está mais disponível. Atualize a loja.", 404)
    snapshot = [{"id": by_id[sid]["_id"], "name": by_id[sid]["name"],
                 "price": float(by_id[sid]["price"]), "quantity": quantity,
                 "subtotal": round(float(by_id[sid]["price"]) * quantity, 2)}
                for sid, quantity in quantities.items()]
    return by_id, snapshot


def _parts_snapshot(chosen_parts, is_assembly):
    if not isinstance(chosen_parts, list) or len(chosen_parts) > 12:
        raise OrderValidationError("Revise as peças selecionadas.")
    if chosen_parts and not is_assembly:
        raise OrderValidationError("Peças cobradas estão disponíveis nos serviços de montagem.")
    if not chosen_parts:
        return []
    ids = list(dict.fromkeys(str(item.get("id", "")) for item in chosen_parts if isinstance(item, dict)))
    try:
        selected = catalog_repository.active_parts_by_ids([ObjectId(value) for value in ids])
    except Exception as error:
        raise OrderValidationError("Revise as peças selecionadas.") from error
    by_id = {str(item["_id"]): item for item in selected}
    if len(by_id) != len(ids) or len(ids) != len(chosen_parts):
        raise OrderValidationError("Uma das peças selecionadas não está disponível. Pesquise novamente.")
    categories = [by_id[value]["category"] for value in ids]
    if len(categories) != len(set(categories)):
        raise OrderValidationError("Selecione no máximo uma peça de cada categoria.")
    return [{"id": by_id[value]["_id"], "name": by_id[value]["name"],
             "category": by_id[value]["category"], "price": float(by_id[value]["price"])}
            for value in ids]


def _brl(value):
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _whatsapp_url(order):
    lines = [f"{item['quantity']}x {item['name']} — R$ {_brl(item['subtotal'])}" for item in order["items"]]
    lines.extend(f"Peça para montagem: {item['name']} — R$ {_brl(item['price'])}" for item in order["parts"])
    owned_parts = order["existing_parts"]
    address = order["address"]
    full_address = ", ".join(value for value in (address["logradouro"], address["bairro"], address["localidade"], address["uf"]) if value)
    delivery = "Retirada no endereço" if order["fulfillment"] == "pickup" else "Entrega no ponto ByteCare"
    lines.extend([
        f"Computador/peças atuais: {order['computer_spec'] or 'Não informado'}",
        f"Peças informadas: {', '.join(owned_parts) or 'Não informado'}",
        f"CEP/endereço: {order['cep']} · {full_address}",
        f"Forma de entrega: {delivery}", f"Coleta: R$ {_brl(order['pickup_fee'])}",
        f"Observações: {order['notes'] or 'Nenhuma'}", f"Total: R$ {_brl(order['total'])}",
        f"Pedido ByteCare: {order['code']}",
    ])
    number = re.sub(r"\D", "", current_app.config["WHATSAPP_NUMBER"])
    if not 10 <= len(number) <= 15:
        number = "5586988166764"
    message = "Olá, gostaria de solicitar:\n" + "\n".join(lines)
    return f"https://wa.me/{number}?text={urllib.parse.quote(message)}"


def create_order(data):
    required = ["name", "email", "phone", "fulfillment", "cep"]
    if any(not str(data.get(key, "")).strip() for key in required):
        raise OrderValidationError("Preencha seus dados, escolha serviços e informe o CEP.")
    if data["fulfillment"] not in ("dropoff", "pickup"):
        raise OrderValidationError("Escolha entrega no ponto de atendimento ou retirada.")
    services_by_id, items = _service_items(data.get("items", []))
    digits, address = lookup_cep(data["cep"])
    pickup_fee = pickup_fee_for_uf(address["uf"]) if data["fulfillment"] == "pickup" else 0
    is_assembly = any(bool(services_by_id[sid].get("assembly")) for sid in services_by_id)
    parts = _parts_snapshot(data.get("parts", []), is_assembly)
    existing_parts = data.get("existing_parts", [])
    if not isinstance(existing_parts, list):
        raise OrderValidationError("Revise a lista de peças que você já possui.")
    service_total = round(sum(item["subtotal"] for item in items), 2)
    parts_total = round(sum(item["price"] for item in parts), 2)
    code = secrets.token_hex(3).upper()
    computer_spec = str(data.get("computer_spec", "")).strip()[:500]
    order = {
        "code": code,
        "customer": {"name": data["name"].strip(), "email": data["email"].strip().lower(), "phone": data["phone"].strip()},
        "service": {"id": items[0]["id"], "name": items[0]["name"], "price": items[0]["price"]},
        "items": items, "services_total": service_total, "parts": parts,
        "computer_spec": computer_spec,
        "existing_parts": [str(item)[:120] for item in existing_parts if isinstance(item, str)][:12],
        "parts_total": parts_total, "assembly": is_assembly,
        "fulfillment": data["fulfillment"], "cep": digits, "address": address,
        "pickup_fee": pickup_fee, "total": round(service_total + parts_total + pickup_fee, 2),
        "notes": str(data.get("notes", "")).strip()[:1000],
        "status": "Recebido", "created_at": datetime.now(timezone.utc),
    }
    order_repository.insert_order(order)
    try:
        redis_client = get_redis()
        for item in items:
            redis_client.zincrby("bytecare:popular_services", item["quantity"], item["name"])
    except Exception:
        pass
    return {"code": code, "total": order["total"], "whatsapp_url": _whatsapp_url(order)}

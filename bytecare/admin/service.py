"""Administrative use cases for authentication, catalog, and orders."""

from datetime import datetime, timezone

from bytecare.catalog import repository as catalog_repository
from bytecare.catalog import service as catalog_service
from bytecare.extensions import get_redis
from bytecare.orders import repository as order_repository


class AdminValidationError(Exception):
    pass


ORDER_STATUSES = ("Recebido", "Em análise", "Aguardando aprovação", "Em manutenção", "Pronto", "Concluído", "Cancelado")


def dashboard_data():
    catalog_service.ensure_catalog_seeded()
    catalog_service.ensure_parts_seeded()
    all_services = list(catalog_repository.services_collection().find().sort("name", 1))
    recent_orders = order_repository.recent_orders()
    part_count = catalog_repository.parts_collection().count_documents({"active": True})
    try:
        redis_online = bool(get_redis().ping())
    except Exception:
        redis_online = False
    return all_services, recent_orders, part_count, redis_online


def save_service(form):
    try:
        price = float(form.get("price", "0").replace(",", "."))
    except ValueError as error:
        raise AdminValidationError("Informe um preço válido.") from error
    name = form.get("name", "").strip()
    if not name or price < 0:
        raise AdminValidationError("Informe um nome e um preço válido.")
    image_url = form.get("image_url", "").strip()
    if image_url and not image_url.startswith(("https://", "http://")):
        raise AdminValidationError("A imagem precisa usar uma URL http:// ou https://.")
    category = form.get("category", "Geral").strip() or "Geral"
    description = form.get("description", "").strip()
    document = {
        "name": name, "nome": name, "category": category, "categoria": category,
        "description": description, "descricao": description,
        "price": price, "preco": price, "image_url": image_url, "imagem_url": image_url,
        "duration": form.get("duration", "A combinar").strip(),
        "icon": form.get("icon", "✦").strip()[:4],
        "featured": form.get("featured") == "on", "active": form.get("active") == "on",
        "assembly": form.get("assembly") == "on", "updated_at": datetime.now(timezone.utc),
    }
    service_id = form.get("id", "")
    try:
        if service_id:
            result = catalog_repository.save_service_document(document, service_id)
            if not result.matched_count:
                raise AdminValidationError("Serviço não encontrado.")
        else:
            document["created_at"] = datetime.now(timezone.utc)
            catalog_repository.save_service_document(document)
    except AdminValidationError:
        raise
    except Exception as error:
        raise AdminValidationError("Não foi possível salvar o serviço. Confira os dados.") from error
    catalog_service.invalidate_catalog_cache()


def delete_service(service_id):
    try:
        catalog_repository.delete_service_document(service_id)
    except Exception as error:
        raise AdminValidationError("Serviço inválido.") from error
    catalog_service.invalidate_catalog_cache()


def update_order_status(order_id, status):
    if status not in ORDER_STATUSES:
        raise AdminValidationError("Status de pedido inválido.")
    try:
        result = order_repository.update_order_status(order_id, status)
        if not result.matched_count:
            raise AdminValidationError("Pedido não encontrado.")
    except AdminValidationError:
        raise
    except Exception as error:
        raise AdminValidationError("Pedido inválido.") from error

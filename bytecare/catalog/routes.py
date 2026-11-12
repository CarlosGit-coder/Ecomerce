"""Public catalog and component-search routes."""

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for

from bytecare.catalog import repository
from bytecare.catalog import service as catalog_service
from bytecare.common.database import mongo_ready

storefront_bp = Blueprint("storefront", __name__)
catalog_api_bp = Blueprint("catalog_api", __name__)


@storefront_bp.get("/")
def home():
    if mongo_ready():
        catalog_service.ensure_catalog_seeded()
        categories = repository.service_categories()
        listing, cache_status = catalog_service.get_service_list(
            request.args.get("q", "").strip(), request.args.get("categoria", "")
        )
        featured = repository.featured_services()
        popular = catalog_service.get_popular_services(repository.recommended_services())
        catalog_service.ensure_parts_seeded()
        part_categories = repository.part_categories()
        recently_viewed = catalog_service.get_recently_viewed()
    else:
        categories, listing, featured, popular, part_categories, recently_viewed = [], [], [], [], [], []
        cache_status = "OFFLINE"
    return render_template(
        "index.html", services=listing, featured=featured, categories=categories,
        popular=popular, part_categories=part_categories, recently_viewed=recently_viewed,
        catalog_cache_status=cache_status, search=request.args.get("q", ""),
        selected_category=request.args.get("categoria", ""),
    )


@storefront_bp.get("/servicos/<sid>")
def service_detail(sid):
    if not mongo_ready():
        return redirect(url_for("storefront.home"))
    catalog_service.ensure_catalog_seeded()
    try:
        item = repository.find_service(sid)
    except Exception:
        item = None
    if not item:
        flash("Este serviço não está disponível.", "error")
        return redirect(url_for("storefront.home"))
    catalog_service.record_recent_view(item["_id"])
    return render_template("service_detail.html", service=item)


@catalog_api_bp.get("/api/pecas")
def search_parts():
    if not mongo_ready():
        return jsonify(error="Catálogo de peças indisponível."), 503
    catalog_service.ensure_parts_seeded()
    term = request.args.get("q", "").strip()
    category = request.args.get("categoria", "").strip()
    if len(term) < 2 and not category:
        return jsonify(items=[])
    result = repository.search_parts(term, category)
    return jsonify(items=[{"id": str(item["_id"]), "name": item["name"],
                          "category": item["category"], "price": item["price"]} for item in result])

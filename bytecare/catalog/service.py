"""Catalog use cases and Redis cache/recent-view adapters."""

import json
import secrets
from datetime import datetime, timezone
from hashlib import sha256

from bson import ObjectId
from flask import current_app, session

from bytecare.catalog import repository
from bytecare.extensions import get_redis


RECENT_VIEWS_TTL_SECONDS = 30 * 24 * 60 * 60


def invalidate_catalog_cache():
    client = get_redis()
    if not client:
        return
    try:
        keys = list(client.scan_iter(match="bytecare:catalog:*", count=100))
        if keys:
            client.delete(*keys)
    except Exception:
        current_app.logger.exception("Falha ao invalidar o cache do catálogo no Redis.")


def ensure_catalog_seeded():
    if repository.seed_services():
        invalidate_catalog_cache()


def ensure_parts_seeded():
    repository.seed_parts()


def get_service_list(search="", category=""):
    cache_identity = json.dumps([search.casefold().strip(), category.strip()], ensure_ascii=False, separators=(",", ":"))
    cache_key = "bytecare:catalog:" + sha256(cache_identity.encode("utf-8")).hexdigest()
    client = get_redis()
    if client:
        try:
            cached = client.get(cache_key)
            if cached:
                result = json.loads(cached)
                for item in result:
                    item["_id"] = ObjectId(item["_id"])
                current_app.logger.info("Catálogo Redis HIT (q=%r, categoria=%r)", search, category)
                return result, "HIT"
        except Exception:
            current_app.logger.exception("Falha ao ler cache do catálogo; consultando MongoDB.")
    result = repository.list_services_from_mongo(search, category)
    if client:
        try:
            payload = [{**item, "_id": str(item["_id"])} for item in result]
            client.setex(cache_key, current_app.config["REDIS_CATALOG_TTL"], json.dumps(payload, ensure_ascii=False, default=str))
            current_app.logger.info("Catálogo Redis MISS / MongoDB (q=%r, categoria=%r)", search, category)
            return result, "MISS"
        except Exception:
            current_app.logger.exception("Falha ao gravar cache do catálogo no Redis.")
    current_app.logger.info("Catálogo Redis BYPASS / MongoDB (Redis indisponível)")
    return result, "BYPASS"


def get_popular_services(fallback):
    client = get_redis()
    try:
        names = client.zrevrange("bytecare:popular_services", 0, 3)
        if names:
            found = {item["name"]: item for item in repository.services_collection().find({"name": {"$in": names}, "active": True})}
            result = [found[name] for name in names if name in found]
            if result:
                for item in result:
                    item["_order_count"] = int(client.zscore("bytecare:popular_services", item["name"]) or 0)
                return result
    except Exception:
        pass
    for item in fallback[:4]:
        item["_order_count"] = 0
    return fallback[:4]


def record_recent_view(service_id):
    client = get_redis()
    if not client:
        return
    try:
        key = f"bytecare:recently_viewed:{visitor_id()}"
        client.zadd(key, {str(service_id): datetime.now(timezone.utc).timestamp()})
        client.zremrangebyrank(key, 0, -9)
        client.expire(key, RECENT_VIEWS_TTL_SECONDS)
    except Exception:
        current_app.logger.exception("Falha ao registrar serviço visualizado no Redis.")


def get_recently_viewed(limit=6):
    client = get_redis()
    if not client or "visitor_id" not in session:
        return []
    try:
        ids = client.zrevrange(f"bytecare:recently_viewed:{session['visitor_id']}", 0, limit - 1)
        valid_ids = [ObjectId(value) for value in ids if ObjectId.is_valid(value)]
        found = {str(item["_id"]): item for item in repository.services_collection().find({"_id": {"$in": valid_ids}, "active": True})}
        return [found[value] for value in ids if value in found]
    except Exception:
        current_app.logger.exception("Falha ao consultar histórico recente no Redis.")
        return []


def visitor_id():
    if "visitor_id" not in session:
        session["visitor_id"] = secrets.token_urlsafe(18)
    session.permanent = True
    return session["visitor_id"]

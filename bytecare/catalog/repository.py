"""MongoDB persistence for the service catalog and assembly parts."""

import re
from datetime import datetime, timezone

from bson import ObjectId
from pymongo import ASCENDING, DESCENDING, UpdateOne

from bytecare.data.catalog_seed import STARTER_PARTS, STARTER_SERVICES
from bytecare.extensions import get_db
from flask import current_app

def services_collection():
    return get_db().services


def parts_collection():
    return get_db().parts


def seed_services():
    """Insert starter services once per process while preserving existing data."""


    if current_app.extensions.get("bytecare_services_seeded"):
        return False
    now = datetime.now(timezone.utc)
    services_collection().bulk_write(
        [UpdateOne({"name": item["name"]}, {"$setOnInsert": {**item, "created_at": now, "updated_at": now}}, upsert=True)
         for item in STARTER_SERVICES], ordered=False,
    )
    services_collection().update_many({}, [{"$set": {
        "nome": "$name", "descricao": "$description", "preco": "$price",
        "categoria": "$category", "imagem_url": {"$ifNull": ["$imagem_url", ""]},
    }}])
    services_collection().update_many(
        {"name": {"$in": ["Montagem de PC", "Montagem de setup gamer"]}},
        {"$set": {"assembly": True}},
    )
    current_app.extensions["bytecare_services_seeded"] = True
    return True


def seed_parts():

    if current_app.extensions.get("bytecare_parts_seeded"):
        return
    now = datetime.now(timezone.utc)
    parts_collection().bulk_write(
        [UpdateOne({"name": item["name"]}, {"$setOnInsert": {**item, "created_at": now}}, upsert=True)
         for item in STARTER_PARTS], ordered=False,
    )
    current_app.extensions["bytecare_parts_seeded"] = True


def list_services_from_mongo(search="", category=""):
    query = {"active": True}
    if category:
        query["category"] = category
    if search:
        pattern = re.escape(search)
        query["$or"] = [
            {"name": {"$regex": pattern, "$options": "i"}},
            {"description": {"$regex": pattern, "$options": "i"}},
            {"category": {"$regex": pattern, "$options": "i"}},
        ]
    return list(services_collection().find(query).sort([("featured", DESCENDING), ("name", ASCENDING)]))


def service_categories():
    return sorted(services_collection().distinct("category", {"active": True}))


def featured_services(limit=3):
    return list(services_collection().find({"active": True, "featured": True}).sort("name", ASCENDING).limit(limit))


def recommended_services(limit=4):
    return list(services_collection().find({"active": True}).sort("featured", DESCENDING).limit(limit))


def find_service(service_id, active_only=True):
    query = {"_id": ObjectId(service_id)}
    if active_only:
        query["active"] = True
    return services_collection().find_one(query)


def find_active_services(service_ids):
    return list(services_collection().find({"_id": {"$in": service_ids}, "active": True}))


def search_parts(term="", category=""):
    query = {"active": True}
    if category:
        query["category"] = category
    if term:
        query["name"] = {"$regex": re.escape(term), "$options": "i"}
    return list(parts_collection().find(query, {"name": 1, "category": 1, "price": 1}).sort("name", ASCENDING).limit(15))


def part_categories():
    return sorted(parts_collection().distinct("category", {"active": True}))


def active_parts_by_ids(ids):
    return list(parts_collection().find({"_id": {"$in": ids}, "active": True}))


def save_service_document(document, service_id=""):
    if service_id:
        return services_collection().update_one({"_id": ObjectId(service_id)}, {"$set": document})
    return services_collection().insert_one(document)


def delete_service_document(service_id):
    return services_collection().delete_one({"_id": ObjectId(service_id)})

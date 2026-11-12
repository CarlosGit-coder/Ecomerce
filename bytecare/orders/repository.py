"""MongoDB persistence for customer service orders."""

from pymongo import DESCENDING

from bytecare.extensions import get_db


def insert_order(document):
    return get_db().orders.insert_one(document)


def find_order_by_code(code):
    return get_db().orders.find_one({"code": code})


def recent_orders(limit=12):
    return list(get_db().orders.find().sort("created_at", DESCENDING).limit(limit))


def update_order_status(order_id, status):
    from bson import ObjectId

    return get_db().orders.update_one({"_id": ObjectId(order_id)}, {"$set": {"status": status}})

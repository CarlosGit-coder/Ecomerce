"""Adapters initialized once per Flask application instance."""

import redis
from flask import current_app
from pymongo import MongoClient


def init_extensions(app):
    if not app.config["MONGO_URI"]:
        raise RuntimeError(
            "MONGO_URI não configurada. Defina a connection string do MongoDB Atlas no arquivo .env."
        )
    mongo_client = MongoClient(app.config["MONGO_URI"], serverSelectionTimeoutMS=2500)
    app.extensions["mongo_client"] = mongo_client
    app.extensions["mongo_db"] = mongo_client[app.config["MONGO_DB"]]
    app.extensions["redis_client"] = redis.Redis.from_url(
        app.config["REDIS_URL"], socket_connect_timeout=1, socket_timeout=1,
        decode_responses=True,
    )


def get_mongo_client():
    return current_app.extensions["mongo_client"]


def get_db():
    return current_app.extensions["mongo_db"]


def get_redis():
    return current_app.extensions.get("redis_client")

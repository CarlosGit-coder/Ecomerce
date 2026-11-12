"""Shared health checks for persistence adapters."""

from pymongo.errors import PyMongoError
from flask import current_app, g

from bytecare.extensions import get_mongo_client


def mongo_ready():
    # Several layers can check availability during one request (route,
    # template context processor, etc.). Reuse the result to avoid duplicate
    # Atlas pings and repeated timeout warnings for the same page load.
    if hasattr(g, "mongo_ready"):
        return g.mongo_ready

    try:
        get_mongo_client().admin.command("ping")
        g.mongo_ready = True
    except PyMongoError as exc:
        # PyMongo's server-selection message contains node-level causes
        # (for example TLS reset or DNS failure), but not the connection URI.
        current_app.logger.warning("Falha ao verificar conexão com MongoDB: %s", exc)
        g.mongo_ready = False
    return g.mongo_ready

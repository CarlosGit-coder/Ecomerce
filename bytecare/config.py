"""Application settings loaded from environment variables."""

import os
from datetime import timedelta

from dotenv import load_dotenv

# Load local configuration for direct runs such as ``python app.py``.
load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "bytecare-chave-local")
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    MONGO_URI = os.getenv("MONGO_URI", "").strip()
    MONGO_DB = os.getenv("MONGO_DB", "Ecomerce")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REDIS_CATALOG_TTL = max(30, int(os.getenv("CATALOG_CACHE_TTL_SECONDS", "300")))
    SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "").strip()
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "5586988166764")

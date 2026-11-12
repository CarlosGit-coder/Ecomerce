"""Supabase Auth adapter used by the administrative area."""

from flask import current_app
from supabase import create_client


def authenticate_admin(email, password):
    url = current_app.config["SUPABASE_URL"]
    key = current_app.config["SUPABASE_KEY"]
    if not url or not key:
        raise RuntimeError("Supabase não está configurado.")
    result = create_client(url, key).auth.sign_in_with_password(
        {"email": email, "password": password}
    )
    if not result.user:
        raise ValueError("Supabase não retornou um usuário autenticado.")
    return result.user

"""Session-level authorization helpers."""

from flask import session


def admin_required():
    return bool(session.get("admin_user_id"))

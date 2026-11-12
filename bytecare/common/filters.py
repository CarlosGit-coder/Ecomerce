"""Jinja formatting helpers."""


def money(value):
    return f"R$ {float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def date_br(value):
    return value.astimezone().strftime("%d/%m/%Y às %H:%M") if value else "—"

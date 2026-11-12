"""Compatibility entry point for ``python app.py`` and ``gunicorn app:app``."""

import os

from bytecare import create_app

app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=os.getenv("FLASK_DEBUG") == "1")

"""ByteCare modular Flask application factory."""

from flask import Flask

from bytecare.common.database import mongo_ready
from bytecare.common.filters import date_br, money
from bytecare.config import Config
from bytecare.extensions import init_extensions

from bytecare.admin.routes import admin_bp
from bytecare.catalog.routes import catalog_api_bp, storefront_bp
from bytecare.orders.routes import orders_bp

def create_app(config_object=Config):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(config_object)
    app.logger.setLevel(app.config["LOG_LEVEL"])
    init_extensions(app)

    app.register_blueprint(storefront_bp)
    app.register_blueprint(catalog_api_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(admin_bp)
    app.add_template_filter(money, "money")
    app.add_template_filter(date_br, "date_br")

    @app.context_processor
    def inject_status():
        return {"db_online": mongo_ready()}

    return app

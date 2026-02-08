from app.blueprints.admin import admin_bp
from app.blueprints.main import main_bp


def register_routes(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

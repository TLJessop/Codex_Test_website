from flask import Flask

from app.models import db
from app.routes import register_routes


def create_app(config_object="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    register_routes(app)

    return app

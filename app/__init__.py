from flask import Flask

from app.routes import register_routes


def create_app(config_object="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    register_routes(app)

    return app

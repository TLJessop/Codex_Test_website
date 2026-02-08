from flask import Flask

from app.models import User, db
from app.routes import register_routes


def create_app(config_object="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    with app.app_context():
        db.create_all()
        admin_username = app.config.get("ADMIN_USERNAME")
        admin_password = app.config.get("ADMIN_PASSWORD")
        if admin_username and admin_password:
            existing_admin = User.query.filter_by(username=admin_username).first()
            if not existing_admin:
                admin_user = User(username=admin_username)
                admin_user.set_password(admin_password)
                db.session.add(admin_user)
                db.session.commit()

    register_routes(app)

    return app

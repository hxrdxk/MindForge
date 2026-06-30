from datetime import datetime

from flask import Flask

from config import Config
from extensions import db, migrate


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from routes.main import main_bp
    app.register_blueprint(main_bp)

    @app.context_processor
    def inject_brand():
        return {
            "brand": {
                "name": app.config["PROJECT_NAME"],
                "tagline": app.config["PROJECT_TAGLINE"],
                "description": app.config["PROJECT_DESCRIPTION"],
                "author": app.config["PROJECT_AUTHOR"],
                "logo": app.config["LOGO_PATH"],
                "favicon": app.config["FAVICON"],
            },
            "current_year": datetime.now().year,
        }

    return app
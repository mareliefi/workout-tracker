# app/__init__.py

import os
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from .models import db
from .views import api_bp

load_dotenv()

def create_app(config_class=None):
    app = Flask(__name__)

    # If a config_class is provided, use it, otherwise fall back to environment variables
    if config_class:
        app.config.from_object(config_class)
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = (
            os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "False") == "True"
        )
        app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    db.init_app(app)
    Migrate(app, db)

    # Register the API blueprint with the prefix "/api"
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.route("/")
    def index():
        return "Workout Tracker API is running."

    return app



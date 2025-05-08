# app/__init__.py

import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate

from app.models import db
from app.views import api_bp

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = (
        os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "False") == "True"
    )
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(api_bp, url_prefix="/v1")

    @app.route("/")
    def index():
        return "Workout Tracker API is running."

    return app

from flask import Flask
from flask_migrate import Migrate
from models import db
from dotenv import load_dotenv
import os

load_dotenv()  # Load from .env


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = (
        os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "False") == "True"
    )

    db.init_app(app)
    migrate = Migrate(app, db)

    @app.route("/")
    def index():
        return "Workout Tracker API"

    return app

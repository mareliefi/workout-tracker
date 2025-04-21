import os
from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from models import db
from views import api_bp

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = (
        os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "False") == "True"
    )
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(api_bp, url_prefix="/v1")

    @app.route("/")
    def index():
        return "Workout Tracker API is running."

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

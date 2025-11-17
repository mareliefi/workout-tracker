# app/__init__.py
import os
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
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
    
    # Enable CORS for both local development and Docker
    CORS(app, 
         origins=[
             'http://localhost:3000',      # Local React dev server
             'http://frontend:3000',       # Docker frontend service (dev mode)
             'http://127.0.0.1:3000',      # Alternative localhost
             'http://localhost:80',        # Docker Nginx (production)
             'http://frontend:80'          # Docker frontend service (production)
         ],
         supports_credentials=True)
    
    db.init_app(app)
    Migrate(app, db)
    
    # Register the API blueprint with the prefix "/api"
    app.register_blueprint(api_bp, url_prefix="/api")
    
    @app.route("/")
    def index():
        return "Workout Tracker API is running."
    
    return app

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
    
    if config_class:
        app.config.from_object(config_class)
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = (
            os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "False") == "True"
        )
        app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    
    # Enhanced CORS for both cookie and header-based auth
    CORS(app, 
         origins=[
             'http://localhost:3000',
             'http://frontend:3000',
             'http://127.0.0.1:3000',
             'http://localhost:80',
             'http://frontend:80'
         ],
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'],
         expose_headers=['Content-Type', 'Authorization', 'Set-Cookie'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'])
    
    db.init_app(app)
    Migrate(app, db)
    
    app.register_blueprint(api_bp, url_prefix="/api")
    
    @app.route("/")
    def index():
        return "Workout Tracker API is running."
    
    return app

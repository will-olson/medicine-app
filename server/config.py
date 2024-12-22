import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()

db = SQLAlchemy()

migrate = Migrate()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    DEBUG = os.getenv("DEBUG", True)

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    RXNORM_API_BASE_URL = "https://rxnav.nlm.nih.gov/REST"
    PRESCRIBABLE_API_BASE_URL = "https://rxnav.nlm.nih.gov/REST"
    RXCLASS_API_BASE_URL = "https://rxnav.nlm.nih.gov/REST"

    OPENFDA_API_BASE_URL = "https://api.fda.gov"
    OPENFDA_API_KEY = os.getenv("OPENFDA_API_KEY")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    
    db.init_app(app)

    
    migrate.init_app(app, db)

    return app

from flask import Flask
from flask_migrate import Migrate
from .config import Config
from .models import db
from .routes import api_bp # Import the Blueprint

migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db) # Initialize Flask-Migrate

    # Register Blueprints
    app.register_blueprint(api_bp) # Register the API blueprint

    # Optional: Create DB tables if they don't exist within app context
    # Note: Migrations are the preferred way to manage schema
    # with app.app_context():
    #     db.create_all() # Generally avoid this after initial setup; use migrations

    return app

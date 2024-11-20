from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')  # Adjust configuration as needed

    db.init_app(app)

    # Register Blueprints
    from .routes import main
    app.register_blueprint(main)

    return app

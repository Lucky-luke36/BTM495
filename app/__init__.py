from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .routes import login

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    # Register Blueprints
    from .routes import events, speakers, venues, time_slots
    app.register_blueprint(login.bp)
    app.register_blueprint(events.bp)
    app.register_blueprint(speakers.bp)
    app.register_blueprint(venues.bp)
    app.register_blueprint(time_slots.bp)

    with app.app_context():
        db.create_all()

    return app

from flask import Flask, g, session
from app.extentions import db
from app.models.admin import Admin

from .routes import login


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    @app.before_request
    def load_logged_in_user():
        user_id = session.get('user_id')
        if user_id is None:
            g.admin = None
        else:
            g.admin = Admin.query.get(user_id)

    # Register Blueprints
    from .routes import events, speakers, venues, manager
    app.register_blueprint(login.bp)
    app.register_blueprint(events.bp)
    app.register_blueprint(speakers.bp)
    app.register_blueprint(venues.bp)
    app.register_blueprint(manager.bp)

    with app.app_context():
        db.create_all()

    return app

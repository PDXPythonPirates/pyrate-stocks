from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .models import db
    db.init_app(app)

    from app.main import main
    from app.services import ticker, user
    app.register_blueprint(main)
    app.register_blueprint(ticker.ticker)
    app.register_blueprint(user.user)

    with app.app_context():
        db.create_all()

        return app
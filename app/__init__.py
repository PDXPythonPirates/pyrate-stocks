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

    from app.main import main_bp
    from app.services import ticker, user
    app.register_blueprint(main_bp)
    app.register_blueprint(ticker.ticker_bp)
    app.register_blueprint(user.user_bp)

    with app.app_context():
        db.create_all()

        return app
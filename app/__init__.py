from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.permanent_session_lifetime = timedelta(hours = 1)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .models import db
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # commenting out previous configuration
    # app.config.from_object(config_class)
    # config_class.init_app(app)

    # work around to address error msg: 'Neither SQLALCHEMY_DATABASE_URI nor SQLALCHEMY_BINDS is set'
    app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL') or 'sqlite:///' + 'app.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
            
    from app.models import db
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.main import main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

        return app
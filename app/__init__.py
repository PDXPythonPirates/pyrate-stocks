from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    config_class.init_app(app)
            
    from app.models import db
    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)
    

    from app.main import main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

        return app
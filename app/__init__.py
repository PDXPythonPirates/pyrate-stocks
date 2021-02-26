from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
login = LoginManager()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
        
            
    from app.models import db
    db.init_app(app)
    login.init_app(app)
    

    from app.main import main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

        return app
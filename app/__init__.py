from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_mail import Mail


db = SQLAlchemy()
login = LoginManager()
mail = Mail()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
        
            
    from app.models import db
    db.init_app(app)
    login.init_app(app)
   
    

    from app.main import main_bp
    app.register_blueprint(main_bp)
    mail.init_app(app)

    with app.app_context():
        db.create_all()

        return app
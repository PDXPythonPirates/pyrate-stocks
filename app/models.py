from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
from app import db
from config import Config
from app import login
import jwt

@login.user_loader
def load_user(id):
    return Account.query.get(int(id))

class Account(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(30))
    password_hash = db.Column(db.String(128))
    stocks = db.Column(db.String(32))

    def __init__(self, username, email, password_hash, stocks):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.stocks = stocks

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=1800):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            Config.SECRET_KEY, algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, Config.SECRET_KEY,
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return Account.query.get(id)
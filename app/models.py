from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db
from app import login

@login.user_loader
def load_user(id):
    return Account.query.get(int(id))

class Account(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(10))
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
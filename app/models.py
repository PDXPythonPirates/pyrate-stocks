from app import db

class Ticker(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    symbol = db.Column(db.String(10))

class Account(db.Model):

    __tablename__ = 'account'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(10))
    email = db.Column(db.String(10))
    stocks = db.Column(db.String(32))

    def __init__(self, username, password, email, stocks):
        self.username = username
        self.password = password
        self.email = email
        self.stocks = stocks
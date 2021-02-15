from app import db

class Account(db.Model):
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
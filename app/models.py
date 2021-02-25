from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db
from app import login

import pandas as pd
import sqlite3

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

class importCsvSymbols():
    def importCsvDb():
        # Read original csv data
        # CSV Source: https://www.nasdaq.com/market-activity/stocks/screener 
        symbolList = pd.read_csv("app/csvfiles/nasdaq_screener_1614251368892.csv", usecols=["Symbol", "Name"], index_col=['Symbol'])
        print("Reading csv columns ... ")

        # Parse original csv data to columns needed & save to new csv file
        symbolList.to_csv('app/csvfiles/symbolList.csv', index_label=None)
        print("Parsing csv ... ")

        # Open database connection
        con = sqlite3.connect("data-dev.sqlite3")
        cur = con.cursor()
        print("Connecting to database ...")

        # Database read csv 
        df = pd.read_csv("app/csvfiles/symbolList.csv")
        print("Reading csv file ...")

        # Import csv data into table
        df.to_sql(
            name='symbolList',
            con = con,
            index=False,
            if_exists='replace')
        print("Creating symbolList table in database ...")
        
        # Close database connection
        con.close()
        print("Closing database connection ...")
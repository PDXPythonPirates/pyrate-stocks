from flask import session
from app import db
from app.models import Account

class UService:

    def get_data():
        user_data = Account.query.filter_by(username=session['user']).first()
        return user_data

    def get_symbols(user_data):
        symbol_list = user_data.stocks.replace(' ', '').split(',')
        return symbol_list

    def add_ticker(self, ticker):
        ticker = ticker.replace(' ', '')
        user = self.get_data()
        user.stocks = user.stocks + f',{ticker}'
        db.session.commit()

    def update_tickers(self, ticker_list):
        ticker_list = ','.join(ticker_list)
        user = self.get_data()
        user.stocks = ticker_list
        db.session.commit()
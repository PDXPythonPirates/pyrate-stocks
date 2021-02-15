from flask import session
from app import db
from app.models import Account


class UService:

    # Retrieve user's session data
    def get_data():
        user_data = Account.query.filter_by(username=session['user']).first()
        return user_data

    # Get a list of symbols the user follows
    def get_symbols(user_data):
        if(user_data.stocks == None):
            symbol_list = []
        else:
            symbol_list = user_data.stocks.replace(' ', '').split(',')
        return symbol_list

    # Add a stock ticker symbol to the user's followed symbols
    def add_ticker(self, ticker):
        ticker = ticker.replace(' ', '')
        user = self.get_data()
        user.stocks = user.stocks + f',{ticker}'
        db.session.commit()

    # Update the list of stock ticker symbols the user follows
    def update_tickers(self, ticker_list):
        ticker_list = ','.join(ticker_list)
        user = self.get_data()
        user.stocks = ticker_list
        db.session.commit()

    # Delete stock ticker symbol from user's followed symbols
    def delete_ticker(self, user_symbols, symbol):
        symbol = symbol.lower()
        user_symbols.remove(symbol)
        UService.update_tickers(UService, user_symbols)
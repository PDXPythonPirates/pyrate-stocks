import yfinance as yf
from flask import session, render_template
from app import db
from app.main import main_bp
from app.models import Account
from flask_login import current_user, login_user, login_required, logout_user
from app.main.forms import LoginForm, UpdateForm, SignUpForm

class Ticker:
    def ticker_data(symbols):
        stocks = []
        for s in symbols:
            try:
                ticker = yf.Ticker(s)
                current_price = ticker.info['bid']
                stock_data = {}
                stock_data['symbol'] = s
                stock_data['current_price'] = current_price
                stocks.append(stock_data)
            except KeyError:
                print('couldn\'t find stock ticker data')
                return
        return stocks

    # Retrieve user's session data
    def get_data():
        user_data = Account.query.filter_by(username=session['user']).first()
        return user_data

    # Get a list of symbols the user follows
    def get_symbols(user_data):
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
        user_symbols.remove(symbol)
        Ticker.update_tickers(Ticker, user_symbols)
    
    # #ISSUE: DASHBOARD DOES NOT RENDER ON LOGIN. USER IS REDIRECTED TO LOGIN PAGE.
    # # Takes user data as an input, gets followed symbols, retrieve ticker data
    # def dashboard():
    #     if 'user' in session:
    #         user_symbols = Ticker.get_symbols(Ticker.get_data())
    #         ticker_data = Ticker.ticker_data(user_symbols)
    #         # Get stock ticker data and render dashboard
    #         return render_template('dashboard.html', stocks=ticker_data, loform=LogoutForm(), uform=UpdateForm())
    #     # Not logged in
    #     else:
    #         return render_template('login.html', form=LoginForm(), display_message='User Login')
    
    # PLACEHOLDER FOR DASHBOARD RENDER ISSUE:
    def dashboard():
        if current_user.is_authenticated:
            return 'dashboard'
        # Not logged in
        else:
            return render_template('login.html', form=LoginForm(), display_message='User Login')
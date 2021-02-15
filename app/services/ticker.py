from flask import render_template, redirect, session
import yfinance as yf
from app.models import Ticker, Account
from app.main.forms import LoginForm, LogoutForm, UpdateForm

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

    # Add a new symbol to track in DB
    def add():
        # TODO: Get list of user's symbols and check for added symbol, if exists, return to dashboard
        # TODO: Check if added symbol exists in ticker table
            # Create new ticker OR Retrieve ticker entry
            # Update user stocks
        return

    # Delete a symbol being tracked in DB             
    def delete(ticker_id):
        # TODO: Pop from user's symbols, but do not remove from the db
        return
from flask import render_template, redirect, session
import yfinance as yf
from app.main import ticker
from app.models import Ticker, Account
from app.main.forms import LoginForm, LogoutForm, UpdateForm


# Add a new symbol to track in DB
@ticker.route("/add", methods=["POST"])
def add():

    # Get list of user's symbols and check for added symbol, if exists, return to dashboard
    # Check if added symbol exists in ticker table
        # Create new ticker OR Retrieve ticker entry
        # Update user stocks

    return


# Delete a symbol being tracked in DB             
@ticker.route("/delete/<int:ticker_id>")
def delete(ticker_id):

    # Pop from user's symbols

    return

if __name__=='__main__':
    ticker.run(debug=True)
from flask import render_template, redirect, session
from app.main import main_bp
from app.models import Ticker, Account
from app.main.forms import LoginForm, LogoutForm, UpdateForm
from app.services.ticker import ticker_data


@main_bp.route('/')
def home():
    return render_template('home.html')


@main_bp.route('/dashboard/', methods=['GET', 'POST'])
def dashboard():
    lform = LoginForm()
    uform = UpdateForm()

    if 'user' in session:

        # Grab user data and get stock data for the tickers they follow
        user_data = Account.query.filter_by(username=session['user']).first()
        stocks = ticker_data(user_data)

        # Load dashboard and return stock ticker data
        return render_template('dashboard.html', stocks=stocks, loform=LogoutForm(), uform=UpdateForm())

    else:
        form = LoginForm()
        return render_template('login.html', form=form, display_message='User Login')
from flask import render_template, redirect, flash, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from app.main import main_bp
from app.models import Account
from app.main.forms import SignUpForm, LoginForm, LogoutForm, UpdateForm
from app.services.user_svc import UserService
from app import db
from app.services.ticker_svc import TickerService

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    user_signup = UserService.signup()
    return user_signup
    
@main_bp.route('/login/', methods=['GET', 'POST'])
def login():
    user_login = UserService.login()
    return user_login

@main_bp.route('/logout/', methods=['GET', 'POST'])

def logout():
    user_logout = UserService.logout()
    return user_logout

@main_bp.route('/update/', methods=['GET', 'POST'])

def update():
    user_update = UserService.update()
    return user_update

# Get stock ticker data and render dashboard
@main_bp.route('/dashboard/', methods=['GET', 'POST'])
def dashboard():
    if current_user.is_authenticated:
        user_symbols = UserService.get_symbols()
        if len(user_symbols) == 1 and user_symbols[0] == '':
            ticker_data = None
        else:
            ticker_data = TickerService.ticker_data(user_symbols)
        return render_template('dashboard.html', stocks=ticker_data, loform=LogoutForm(), uform=UpdateForm())
    else:
        return render_template('login.html', form=LoginForm(), display_message='User Login')

# Add a new symbol to track in DB
@main_bp.route("/add/", methods=["POST"])
def add():
    symbol = request.form['symbol']
    symbol = symbol.lower()
    user_symbols = UserService.get_symbols()
    if symbol not in user_symbols:
        UserService.add_ticker(symbol)
    return redirect(url_for('main_bp.dashboard'))

# Delete the symbol from user's followed symbols
@main_bp.route("/delete/<symbol>")
def delete(symbol):
    user_symbols = UserService.get_symbols()
    symbol = symbol.lower()
    if symbol in user_symbols:
        UserService.delete_ticker(user_symbols, symbol)
    return redirect(url_for('main_bp.dashboard'))
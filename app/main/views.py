from flask import render_template, redirect, before_render_template, flash, url_for
from flask_login import current_user, login_user, login_required, logout_user
from app.main import main_bp
from app.models import Account, Ticker
from app.main.forms import LoginForm, LogoutForm, UpdateForm
from app.services.user import User
from app.services.ticker import Ticker

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    user_signup = User.signup()
    return user_signup
    
@main_bp.route('/login/', methods=['GET', 'POST'])
def login():
    user_login = User.login()
    return user_login

@main_bp.route('/update/', methods=['GET', 'POST'])
def update():
    user_update = User.update()
    return user_update

@main_bp.route('/logout/', methods=['GET', 'POST'])
def logout():
    user_logout = User.logout()
    return user_logout

@main_bp.route('/dashboard/', methods=['GET', 'POST'])
def dashboard():
    if current_user.is_authenticated:
        return 'dashboard'
        # user_symbols = UService.get_symbols(UService.get_data())
        # ticker_data = TService.ticker_data(user_symbols)
        # return render_template('dashboard.html', stocks=ticker_data, loform=LogoutForm(), uform=UpdateForm())
    # Not logged in
    else:
        return render_template('login.html', form=LoginForm(), display_message='User Login')

@main_bp.route("/add", methods=["POST"])
def add():
    ticker_add = Ticker.add()
    return ticker_add

@main_bp.route("/delete/<int:ticker_id>")
def delete():
    ticker_delete = Ticker.delete()
    return ticker_delete




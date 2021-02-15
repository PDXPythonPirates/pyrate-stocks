from flask import render_template, redirect, session, flash,url_for
from flask_login import current_user, login_user, login_required, logout_user
from app.main import main_bp
from app.models import Account, Ticker
from app.main.forms import LoginForm, LogoutForm, UpdateForm

from app.services.user import User


@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    flash('accessing signup page')
    user_signup = User.signup()
    return user_signup
    
@main_bp.route('/login/', methods=['GET', 'POST'])
def login():
    print('accessing login page')
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
        
        return redirect(url_for('main_bp.dashboard'))
    else:
        form = LoginForm()
        return render_template('login.html', form=form, display_message='User Login')
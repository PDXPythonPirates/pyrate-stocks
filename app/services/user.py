from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, login_required, logout_user
from app import db
from app.main import user_bp,main_bp
from app.models import Account
from app.main.forms import LoginForm, UpdateForm, SignUpForm


@user_bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        flash('You already signed in!')
        return redirect(url_for('main_bp.dashboard'))
    sform = SignUpForm()
    lform = LoginForm()

    if sform.validate_on_submit():
        user = Account(username=sform.username.data, email=sform.email.data, password_hash='xxx', stocks=sform.stocks.data)
        user.set_password(sform.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You were successfully logged in')
        return render_template('login.html', form=lform)
    flash('Please sign Up')
    return render_template('signup.html', title='Signup', form=sform)
    

@user_bp.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You already signed in!')
        return redirect(url_for('main_bp.dashboard'))

    lform = LoginForm()
    if lform.validate_on_submit():
        user = Account.query.filter_by(username=lform.username.data).first()
        if user is None or not user.check_password(lform.password.data):
            flash('Please sign up first!')
            return redirect(url_for('user_bp.login'))

        flash('You are logged in.')
        login_user(user, remember=lform.remember.data)
        return redirect(url_for('main_bp.dashboard'))

    return render_template('login.html', title='Sign In', form=lform)

@user_bp.route('/update/', methods=['GET', 'POST'])
@login_required
def update():
    uform = UpdateForm()
    if uform.validate_on_submit():
        current_user.username = uform.username.data
        current_user.email = uform.email.data
        current_user.password = uform.password.data
        current_user.set_password(uform.password.data)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main_bp.dashboard'))
      
    return render_template('update.html', title='Update',
                           form=uform)


@user_bp.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You are logged out!')
    return redirect(url_for('main_bp.home'))

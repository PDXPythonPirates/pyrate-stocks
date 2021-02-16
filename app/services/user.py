from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from app import db
from app.models import Account
from app.main import main_bp
from app.main.forms import LoginForm, UpdateForm, SignUpForm

class User:
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
        
    def login():
        
        if current_user.is_authenticated:
            flash('You already signed in!')
            return redirect(url_for('main_bp.dashboard'))

        lform = LoginForm()
        if lform.validate_on_submit():
            if Account.query.filter_by(username=lform.username.data).count() < 1:
                flash('Please sign Up')
                return render_template('signup.html', title='Signup', form=SignUpForm())
            user = Account.query.filter_by(username=lform.username.data).first()
            if user is None or not user.check_password(lform.password.data):
                flash('Inccorrect login!')
                return redirect(url_for('main_bp.login'))
            flash('You are logged in.')
            login_user(user, remember=lform.remember.data)
            return redirect(url_for('main_bp.dashboard'))
        return render_template('login.html', title='Sign In', form=lform)

    @login_required
    def update():
        if current_user.is_authenticated:
            _username = current_user.username
            user = Account.query.filter_by(username=_username).first()
            uform = UpdateForm()
            if request.method == 'POST':
                if uform.username.data != _username:
                    flash('Your username is incorrect.')
                    return render_template('update.html', form=uform)
                if uform.validate_on_submit():
                    uform.populate_obj(user)
                    user.set_password(uform.password.data)
                    db.session.commit()
                    flash('Your inforamtion is update!')
                    return redirect(url_for('main_bp.dashboard'))
            flash('Form not validated')
            return render_template('update.html', form=uform)
        
        flash('Please login first.')
        render_template('login.html', title='Sign In', form=LoginForm())
        
    @login_required
    def logout():
        logout_user()
        flash('You are logged out!')
        return redirect(url_for('main_bp.home'))

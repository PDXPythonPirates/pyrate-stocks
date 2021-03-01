from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from app import db
from app.models import Account
from app.services.email import send_password_reset_email
from app.main.forms import LoginForm, UpdateForm, SignUpForm, ResetPasswordRequestForm, ResetPasswordForm


class UserService():
    def signup():
        if current_user.is_authenticated:
            flash('You already signed in!')
            return redirect(url_for('main_bp.dashboard'))
        
        sform = SignUpForm()
        if sform.validate_on_submit():
            user = Account(username=sform.username.data, email=sform.email.data, password_hash='xxx', stocks=sform.stocks.data)
            user.set_password(sform.password.data)
            db.session.add(user)
            db.session.commit()
            flash(f'Welcome {user.username}! You\'re now a new user.')
            # lform.username.data = user.username
            return redirect(url_for('main_bp.dashboard'))
        flash('Please sign Up')
        return render_template('signup.html', title='Signup', form=sform)    
        
    def login():
        if current_user.is_authenticated:
            flash('You already signed in!')
            return redirect(url_for('main_bp.dashboard'))

        lform = LoginForm()
        if lform.validate_on_submit():
            user = Account.query.filter_by(username=lform.username.data).first()
            if user is None:
                flash('Please sign Up')
                return render_template('signup.html', title='Signup', form=SignUpForm())

            if not user.check_password(lform.password.data):    
                flash('Wrong password!')
                lform.username.data = user.username
                return render_template('login.html', title='Sign In', form=lform)
            
            flash('You are logged in.')
            login_user(user, remember=lform.remember.data)
            return redirect(url_for('main_bp.dashboard'))
        return render_template('login.html', title='Sign In', form=LoginForm())

    def reset_passwd_request():
        if current_user.is_authenticated:
            return redirect(url_for('main_bp.dashboard'))
        form = ResetPasswordRequestForm()
        if form.validate_on_submit():
            user = Account.query.filter_by(email=form.email.data).first()
            if user:
                print('useremail for send_password_reset_email function in user_srv.py=', user.email)
                send_password_reset_email(user)
            flash('Check your email for the instructions to reset your password')
            return redirect(url_for('main_bp.login'))
        return render_template('reset_password_request.html',
                            title='Reset Password', form=form)

    def reset_passwd(token):
        if current_user.is_authenticated:
            return redirect(url_for('main_bp.dashboard'))
        user = Account.verify_reset_password_token(token)
        if not user:
            return redirect(url_for('main_bp.login'))
        form = ResetPasswordForm()
        if form.validate_on_submit():
            user.set_password(form.password.data)
            db.session.commit()
            flash('Your password has been reset.')
            return redirect(url_for('main_bp.login'))
        return render_template('reset_password.html', form=form)

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
                    flash('Your inforamtion is updated!')
                    return redirect(url_for('main_bp.dashboard'))
            
            uform.username.data = current_user.username
            uform.email.data = current_user.email
            uform.stocks.data = current_user.stocks
            return render_template('update.html', form=uform)
        
        flash('Please login first.')
        render_template('login.html', title='Sign In', form=LoginForm())
    

    def get_data():
        user = Account.query.filter_by(username=current_user.username).first()
        return user

    # Get a list of symbols the user follows
    def get_symbols():

        # Turn string of symbols into list
        # NOTE: If the user entered a comma, it will produce 2 empty symbols
        user = UserService.get_data()

        # Format list
        symbol_list = user.stocks.replace(' ', '').split(',')
        new_symbols = []
        
        # If the user accidentally put a comma at the end or beginning of their string,
        # this check will remove the empty symbols to prevent ticker data error
        for item in range(len(symbol_list)):
            if symbol_list[item] != '':
                symbol_list[item] = symbol_list[item].lower()
                if symbol_list[item] in new_symbols:
                    continue
                else:
                    new_symbols.append(symbol_list[item])
            else:
                flash('Index item ' + str(item) + ' is NOT valid.')
        
        # If there's an issue with the symbol list, update user symbols in db
        if not new_symbols:
            return symbol_list
        else:
            UserService.update_tickers(new_symbols)
            return new_symbols

    # Add a stock ticker symbol to the user's followed symbols
    def add_ticker(ticker):
        ticker = ticker.replace(' ', '')
        user = UserService.get_data()
        user.stocks = user.stocks + f',{ticker}'
        db.session.commit()

    # Update the list of stock ticker symbols the user follows
    def update_tickers(ticker_list):
        ticker_list = ','.join(ticker_list)
        user = UserService.get_data()
        user.stocks = ticker_list
        db.session.commit()

    # Delete stock ticker symbol from user's followed symbols
    def delete_ticker(user_symbols, symbol):
        user_symbols.remove(symbol)
        UserService.update_tickers(user_symbols)

  
    def logout():
        logout_user()
        flash('You are logged out!')
        return redirect(url_for('main_bp.home'))

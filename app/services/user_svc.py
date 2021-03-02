from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from app import db
from app.models import Account
from app.main.forms import LoginForm, UpdateForm, SignUpForm

class UserService():
    def signup():
        if current_user.is_authenticated:
            flash('You already signed in!', 'notify')
            return redirect(url_for('main_bp.dashboard'))
        
        sform = SignUpForm()
        lform = LoginForm()

        if sform.validate_on_submit():
            user = Account(username=sform.username.data, email=sform.email.data, password_hash='xxx', stocks=sform.stocks.data)
            user.set_password(sform.password.data)
            db.session.add(user)
            db.session.commit()
            flash(f'Welcome {user.username}! Please login.', 'notify')
            # lform.username.data = user.username
            return redirect(url_for('main_bp.dashboard'))
        return render_template('signup.html', title='Signup', form=sform)    
        
    def login():
        if current_user.is_authenticated:
            flash('You already signed in!', 'notify')
            return redirect(url_for('main_bp.dashboard'))

        lform = LoginForm()
        if lform.validate_on_submit():
            user = Account.query.filter_by(username=lform.username.data).first()
            if user is None:
                flash('Please sign Up', 'notify')
                return render_template('signup.html', title='Signup', form=SignUpForm())

            if not user.check_password(lform.password.data):    
                flash('Wrong password!', 'alert')
                lform.username.data = user.username
                return render_template('login.html', title='Sign In', form=lform)
            
            flash(f'Welcome, {user.username}!', 'notify')
            login_user(user, remember=lform.remember.data)
            return redirect(url_for('main_bp.dashboard'))
        return render_template('login.html', title='Sign In', form=lform)

    
    def update():
        if current_user.is_authenticated:
            _username = current_user.username
            user = Account.query.filter_by(username=_username).first()
            uform = UpdateForm()
            if request.method == 'POST':
                if uform.username.data != _username:
                    flash('Your username is incorrect.', 'alert')
                    return render_template('update.html', form=uform)
                if uform.validate_on_submit():
                    uform.populate_obj(user)
                    user.set_password(uform.password.data)
                    db.session.commit()
                    flash('Your inforamtion has been updated.', 'notify')
                    return redirect(url_for('main_bp.dashboard'))
            
            uform.username.data = current_user.username
            uform.email.data = current_user.email
            uform.stocks.data = current_user.stocks
            return render_template('update.html', form=uform)
        
        flash('Please login first.', 'alert')
        render_template('login.html', title='Sign In', form=LoginForm())
    
    # Get user data based on the current_user's username
    def get_data():
        user = Account.query.filter_by(username=current_user.username).first()
        return user

    # Get a list of symbols the user follows
    def get_symbols():

        # Retrieve all user data
        user = UserService.get_data()

        # Parse through user's stock symbol list
        symbol_list = user.stocks.replace(' ', '').split(',')
        new_symbols = []
        print('Parsing through list: ' + str(symbol_list))

        # If the user accidentally put a comma at the end or beginning of their string,
        # this check will remove the empty symbols to prevent ticker data error
        for item in range(len(symbol_list)):
            symbol = symbol_list[item].lower()
            if symbol != '':
                if symbol in new_symbols:
                    continue
                else:
                    new_symbols.append(symbol)
                    print('Ticker symbol \'' + str(symbol) + '\' is valid.')
            else:
                print('Ticker symbol \'' + str(symbol) + '\' is NOT valid.')
        
        # If there's an issue with the symbol list, update user symbols in db
        if not new_symbols:
            return symbol_list
        else:
            print('Updated list: ' + str(new_symbols))
            UserService.update_tickers(new_symbols)
            return new_symbols

    # Add a stock ticker symbol to end of the user's followed symbols
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
        print('Updating symbols saved to user profile...')
        db.session.commit()

    # Delete stock ticker symbol from user's followed symbols
    def delete_ticker(user_symbols, symbol):
        symbol = symbol.lower()
        if symbol in user_symbols:
            user_symbols.remove(symbol)
            print(f'Deleting: {symbol}')
            UserService.update_tickers(user_symbols)
        else:
            print(f'Symbol {symbol} is not in the user symbols')
            return

    # Remove user from current_user session
    def logout():
        logout_user()
        flash('You are logged out!', 'notify')
        return redirect(url_for('main_bp.home'))

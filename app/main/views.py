from flask import Flask, render_template, redirect, session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from werkzeug.utils import secure_filename
from operator import irshift
from datetime import timedelta
from keychain import Keys
import yfinance as yf
import json

from forms import SignUpForm, LoginForm, UpdateForm, LogoutForm
from keychain import Keys

# App configuration
app = Flask(__name__, template_folder='../templates')
app.config['SECRET_KEY'] = Keys.secret()
app.permanent_session_lifetime = timedelta(days = 1)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##### MODELS #####

# Ticker table
class Ticker(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    symbol = db.Column(db.String(10))

# Account table
class Account(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(10))
    email = db.Column(db.String(10))
    stocks = db.Column(db.String(32))

    def __init__(self, username, password, email, stocks):
        self.username = username
        self.password = password
        self.email = email
        self.stocks = stocks

# Database table init & save to ensure tables are created
db.create_all()
db.session.commit()


##### HOME #####

@app.route('/')
def home():
    return render_template('home.html')


##### SIGNUP #####

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    sform = SignUpForm()
  
    # When form is submitted, assign data to local variables
    if sform.validate_on_submit():
        username = sform.username.data
        password = sform.password.data
        email = sform.email.data
        stocks = sform.stocks.data

        # Query database for accounts that have a matching username
        # If a name exists, user is redirected to the homepage.
        if Account.query.filter_by(username=username).count() < 1:
            new = Account(username, password, email, stocks)
            db.session.add(new)
            db.session.commit()

            # Added user account information to DB. Render the dashboard.
            return render_template('dashboard.html', form=sform, display_message='Welcome to Financial App!')
        
        # If the username already exists, go back to the signup form with empty fields.
        sform = SignUpForm()
        return render_template('signup.html', form=sform, display_message='Please try a different username.')

    # When navigating to the signup page (no post request)
    return render_template('signup.html', form=sform)


##### LOGIN #####

@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Load loginform and assign both fields to local variables
    lform = LoginForm()
    username = lform.username.data
    password = lform.password.data

    # If the user is logged in already, send them back to their dashboard
    if 'user' in session:
        return render_template('dashboard.html', form=lform, display_message='You are already logged in!')

    # When the login form is submitted
    if lform.validate_on_submit():

        # Check db for username & password match
        user_info = Account.query.filter_by(username=username).first()
        _username = user_info.username
        _password = user_info.password

        # If the username and password match the corresponding database account entry, start a user session
        if _username == username and _password == password:
            session.permanent=True
            session['user'] = username

            # Login successful
            return render_template('dashboard.html', form=lform, display_message='Welcome back!')
        
        # Login information could not be matched with username/password from account table in the DB
        return render_template('login.html', form=lform, display_message='Incorrect Login')

    # User just arrived at the login page and is not yet logged in to their account
    return render_template('login.html', form=lform, display_message='User Login')


##### DASHBOARD #####

@app.route('/dashboard/', methods=['GET', 'POST'])
def dashboard():
    if 'user' in session:
        # TODO: Check to make sure following logic will get a list of symbols from the user's stocks column in the Account table.
        user_data = Account.query.filter_by(username=session['user'])
        stocks = user_data.stocks

        # unfinished
        stocks = stocks.split().strip()
        for i in stocks:
            t = yf.Ticker(i)


        # TODO: Create a query here that will get all of the ticker data for each item in the "stocks" variable

        # Load dashboard and return stock ticker data
        return render_template('dashboard.html', tickers=tickers)

    else:
        form = LoginForm()
        return render_template('login.html', form=form, display_message='User Login')


################# THIS WILL NOT BE EXECUTED ######################
    ticker_list = Ticker.query.all()
    ticker = yf.Ticker('TSLA') # TODO: Need to pass ticker, using TSLA to temporarily render data as a test
    current_price = ticker.info['bid'] 
    market_high = ticker.info['dayHigh']
    market_low = ticker.info['dayLow']
    market_open = ticker.info['open']
    market_close = ticker.info['previousClose']
    return render_template(
        "dashboard.html", 
        ticker_list=ticker_list, 
        current_price=current_price, 
        market_high=market_high, 
        market_low=market_low,
        market_open=market_open,
        market_close=market_close)
##################################################################


##### ADD STOCK TICKER SYMBOL #####

# Add a new symbol to track in DB
@app.route("/add", methods=["POST"])
def add():

    # TODO: Create a query here that will get a list of symbols from the user's "stocks" column in the Account table.
    # TODO: Check if the stock data for this specific stock already exists in the ticker table
        # If the above check returns "False", create new ticker entry and update the user profile to include the newly followed stock symbol.
        # If the above check returns "True", retrieve the ticker entry, check to see if symbol exists in user's "stocks" column,
            # and update the user profile to include the newly followed stock symbol.
    
    """
    This is the previously used code for adding a stock ticker symbol to the dashboard:

    symbol = request.form.get("symbol")
    new_ticker = Ticker(symbol=symbol) # TODO: Instead of adding a new ticker to the ticker table, we need to add the ticker symbol to the user's account information
    print(new_ticker)
    db.session.add(new_ticker)
    db.session.commit()
    return redirect('/dashboard')
    """


##### DELETE STOCK TICKER SYMBOL #####

# Delete a symbol being tracked in DB             
@app.route("/delete/<int:ticker_id>")   
def delete(ticker_id):

    """
    This code needs to be updated so that it does not delete from the ticker table, 
    but from the "stock" column in the user's Account table entry:

    Ticker.query.filter_by(id=ticker_id).delete()
    db.session.commit()
    return redirect('/dashboard')
    """


##### UPDATE #####

@app.route('/update/', methods=['GET', 'POST'])
def update():
    uform = UpdateForm()
    
    # If the form was submitted as a POST request
    if uform.validate_on_submit():

        # Form data stored in local variables
        username = uform.username.data
        password = uform.password.data
        email = uform.email.data
        stocks = uform.stocks.data

        # Query the account table (using username column) to get all of the user's information
        user_info = Account.query.filter_by(username=username).first()
        _username = user_info.username

        # Is this 'if' statement necessary?
        if _username == username:
            user_info.password = password
            user_info.email = email
            user_info.stocks = stocks
            db.session.commit()
            return render_template('dashboard.html', form=uform, display_message='Your account info is updated')
        
        else:
            return render_template('update.html', form=uform, display_message="User doesn't exist")

    return render_template('update.html', form=uform)


##### LOGOUT #####

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    loform = LogoutForm()

    # If the logout button was clicked, remove user from session.
    if loform.validate_on_submit():
        session.pop('user', None)
        return render_template('home.html', form=loform, display_message='You are logged out')

    else:
        return render_template('dashboard.html')


##### RUN APP #####

if __name__=='__main__':
    app.run(debug=True)
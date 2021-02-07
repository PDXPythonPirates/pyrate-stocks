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

# Database table init & save to ensure tables are created
db.create_all()
db.session.commit()

##### HOME #####
@app.route('/')
def home():

    return render_template('home.html')


##### DASHBOARD #####

@app.route('/dashboard/', methods=['GET', 'POST'])
def dashboard():
    if 'user' in session:
        # Create a query here that will get a list of symbols from the user's stocks column in the users table.
        stocks = Account.query.filter_by(username=session['user']).first()
        return render_template('dashboard.html', stocks=stocks)
    else:
        form = LoginForm()
        return render_template('login.html', form=form, display_message='User Login')

    # TODO: Create a query here that will get a list of symbols from the user's followed_tickers column in the users table.
    # TODO: Feed the list of symbols through the yf.Ticker()
    ticker_list = Ticker.query.all()
    ticker = yf.Ticker('TSLA') # TODO: Need to pass ticker, using TSLA to temporarily render data as a test
    current_price = ticker.info['bid'] 
    market_high = ticker.info['dayHigh']
    market_low = ticker.info['dayLow']
    market_open = ticker.info['open']
    market_close = ticker.info['previousClose']
    # TODO: Create a context for all of the data and pass a single context variable to the dashboard template
    return render_template(
        "dashboard.html", 
        ticker_list=ticker_list, 
        current_price=current_price, 
        market_high=market_high, 
        market_low=market_low,
        market_open=market_open,
        market_close=market_close)

# Add a new symbol to track in DB
@app.route("/add", methods=["POST"])
def add():
    symbol = request.form.get("symbol")
    new_ticker = Ticker(symbol=symbol)
    print(new_ticker)
    db.session.add(new_ticker)
    db.session.commit()
    return redirect('/dashboard')

# Delete a symbol being tracked in DB             
@app.route("/delete/<int:ticker_id>")   
def delete(ticker_id):
    Ticker.query.filter_by(id=ticker_id).delete()
    db.session.commit()
    return redirect('/dashboard')

##### SIGNUP #####


@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    sform = SignUpForm()
  
    if sform.validate_on_submit():
        sname = sform.username.data
        spasswd = sform.password.data
        semail = sform.email.data
        sstocks = sform.stocks.data

        if Account.query(Account).filter_by(username=sname).count() < 1:
            new = Account(sname, spasswd, semail, sstocks)
            db.session.add(new)
            db.session.commit()
            return render_template('dashboard.html', form=sform, display_message='Welcome. You are all set.')
        
        return render_template('home.html',
                    display_message='User already exists.')
    return render_template('signup.html', form=sform)

##### LOGIN #####

@app.route('/login/', methods=['GET', 'POST'])
def login():
    lform = LoginForm()
    username = lform.username.data
    password = lform.password.data

    if lform.validate_on_submit():
        session.permanent=True
        session['user'] = username

        # Check db for username & password match
        user_info = Account.query.filter_by(username=username).first()
        usern = user_info.username
        passwd = user_info.password
        if usern == username and passwd == password:
            return render_template('dashboard.html', form=lform, 
                        display_message='Remember logout when you are done.')
                
        return render_template('login.html', form=lform,
                                                display_message='Incorrect Login')
    else:
        if 'user' in session:
            return render_template('dashboard.html', form=lform, 
                                display_message='Remember logout when you are done.')
        else:
            return render_template('login.html', form=lform, display_message='User Login')


##### UPDATE #####

@app.route('/update/', methods=['GET', 'POST'])
def update():
    uform = UpdateForm()
        
    if uform.validate_on_submit():
        username = uform.username.data
        password = uform.password.data
        email = uform.email.data
        stocks = uform.stocks.data

        user_info = Account.query.filter_by(username=username).first()
        usern = user_info.username
        if usern == username:
            user_info.password = password
            user_info.email = email
            user_info.stocks = stocks
            db.session.commit()
            return render_template('dashboard.html', form=uform, 
                                 display_message='Your account info is updated')
                
        else:
            return render_template('update.html', form=uform, 
                                        display_message="User doesn't exist")

        
    return render_template('update.html', form=uform)

##### LOGOUT #####

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    loform = LogoutForm()
    if loform.validate_on_submit():
        session.pop('user', None)
        return render_template('home.html', form=loform, 
                                        display_message='You are logged out')
    else:
        return render_template('dashboard.html')

##### RUN APP #####

if __name__=='__main__':
    app.run(debug=True)
from flask import Flask, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

import json
import yfinance as yf

from forms import LoginForm, LogoutForm, SignUpForm
from keychain import Keys

# App configuration
app = Flask(__name__, template_folder='../templates')
app.config['SECRET_KEY'] = Keys.secret()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database models
class Ticker(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    symbol = db.Column(db.String(10))

# Database table init & save to ensure tables are created
db.create_all()
db.session.commit()


##### DASHBOARD #####

@app.route("/dashboard")
def dashboard():

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
    form = SignUpForm()

    print('signup page accessed')
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        with open('app/main/user_data.json', mode='r') as file:
            data = json.load(file)

        with open('app/main/user_data.json', mode='w') as file:
            all_users = data['users']
            user_data = {
                'password': password,
                'email': email
            }
            user = {username: user_data}
            all_users.append(user)
            data = {"users":all_users}
            json.dump(data, file)

        return redirect('/login')

    return render_template('signup.html', form=form)


##### LOGIN #####

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check user_data.json for username & password match
        with open('app/main/user_data.json', 'r') as file:
            data = json.load(file)
            all_users = data['users']

            for user in all_users:
                _username = list(user.keys())[0]
                if username == _username and password == user[_username]['password']:
                    return render_template('dashboard.html', form=LogoutForm(), display_message='Login Success')
        
            return render_template('login.html', form=form, display_message='Incorrect Login')

    return render_template('login.html', form=form, display_message='User Login')


##### PROFILE #####

@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    form = LogoutForm()

    return render_template('profile.html', form=form)


##### LOGOUT #####

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    form = LogoutForm()
    
    if form.validate_on_submit():

        return render_template('home.html', form=form, display_message='Successfully logged out')
    else:
        
        return render_template('profile.html')
    
    
#### HOME #####

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


##### RUN APP #####

if __name__=='__main__':
    app.run(debug=True)
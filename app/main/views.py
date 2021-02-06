from flask import Flask, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, LogoutForm, SignUpForm
from keychain import Keys

import json
import requests
from datetime import date

today = date.today()
date = today.strftime('%Y-%m-%d')

app = Flask(__name__, template_folder='../templates')
app.config['SECRET_KEY'] = Keys.secret()
# Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Ticker(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    symbol = db.Column(db.String(10))
    
db.create_all()
db.session.commit()


### TEST TO PRINT STOCK DATA ###
# ticker = yf.Ticker('TSLA')
# df = ticker.info
# for key,value in df.items():
#     print(key, ":", value)

db.create_all()
db.session.commit()

##### DASHBOARD #####

@app.route("/dashboard")
def dashboard():
    ticker_list = Ticker.query.all()
    ticker = yf.Ticker('TSLA') # TODO: temporary.... how to pass 'symbol' from Ticker class?
    current_price = ticker.info['bid'] 
    market_high = ticker.info['dayHigh']
    market_low = ticker.info['dayLow']
    market_open = ticker.info['open']
    market_close = ticker.info['previousClose']
    return render_template("dashboard.html", 
                           ticker_list=ticker_list, 
                           current_price=current_price, 
                           market_high=market_high, 
                           market_low=market_low,
                           market_open=market_open,
                           market_close=market_close)
    
# Add a new symbol to track in DB
@app.route("/add", methods=["POST"])
def add():

    # Format the API request and get a response object
    symbol = request.form.get("symbol").upper()
    api_request = api + apiFunction + '&symbol=' + symbol + apiOption + '&apikey=' + apiKey # this creates a URL for the request
    response = requests.get(api_request).json() # request and stores response object to 'response' variable

    # parse through response object to get the data we want to access
    data = response['Time Series (60min)']
    open = list(response['Time Series (60min)'])[-1] # last dictionary in response object
    latest = next(iter(response['Time Series (60min)'])) # latest dictionary in response object

    earliest_data = data[open] # earliest dictionary of data available today
    latest_data = data[latest] # latest dictionary of data available today

    print(earliest_data)
    print(latest_data)

    current_price = latest_data['4. close'] # gets latest hour closing price. This is not a great reflection of current price, but works well for testing & to find the current price every 60 mins.
    #market_high = max([k['2. high'] for k, v in data.items()]) # gets highest number from highs today
    #market_low = min([k['3. low'] for k, v in data.items()]) # gets lowest number from lows today
    #market_open = earliest_data['1. open']
    #market_close = latest_data['4. close']


    ticker_data = Ticker(
        symbol = symbol,
        current_price = current_price,
        market_high = 'n/a',
        market_low = 'n/a',
        market_open = 'n/a',
        market_close = 'n/a'
        )

    db.session.add(ticker_data)
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
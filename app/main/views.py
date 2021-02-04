from flask import Flask, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from forms import LoginForm, LogoutForm, SignUpForm
from keychain import Keys
import json

app = Flask(__name__, template_folder='../templates')
app.config['SECRET_KEY'] = Keys.secret()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Bootstrap(app)
db = SQLAlchemy(app)

# DB class for dashboard.html
class Ticker(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    symbol = db.Column(db.String(50))
    current_price = db.Column(db.String(50))
    market_high = db.Column(db.String(50))
    market_low = db.Column(db.String(50))
    market_open = db.Column(db.String(50))
    market_close = db.Column(db.String(50))

    # # save??
    # def __init__(self, symbol, current_price, market_high, market_low, market_open, market_close):
    #     self.symbol = symbol
    #     self.current_price = current_price
    #     self.market_high = market_high
    #     self.market_low = market_low
    #     self.market_open = market_open
    #     self.market_close = market_close

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
    
    

    
##### DASHBOARD #####

@app.route("/dashboard")
def dashboard():
    ticker_list = Ticker.query.all()
    return render_template("dashboard.html", ticker_list=ticker_list)

# Add a new symbol to track in DB
@app.route("/add", methods=["POST"])
def add():
    symbol = request.form.get("symbol")
    new_ticker = Ticker(symbol=symbol)
    db.session.add(new_ticker)
    db.session.commit()
    return redirect('/dashboard')

# Delete a symbol being tracked in DB             
@app.route("/delete/<int:ticker_id>")   
def delete(ticker_id):
    ticker = Ticker.query.filter_by(id=ticker_id).first
    db.session.delete(symbol)
    db.session.commit()
    return redirect('/dashboard')


##### RUN APP #####

if __name__=='__main__':
    db.create_all()
    app.run(debug=True)
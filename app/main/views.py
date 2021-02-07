from operator import irshift
from flask import Flask, render_template, redirect, request, session
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from forms import SignUpForm, LoginForm, UpdateForm, LogoutForm
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from keychain import Keys
import json

app = Flask(__name__, template_folder='../templates')
app.config['SECRET_KEY'] = Keys.secret()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days = 1)
Bootstrap(app)

db = SQLAlchemy(app)

# account table
class Account(db.Model):

    __tablename__ = 'account'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(10))
    email = db.Column(db.String(20))
    stocks = db.Column(db.String(20))

    def __init__(self, username, password, email, stocks):
        self.username = username
        self.password = password
        self.email = email
        self.stocks = stocks

##### SIGNUP #####

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    sform = SignUpForm()
  
    if sform.validate_on_submit():
        username = sform.username.data
        password = sform.password.data
        email = sform.email.data
        stocks = sform.stocks.data

        if Account.query.filter_by(username=username).count() < 1:
            new = Account(username, password, email, stocks)
            db.session.add(new)
            db.session.commit()
            return render_template('dashboard.html', form=sform, display_message='Welcome. You are all set.')
        
        return render_template('home.html',
                    display_message='User already exists. Try it again.')
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
                        display_message='Remember logout when you are done --')
                
        return render_template('login.html', form=lform,
                                                display_message='Incorrect Login')
    else:
        if 'user' in session:
            return render_template('dashboard.html', form=lform, 
                                display_message='Remember logout when you are done --')
        else:
            return render_template('login.html', form=lform, display_message='User Login')
  
##### PROFILE #####

@app.route('/dashboard/', methods=['GET', 'POST'])
def dashboard():
    lform = LoginForm()
    uform = UpdateForm()

    if 'user' in session:
        # Create a query here that will get a list of symbols from the user's stocks column in the users table.
        stocks = Account.query.filter_by(username=session['user']).first()
        return render_template('dashboard.html', stocks=stocks)
    elif uform.validate_on_submit():
        return render_template('update.html', form=uform)
    else:
        return render_template('login.html', form=form, display_message='User Login')
    

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
            db.session.merge(user_info)
            db.session.flush()
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
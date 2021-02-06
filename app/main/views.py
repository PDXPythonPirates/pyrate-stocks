from flask import Flask, render_template, redirect, session
from flask_bootstrap import Bootstrap
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
class account(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(10))
    email = db.Column(db.String(10))
    stocks = db.Column(db.String(20), unique=True, nullable=False)

##### SIGNUP #####

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        stocks = form.stocks.data

        user_info = account.query.filter_by(username=username).first()
        if not user_info:
            user_info = account(username=username, email=email,password = password, stocks = stocks)
            db.session.add(user_info)
            db.session.commit()
            return render_template('dashboard.html', form=form, 
                    display_message='Welcome. You are all set.')
        return render_template('login.html', form=form, 
                    display_message='user already exists.')
    return render_template('signup.html', form=form)

##### LOGIN #####

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username = form.username.data
    password = form.password.data

    if form.validate_on_submit():
        session.permanent=True
        session['user'] = username

        # Check db for username & password match
        user_info = account.query.filter_by(username=username).first()
        usern = user_info.username
        passwd = user_info.password
        if usern == username and passwd == password:
            return render_template('dashboard.html', form=form, 
            display_message='Remember logout when you are done.')
                
        return render_template('login.html', form=form,
                                                display_message='Incorrect Login')
    else:
        if 'user' in session:
            return render_template('dashboard.html', form=form, 
                                display_message='Remember logout when you are done.')
            
        return render_template('login.html', form=form, display_message='User Login')
  
##### PROFILE #####

@app.route('/dashboard/', methods=['GET', 'POST'])
def dashboard():
    if 'user' in session:
        # Create a query here that will get a list of symbols from the user's stocks column in the users table.
        stocks = account.query.filter_by(username=session['user']).first()
        return render_template('dashboard.html', stocks=stocks)
    else:
        form = LoginForm()
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

        user_info = account.query.filter_by(username=username).first()
        usern = user_info.username
        if usern == username:
            user_info.password = password
            user_info.email = email
            user_info.stocks = stocks
            db.session.commit()
            return render_template('dashboard.html', form=uform, 
                                 display_message='Successfully updated your info')
                
        else:
            return render_template('update.html', form=uform, 
                                        display_message='Wrong user name')

        
    return render_template('update.html', form=uform)

##### LOGOUT #####

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    lform = LogoutForm()
    if lform.validate_on_submit():
        session.pop('user', None)
        return render_template('home.html', form=lform, 
                                        display_message='Successfully logged out')
    else:
        return render_template('dashboard.html')

##### RUN APP #####

if __name__=='__main__':
    app.run(debug=True)
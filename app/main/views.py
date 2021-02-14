from flask import render_template, redirect, session, url_for
from app import db
from app.main import main_bp
from app.models import Ticker, Account
from app.main.forms import LoginForm, LogoutForm, UpdateForm, SignUpForm
from app.services.ticker import TService


@main_bp.route('/')
def home():
    return render_template('home.html')


@main_bp.route('/dashboard/', methods=['GET', 'POST'])
def dashboard():
    if 'user' in session:
        # Grab user data
        user_data = Account.query.filter_by(username=session['user']).first()
        # Get stock ticker data for the symbols they follow
        stocks = TService.ticker_data(user_data)
        return render_template('dashboard.html', stocks=stocks, loform=LogoutForm(), uform=UpdateForm())
    else:
        return render_template('login.html', form=LoginForm(), display_message='User Login')


@main_bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    # lform = LoginForm()
    # if 'user' in session:
    #     return render_template('dashboard.html', form=lform, 
    #                         display_message='You are stil logged in.')
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
            return redirect(url_for('user_bp.login'))
        
        # If the username already exists, go back to the signup form with empty fields.
        sform = SignUpForm()
        return render_template('signup.html', form=sform, display_message='Please try a different username.')

    # When navigating to the signup page (no post request)
    return render_template('signup.html', form=sform)


@main_bp.route('/login/', methods=['GET', 'POST'])
def login():
    # Load loginform and assign both fields to local variables
    lform = LoginForm()
    sform = SignUpForm()
    username = lform.username.data
    password = lform.password.data

    # If the user is logged in already, send them back to their dashboard
    if 'user' in session:
       return redirect(url_for('main_bp.dashboard'))

    # When the login form is submitted
    if lform.validate_on_submit():

        # Check db for username & password match
        user_info = Account.query.filter_by(username=username).first()
        
        if user_info == None:
            return render_template('signup.html', form=SignUpForm(), display_message='You\'re the first user! Sign up quick!')
        
        _username = user_info.username
        _password = user_info.password

        # If the username and password match the corresponding database account entry, start a user session
        if _username == username and _password == password:
            session.permanent=True
            session['user'] = username

            # Login successful
            return redirect(url_for('main_bp.dashboard'))
        
        # Login information could not be matched with username/password from account table in the DB
        return render_template('login.html', form=lform, display_message='Incorrect Login')

    # User just arrived at the login page and is not yet logged in to their account
    return render_template('login.html', form=lform, display_message='User Login')


@main_bp.route('/update/', methods=['GET', 'POST'])
def update():
    # TODO: Add user session check to make sure user is logged in
    # Currently, you can change someone's pass without logging in
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

        if _username == username:
            user_info.password = password
            user_info.email = email
            user_info.stocks = stocks
            db.session.merge(user_info)
            db.session.flush()
            db.session.commit()
            return redirect('/dashboard/')
        
        else:
            return render_template('update.html', form=uform, display_message="User doesn't exist")

    return render_template('update.html', form=uform)


@main_bp.route('/logout/', methods=['GET', 'POST'])
def logout():
    loform = LogoutForm()

    # If the logout button was clicked, remove user from session.
    if loform.validate_on_submit():
        session.pop('user', None)
        return render_template('home.html', form=loform, display_message='You are logged out')

    else:
        return render_template('dashboard.html')



# Add a new symbol to track in DB
@main_bp.route("/add", methods=["POST"])
def add():

    # TODO: Get list of user's symbols and check for added symbol, if exists, return to dashboard
    # TODO: Check if added symbol exists in ticker table
        # Create new ticker OR Retrieve ticker entry
        # Update user stocks

    return


# Delete a symbol being tracked in DB             
@main_bp.route("/delete/<int:ticker_id>")
def delete(ticker_id):

    # TODO: Pop from user's symbols, but do not remove from the db

    return
from flask import render_template, redirect, session, url_for, request
from app import db
from app.main import main_bp
from app.models import Account
from app.main.forms import LoginForm, LogoutForm, UpdateForm, SignUpForm
from app.services.ticker_svc import TService
from app.services.user_svc import UService


@main_bp.route('/')
def home():
    return render_template('home.html')


@main_bp.route('/signup/', methods=['GET', 'POST'])
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


# If the logout button was clicked, remove user from session.
@main_bp.route('/logout/', methods=['GET', 'POST'])
def logout():
    loform = LogoutForm()
    if loform.validate_on_submit():
        session.pop('user', None)
        return render_template('home.html', form=loform, display_message='You are logged out')

    else:
        return render_template('dashboard.html')


# Get stock ticker data and render dashboard
@main_bp.route('/dashboard/', methods=['GET', 'POST'])
def dashboard():
    user = UService.get_data()
    if 'user' in session and user:
        # Takes user data as an input, gets followed symbols, retrieve ticker data
        user_symbols = UService.get_symbols(UService.get_data())
        ticker_data = TService.ticker_data(user_symbols)
        return render_template('dashboard.html', stocks=ticker_data, loform=LogoutForm(), uform=UpdateForm())
    # Not logged in
    else:
        session.pop('user', None)
        return render_template('login.html', form=LoginForm(), display_message='User Login')


# Add a new symbol to track in DB
@main_bp.route("/add/", methods=["POST"])
def add():
    symbol = request.form['symbol']
    user_symbols = UService.get_symbols(UService.get_data())
    if(symbol not in user_symbols):
        UService.add_ticker(UService, symbol)
    return redirect(url_for('main_bp.dashboard'))


# Delete the symbol from user's followed symbols
@main_bp.route("/delete/<symbol>")
def delete(symbol):
    user_symbols = UService.get_symbols(UService.get_data())
    UService.delete_ticker(UService, user_symbols, symbol)
    return redirect(url_for('main_bp.dashboard'))
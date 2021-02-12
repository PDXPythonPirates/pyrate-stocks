from flask import render_template, redirect, session
from app.main import user
from app.models import Ticker, Account
from app.main.forms import LoginForm, LogoutForm, UpdateForm, SignUpForm


@user.route('/signup/', methods=['GET', 'POST'])
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
            return render_template('dashboard.html', loform=LogoutForm(), uform=UpdateForm(), display_message='Welcome to Financial App!')
        
        # If the username already exists, go back to the signup form with empty fields.
        sform = SignUpForm()
        return render_template('signup.html', form=sform, display_message='Please try a different username.')

    # When navigating to the signup page (no post request)
    return render_template('signup.html', form=sform)


@user.route('/login/', methods=['GET', 'POST'])
def login():
    # Load loginform and assign both fields to local variables
    lform = LoginForm()
    sform = SignUpForm()
    username = lform.username.data
    password = lform.password.data

    # If the user is logged in already, send them back to their dashboard
    if 'user' in session:
       return render_template('dashboard.html', loform=LogoutForm(), uform=UpdateForm(), display_message='You are already logged in!')

    # When the login form is submitted
    if lform.validate_on_submit():

        # Check db for username & password match
        user_info = Account.query.filter_by(username=username).first()
        
        if user_info == None:
            return render_template('signup.html', form=SignUpForm(), display_message='You\'re the first user! Sign up quick!')
        elif 'user' in session:
            return render_template('dashboard.html', loform=LogoutForm(), uform=UpdateForm(), display_message='Remember logout when you are done --')
        
        _username = user_info.username
        _password = user_info.password

        # If the username and password match the corresponding database account entry, start a user session
        if _username == username and _password == password:
            session.permanent=True
            session['user'] = username

            # Login successful
            return render_template('dashboard.html', loform=LogoutForm(), uform=UpdateForm(), display_message='Welcome back!')
        
        # Login information could not be matched with username/password from account table in the DB
        return render_template('login.html', form=lform, display_message='Incorrect Login')

    # User just arrived at the login page and is not yet logged in to their account
    return render_template('login.html', form=lform, display_message='User Login')


@user.route('/update/', methods=['GET', 'POST'])
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


@user.route('/logout/', methods=['GET', 'POST'])
def logout():
    loform = LogoutForm()

    # If the logout button was clicked, remove user from session.
    if loform.validate_on_submit():
        session.pop('user', None)
        return render_template('home.html', form=loform, display_message='You are logged out')

    else:
        return render_template('dashboard.html')

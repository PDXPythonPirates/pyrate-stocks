from flask import Flask, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap
from forms import LoginForm, LogoutForm, SignUpForm
from keychain import Keys
import json


app = Flask(__name__, template_folder='../templates')
app.config['SECRET_KEY'] = Keys.secret()
Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def home():

    return render_template('home.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check user_data.json for username & password match
        file = open('user_data.json',)
        data = json.load(file)
        
        # Not sure if the second check is a real thing. I think this will throw an error.
        if username in data['users']['username'].values() and password == data['users'][username]['password']:
            print(f'successful login for {username}.')
            file.close()
            return render_template('profile.html', form=form, username=username, display_message=f'Welcome, {username}')
        else:
            return render_template('login.html', form=form, display_message='Incorrect Login')

    return render_template('login.html', form=form, display_message='User Login')


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    form = LogoutForm()
    
    if form.validate_on_submit():

        return render_template('home.html', form=form, display_message='Successfully logged out')
    else:
        
        return render_template('profile.html')


@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    form = LogoutForm()

    return render_template('profile.html', form=form)


@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        form = request.form

        # insert new user data into user_data.json here

        #

        return redirect(url_for('login'))

    return render_template('signup.html', form=form)


if __name__=='__main__':
    app.run(debug=True)
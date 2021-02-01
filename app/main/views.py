from flask import Flask, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap
from forms import LoginForm, LogoutForm, SignUpForm
from keychain import Keys
import csv
import json


app = Flask(__name__, template_folder='../templates')
app.config['SECRET_KEY'] = Keys.secret()
Bootstrap(app)

##### HOME #####

@app.route('/', methods=['GET', 'POST'])
def home():

    return render_template('home.html')


##### ADD USER #####

def append_user(file_name, user_data):
    with open(file_name, 'a+') as file:
        json.dump(user_data, file)


##### SIGNUP #####

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    print('signup page accessed')
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        user_data['users'] = {}
        user_data['users'][username] = {}
        user_data['users'][username]['password'] = password
        user_data['users'][username]['email'] = email

        append_user('app/main/user_data.json', user_data)

        return redirect(url_for('login'))

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
            users = data['users']
            print('all users: ', users)

            for user, user_data in users.items():
                print('user: ', user, user_data)
                if user == username and password == user_data['password']:
                    return render_template('profile.html', form=LogoutForm(), username=username, display_message=f'Welcome, {username}')
                else:
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


##### RUN APP #####

if __name__=='__main__':
    app.run(debug=True)
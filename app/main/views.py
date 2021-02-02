from flask import Flask, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap
from app.main.forms import SignUpForm, LoginForm, ProfileForm, UpdateForm
from app.main.keychain import Keys
import csv
import json


app = Flask(__name__, template_folder='../templates')
app.config['SECRET_KEY'] = Keys.secret()
Bootstrap(app)

##### HOME #####

@app.route('/', methods=['GET', 'POST'])
def home():

    return render_template('home.html')


##### SIGNUP #####

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

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
                    return render_template('profile.html', form=form, display_message='Login Success!')
        
        return render_template('login.html', form=form, display_message='Incorrect Login')
    return render_template('login.html', form=form, display_message='User Login')
##### PROFILE #####

@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    form = ProfileForm()

    return render_template('profile.html', form=form)


##### UPDATE-LOGOUT #####

@app.route('/update_logout/', methods=['GET', 'POST'])
def update_logout():
    form = ProfileForm()
    
    if form.validate_on_submit():
        if request.form.action == 'Update':
            return render_template('update.html', form=form, display_message='Update User Info.')
        elif request.form.action == 'Logout':
            return render_template('home.html', form=form, display_message='Successfully logged out')
    return render_template('profile.html')

@app.route('/update/', methods=['GET', 'POST'])
def update():
    form = UpdateForm()
    if form.validate_on_submit():
        return render_template('update.html', form=form)
    return render_template('profile.html')

##### RUN APP #####

if __name__=='__main__':
    app.run(debug=True)
from flask import Flask, render_template, redirect, session
from flask_bootstrap import Bootstrap
from forms import SignUpForm, LoginForm, UpdateForm, LogoutForm
from datetime import timedelta
from keychain import Keys
import json

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = Keys.secret()
app.permanent_session_lifetime = timedelta(days = 1)
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
        session.permanent=True
        username = form.username.data
        password = form.password.data
        session['user'] = username

        # Check user_data.json for username & password match
        with open('app/main/user_data.json', 'r') as file:
            data = json.load(file)
            all_users = data['users']

            for user in all_users:
                _username = list(user.keys())[0]
                if username == _username and password == user[_username]['password']:
                    return render_template('profile.html', form=form, display_message='Login successfully')
                
            return render_template('login.html', form=form, display_message='Incorrect Login')
    else:
        if 'user' in session:
            return render_template('profile.html', form=form, display_message='Welcome back.')
            
        return render_template('login.html', form=form, display_message='User Login')
  
##### PROFILE #####

@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    if 'user' in session:
        return render_template('profile.html')
    else:
        form = LoginForm()
        return render_template('login.html', form=form, display_message='User Login')
    return render_template('profile.html')

##### UPDATE #####

@app.route('/update/', methods=['GET', 'POST'])
def update():
    uform = UpdateForm()
        
    if uform.validate_on_submit():
        username = uform.username.data
        password = uform.password.data
        email = uform.email.data

        with open('app/main/user_data.json', mode='r') as file:
            data = json.load(file)
            all_users = data['users']

            for user in all_users:
                _username = list(user.keys())[0]
                user_data = list(user.values())
               
                if username == _username:
                    user_data[0]['password'] = password
                    user_data[0]['email'] = email
                
                    with open('app/main/user_data.json', mode='w') as file:
                        data = {"users":all_users}
                        json.dump(data, file)

                    return render_template('profile.html', form=uform, display_message='Successfully updated your info')
                
            return render_template('update.html', form=uform, display_message='Wrong user name')

        return render_template('profile.html', form=uform, display_message='Successfully updated your info.')

    return render_template('update.html', form=uform)

##### LOGOUT #####

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    lform = LogoutForm()
    if lform.validate_on_submit():
        session.pop('user', None)
        return render_template('home.html', form=lform, display_message='Successfully logged out')
    else:
        return render_template('profile.html')

##### RUN APP #####

if __name__=='__main__':
    app.run(debug=True)
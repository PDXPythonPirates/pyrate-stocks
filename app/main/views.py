from flask import Flask, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap
from forms import LoginForm, LogoutForm, SignUpForm
from keychain import Keys
import csv


app = Flask(__name__, template_folder='../templates')
app.config['SECRET_KEY'] = Keys.secret()
Bootstrap(app)

##### HOME #####

@app.route('/', methods=['GET', 'POST'])
def home():

    return render_template('home.html')


##### ADD USER #####

def append_list_as_row(file_name, user_data):
    with open(file_name, 'a+', newline='') as file:
        print('test2', user_data)
        writer = csv.writer(file, delimiter=',')
        writer.writerow(user_data)


##### SIGNUP #####

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    print('signup page accessed')
    if form.validate_on_submit():
        print('test0')
        user_data = [form.username.data, form.password.data, form.email.data]
        print('test1', user_data)
        append_list_as_row('app/main/user_data.csv', user_data)

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
        with open('app/main/user_data.csv', 'r') as file:
            user = file.readline()
            user = list(user.split(','))
            user = [x.strip('\n') for x in user]

        
        # Not sure if the second check is a real thing. I think this will throw an error.
        if username == user[0] and password == user[1]:
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
from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_bootstrap import Bootstrap
from forms import LoginForm, LogoutForm
from keychain import Keys

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config['SECRET_KEY'] = Keys.secret()
    Bootstrap(app)
    return app
  
app = create_app()

#app.url_map.strict_slashes = False

# This route will bring you to the homepage.
# As of now, users are directed here after logging out.
@app.route('/', methods=['GET', 'POST'])
def base():

    return render_template('home.html')

# This route is accessable via the link on the homepage.
# login() will render a template, and if the form is submitted,
# the user will be directed to their profile, or back to the
# login template, if they entered incorrect information.
@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # Some user data to utilize before implementing a database
    users = {
        'matthias': {
            'password': 'thispass',
            'creation-date': '01/02/21',
            'location': 'Portland, OR'
        },
        'xuehong': {
            'password': 'anotherpass',
            'creation-date': '01/02/21',
            'location': 'Portland, OR'
        }
    }

    # Checks if the form is valid AND checks if the request was 'POST'.
    # If true, create a context for the user and render their profile.
    # Otherwise, go back to the login page.
    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')

        # Data that pertains to the user.
        context = {
                'form': form,
                'username': username,
                'display_message': f'Welcome, {username}',
                'followed_etfs': ['TSLA', 'AAPL', 'GOOGL', 'GOOG', 'FB', 'AMZN'],
            }

        # Check if the user exists and has entered the correct password.
        if username in users and password == users[username]['password']:
            return render_template('profile.html', context=context)
        # Does not exist or something was entered incorrectly.
        else:
            return render_template('login.html', form=form, display_message='Incorrect Login')

    # If the request was a 'GET' request, the login page will be rendered.
    return render_template('login.html', form=form, display_message='User Login')

# Load user profile.
@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    form = LogoutForm()

    # If POST request is sent via the logout button, render the homepage.
    # This needs work -- can't get it to render home with display message. ((Matthias))
    if form.validate_on_submit():
        print('logged out')
        return render_template('home.html', display_message='Successfully logged out')

    return render_template('profile.html')


# Run app
if __name__=='__main__':
    app.run(debug=True)
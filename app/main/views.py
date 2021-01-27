from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_bootstrap import Bootstrap
from forms import LoginForm
from keychain import Keys

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config['SECRET_KEY'] = Keys.secret()
    Bootstrap(app)
    return app
  
app = create_app()

#app.url_map.strict_slashes = False

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/home/')
def home():
    return render_template('home.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    data = request.json
    print(request.form)
    form = LoginForm()

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

    if form.validate():
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users and password == users[username]['password']:
            return render_template('profile.html', form=form, display_message='Thank you for the visit!')
        else:
            return render_template('login.html', form=form, display_message='Login Failed')

    return render_template('login.html', form=form, display_message='User Login')

# @app.route('/failed')
# def failed():
    # return '<h1>Failed attempt.</h1>'

@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    if form.validate():
        return render_template('home.html',form=form)


if __name__=='__main__':
    app.run(debug=True)
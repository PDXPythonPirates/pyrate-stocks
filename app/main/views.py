from flask import Flask, render_template, redirect, url_for, request
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
def home():
    return '<h1>Home Page</h1>'

@app.route('/login/')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/validate', methods=['GET', 'POST'])
def validate_user():

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

    if form.validate_on_submit():
        if username in users and password == users[username]['password']:
            return redirect('/')
        else:
            return redirect('/login')
    else:
        return redirect('/failed')

@app.route('/failed')
def failed():
    return '<h1>failed</h1>'
 
if __name__=='__main__':
    app.run(debug=True)
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap

def create_app():
    app = Flask(__name__, template_folder='../templates')
    Bootstrap(app)
    return app
  
app = create_app()
#app.url_map.strict_slashes = False

@app.route('/')
def home():
    return '<h1>Home Page</h1>'

@app.route('/login/', methods=['POST'])
def login():
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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and password == users[username]['password']:
            return redirect(url_for('/'))
        else:
            return redirect(url_for('/login/'))  
 
if __name__=='__main__':
    app.run(debug=True)
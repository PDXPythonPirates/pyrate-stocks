from flask import Flask, render_template, redirect

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def home():
    return '<h1>Home Page</h1>'

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login/<username>/<password>')
def verify_user(username, password, method=['POST']):
    
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

    if username in users and password == users[username]['password']:
        return redirect('/')
    else:
        return redirect('/login')

if __name__=='__main__':
    app.run(debug=True)

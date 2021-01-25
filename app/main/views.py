from flask import Flask, render_template, redirect

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def home():
    return '<h1>Home Page</h1>'

@app.route('/login/<username>/<password>')
def login(username, password):
    
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

    if username in users and users[username][password] == password:
        return redirect('/')

    return render_template('login.html')

if __name__=='__main__':
    app.run(debug=True)

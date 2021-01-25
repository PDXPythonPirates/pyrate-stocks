from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/login')
def login():
    context = {

    }
    return render_template('login.html')

@app.route('/home')
def home():
    return '<h1>Home Page </h1>'

@app.route('/about')
def about():
    return '<h1>About Page </h1>'

if __name__=='__main__':
    app.run(debug=True)

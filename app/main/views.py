from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Home Page </h1>'

@app.route('/login')
def login():
    context = {

    }
    return render_template('login.html')
    
if __name__=='__main__':
    app.run()

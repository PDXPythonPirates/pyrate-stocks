from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    # return '<h1>Hello World! </h1>'

@app.route('/home')
def home():
    return '<h1>Home Page </h1>'

@app.route('/about')
def about():
    return '<h1>About Page </h1>'

if __name__=='__main__':
    app.run(debug=True)


# lsof -i :5000
# kill -9 $(lsof -t -i:5000)
from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ... models import Account
from . import main
from .. forms import SignUpForm, LoginForm, UpdateForm, LogoutForm
import yfinance as yf # TODO: Verify that this import lives here

##### HOME #####

@main.route('/user')
def user():
    return "Hello, Hello, World!"

if __name__=='__main__':
    main.run(debug=True)
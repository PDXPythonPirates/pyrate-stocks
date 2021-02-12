from flask import Flask, render_template, redirect, session
from app.main import main # blueprints
from app.models import Ticker, Account
from app.main.forms import LoginForm, LogoutForm, UpdateForm


@main.route('/')
def home():
    return render_template('home.html')

@main.route('/dashboard/', methods=['GET', 'POST'])
def dashboard():
    lform = LoginForm()
    uform = UpdateForm()

    if 'user' in session:

        user_data = Account.query.filter_by(username=session['user']).first()
        symbols = user_data.stocks.replace(" ", "")
        symbols = symbols.split(",")
        stocks = []

        for s in symbols:
            ticker = yf.Ticker(s)
            current_price = ticker.info['bid']

            stock_data = {}
            stock_data['symbol'] = s
            stock_data['current_price'] = current_price

            stocks.append(stock_data)

        # Load dashboard and return stock ticker data
        return render_template('dashboard.html', stocks=stocks, loform=LogoutForm(), uform=UpdateForm())

    else:
        form = LoginForm()
        return render_template('login.html', form=form, display_message='User Login')



if __name__=='__main__':
    main.run(debug=True)
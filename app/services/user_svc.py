from flask import session
from app import db
from app.models import Account


class UService:

    # Retrieve user's session data
    def get_data():
        user_data = Account.query.filter_by(username=session['user']).first()
        return user_data

    # Get a list of symbols the user follows
    def get_symbols(self, user_data):

        # Turn string of symbols into list
        # NOTE: If the user entered a comma, it will produce 2 empty symbols
        symbol_list = user_data.stocks.replace(' ', '').split(',')
        new_symbols = []
        print('List of symbols to process: ' + str(symbol_list))

        # If the user accidentally put a comma at the end or beginning of their string,
        # this check will remove the empty symbols to prevent ticker data error
        for item in range(len(symbol_list)):
            if symbol_list[item] != '':
                if symbol_list[item] in new_symbols:
                    continue
                else:
                    new_symbols.append(symbol_list[item])
                    print('Index item ' + str(item) + ' is valid.')
            else:
                print('Index item ' + str(item) + ' is NOT valid.')
        
        # If there's an issue with the symbol list, update user symbols in db
        if not new_symbols:
            return symbol_list
        else:
            self.update_tickers(self, new_symbols)
            print('Updated list of symbols: ' + str(new_symbols))
            return new_symbols

    # Add a stock ticker symbol to the user's followed symbols
    def add_ticker(self, ticker):
        ticker = ticker.replace(' ', '')
        user = self.get_data()
        user.stocks = user.stocks + f',{ticker}'
        db.session.commit()

    # Update the list of stock ticker symbols the user follows
    def update_tickers(self, ticker_list):
        ticker_list = ','.join(ticker_list)
        user = self.get_data()
        user.stocks = ticker_list
        db.session.commit()

    # Delete stock ticker symbol from user's followed symbols
    def delete_ticker(self, user_symbols, symbol):
        symbol = symbol.lower()
        user_symbols.remove(symbol)
        UService.update_tickers(UService, user_symbols)
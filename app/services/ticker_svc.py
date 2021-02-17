import yfinance as yf
from app.services.user_svc import UserService

class TickerService:
    
    def ticker_data(symbols):
        ticker_data = []
        for s in symbols:
            s = s.upper()
            # Check for symbols short enough to exist
            if(len(s) <= 5):
                try:
                    # Create ticker object and try to retrieve ticker data
                    ticker = yf.Ticker(s)
                    current_price = ticker.info['bid']
                except (KeyError, ImportError) as e:
                    # Print the problem ticker to console and delete it from the user's followed tickers
                    print(f'Cannot fetch the {s} ticker info OR may not exist. Deleting from user\'s tickers.')
                    UserService.delete_ticker(UserService.get_symbols(), s)
                    ticker = None
                    pass
                
                # If the ticker was found, finish getting the data
                if(ticker):
                    stock_data = {}
                    stock_data['symbol'] = s
                    stock_data['current_price'] = current_price
                    ticker_data.append(stock_data)
            else:
                # Ticker is too long to exist and will be deleted
                print(f'Ticker symbol {s} was too long. Deleting from user\'s tickers.')
                UserService.delete_ticker(UserService, UserService.get_symbols(UserService.get_data()), s)

        return ticker_data
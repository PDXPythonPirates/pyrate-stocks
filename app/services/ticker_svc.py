import yfinance as yf


class TService:
    
    def ticker_data(symbols):
        ticker_data = []
        for s in symbols:
            try:
                ticker = yf.Ticker(s)
                current_price = ticker.info['bid']
                stock_data = {}
                stock_data['symbol'] = s
                stock_data['current_price'] = current_price
                ticker_data.append(stock_data)
            except KeyError:
                print(ticker_data)
                return ticker_data

        return ticker_data
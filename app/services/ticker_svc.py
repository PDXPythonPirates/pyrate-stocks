import yfinance as yf


class TService:
    
    def ticker_data(symbols):
        stocks = []
        for s in symbols:
            try:
                ticker = yf.Ticker(s)
                current_price = ticker.info['bid']
                stock_data = {}
                stock_data['symbol'] = s
                stock_data['current_price'] = current_price
                stocks.append(stock_data)
            except KeyError:
                print('couldn\'t find stock ticker data')
                return

        return stocks
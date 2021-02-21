from flask import flash
import yfinance as yf
import pandas as pd
from datetime import datetime
from bokeh.models import DatetimeTickFormatter
from bokeh.plotting import figure, output_file
from bokeh.embed import components
from bokeh.resources import CDN
from urllib.error import HTTPError, URLError
from app.services.user_svc import UserService

class TickerService:
    
    def ticker_data(symbols):

        if symbols == None:
            return None

        ticker_data = []
        for s in symbols:
            s = s.upper()
            # Check for symbols short enough to exist
            if(len(s) <= 5):
                try:
                    # Try to retrieve ticker data
                    ticker = yf.Ticker(s)
                    name = ticker.info['shortName']
                    current_price = ticker.info['bid']
                    high = ticker.info['regularMarketDayHigh']
                    low = ticker.info['regularMarketDayLow']
                    open = ticker.info['open']
                    close = ticker.info['previousClose']
                                                            
                except (KeyError, ImportError, HTTPError, URLError) as e:
                    # Print the problem ticker to console and delete it from the user's followed tickers
                    flash(f'Ticker {s} is not a valid entry. ')
                    UserService.delete_ticker(UserService.get_symbols(), s.lower())
                    ticker = None
                    pass
                
                # If the ticker was found, finish getting the data
                if ticker:
                    stock_data = {}
                    stock_data['symbol'] = s
                    stock_data['name'] = name
                    stock_data['current_price'] = current_price
                    stock_data['high'] = high
                    stock_data['low'] = low
                    stock_data['open'] = open
                    stock_data['close'] = close
                    ticker_data.append(stock_data)
            else:
                # Ticker is too long to exist and will be deleted
                flash(f'Ticker symbol {s} was too long. Deleting from user\'s tickers.')
                UserService.delete_ticker(UserService, UserService.get_symbols(UserService.get_data()), s)

        return ticker_data

    def plot(symbol):
        t = yf.Ticker(symbol)
        df = t.history('max')
        df = df.reset_index()
        df['Date'] = pd.to_datetime(df['Date'])

        p = figure(title ='Closing Price History', plot_width=1000, plot_height=300, tools='pan, box_zoom, wheel_zoom, reset')
        p.line(df.Date, df.Close, line_width=2)
        p.title.text_font_size = '20pt'
        p.xaxis.formatter = DatetimeTickFormatter(hourmin = ['%Y:%M'])
        p.xaxis.major_label_text_font_size = "14pt"
        p.yaxis.axis_label = symbol
        p.yaxis.axis_label_text_font_size = '18pt'
      
        p.yaxis.major_label_text_font_size = "14pt"
        p.yaxis[0].ticker.desired_num_ticks = 3
        script, div = components(p)
        cdn_js = CDN.js_files
        cdn_css = CDN.css_files
        
        return script, div, cdn_js[0], cdn_css
from flask import flash
from datetime import datetime
from bokeh.models import DatetimeTickFormatter, ColumnDataSource
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN
from urllib.error import HTTPError, URLError
from app.services.user_svc import UserService
import yfinance as yf
import pandas as pd
import sqlite3

class TickerService:


    def importCsvDb():

        # NOTE: CSV Source: https://www.nasdaq.com/market-activity/stocks/screener. 
        # To use a different csv, update the file below with either a .csv link or .csv file name
        # and place the csv in the csvfiles directory if applicable. 
        
        # Read original csv data
        symbolList = pd.read_csv("app/csvfiles/nasdaq_screener_1614500646091.csv", usecols=["Symbol", "Name"], index_col=['Symbol'])
        print("Reading csv columns ... ")

        # Parse original csv data to columns needed & save to new csv file
        symbolList.to_csv('app/csvfiles/symbolList.csv', index_label=None)
        print("Parsing csv ... ")

        # Open database connection
        con = sqlite3.connect("data-dev.sqlite3")
        cur = con.cursor()
        print("Connecting to database ...")

        # Database read csv 
        df = pd.read_csv("app/csvfiles/symbolList.csv")
        print("Reading csv file ...")

        # Import csv data into table
        df.to_sql(
            name='symbolList',
            con = con,
            index=False,
            if_exists='replace')
        print("Creating symbolList table in database ...")
            
        # Close database connection
        con.close()
        print("Closing database connection ...")
    

    def ticker_data(symbols):

        ticker_data = []
        for s in symbols:
            s = s.upper()
            if(len(s) <= 6):
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
                    flash(f'Ticker {s} is not a valid entry. ', 'alert')
                    UserService.delete_ticker(UserService.get_symbols(), s)
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
                flash(f'Ticker symbol {s} was too long.', 'alert')
                UserService.delete_ticker(UserService.get_symbols(), s)

        return ticker_data


    def plot(symbol):

        t = yf.Ticker(symbol)
        df = t.history('max')
        df = df.reset_index()
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
        df["DateString"] = df["Date"].dt.strftime("%Y-%m-%d")

        source = ColumnDataSource(df)
        _lineColor = (50, 207, 155, 1)
        _fontColor = (50, 207, 155, 1)

        p = figure(plot_width=1000, plot_height=300,
                    sizing_mode='scale_width',tools='pan, box_zoom, wheel_zoom, hover, reset',
                    tooltips = [("Date","@DateString"),("Close", "@Close")])

        p.line('Date', 'Close', line_width=2, source=source, line_color=_lineColor)
        
        p.xaxis.formatter = DatetimeTickFormatter(hourmin = ['%Y:%M'])

        p.yaxis.axis_label = symbol
        p.xaxis.major_label_text_font_size = "14pt"
        p.yaxis.axis_label_text_font_size = '18pt'
        p.yaxis.major_label_text_font_size = "14pt"
        p.yaxis[0].ticker.desired_num_ticks = 3

        p.border_fill_color = "#343a40"
        p.outline_line_color = "#343a40"
        p.yaxis.major_label_text_color = "#747d85"
        p.xaxis.major_label_text_color = "#747d85"
        p.yaxis.axis_label_text_color = "#747d85"

        p.background_fill_alpha = 0
        p.yaxis.axis_line_alpha = .3
        p.xaxis.axis_line_alpha = .3
        p.yaxis.minor_tick_line_alpha = .3
        p.xaxis.minor_tick_line_alpha = .3
        p.xgrid.grid_line_alpha = .3
        p.ygrid.grid_line_alpha = .3

        script, div = components(p)
        cdn_js = CDN.js_files
        cdn_css = CDN.css_files
        
        return script, div, cdn_js[0], cdn_css
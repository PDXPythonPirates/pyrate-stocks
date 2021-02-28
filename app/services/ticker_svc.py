from flask import flash
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
                    flash(f'Ticker {s} is not a valid entry. ')
                    UserService.delete_ticker(UserService.get_symbols(), s.upper())
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
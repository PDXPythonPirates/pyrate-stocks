## **About The Project** 

This app was created by the first cohort of the Python Pyrates Project, hosted by Matt Phillips and Chris Thompson. We are entry level software developers working together to explore the Flask framework and the software development lifecycle. This app provides an interactive dashboard for users to monitor up-to-date (and historical) stock inforamtion.

<br>

**Project Title**

*Pyrate Stocks*

<br>

**Built with**

[![Python](https://img.shields.io/badge/python-3.8.5-blue.svg)](https://www.python.org/downloads/release/python-385/) &emsp;
[![Flask](https://img.shields.io/badge/flask-1.1.2-blue.svg)](https://flask.palletsprojects.com/en/1.1.x/installation/)  


## **Getting Started**

- Create virtural environment \
  `conda create -n myenv python=3.8` or `python -m venv myenv`

- Activate virtural environment \
  `conda activate myenv` (conda environments) or \
  `myenv\Scripts\activate.bat` (Windows) \
  `source myenv/bin/activate` (Mac or Unix based) \

- Clone repository

		git clone https://github.com/PDXPythonPirates/python-pirates-project-cohort-1/tree/main

- Install requirements.txt

		pip install -r requirements.txt


## **Features**

- Anonymous users are presented with Home, Login, and Signup options.

- If a new user attempts to login, they will be directed to the signup page.
 
- After signup, the user is directed to the login page. Any existing users can go diretly to the login page.
 
- After login, the user can navigate to Home, Dashboard, Update, and Logout pages.

- On the Dashboard page: 
 	- The user is presented with the curent information on stocks they selected.  With any ticker the user chooses to follow, the stocks' current price, high, low, open, and close is pulled via the [yFinance](https://pypi.org/project/yfinance/) package that scrapes data from Yahoo! Finance. *Please note: Some tickers are not possible to add on the dashboard due to limitations based on the yFinance Package.*
	
	- The user has options to add and delete stock tickers, and view historical data. 
	
	- In the add ticker input field, the user is presented with recommended tickers as they type in different characters. Suggested tickers are pulled from a .csv file downloaded from [nasdaq.com](https://www.nasdaq.com/market-activity/stocks/screener). The user also has the ability to manually enter a ticker that does not appear in the suggestions.

- On the Update page, the user can change username, password, email and enter stock symbols.  The form is preloaded with username, email and any stocks in the account. *This inforamtion was preloaded with the assumption that they typically don't change. If user enters new inforamtion, it will be saved.*

- The user stays logged in until the user decides to log out.  

## **Resources**

[Portland Python Pirates](https://github.com/PDXPythonPirates) \
[Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/)  \
[Hackers and Slackers' Flask Series](https://hackersandslackers.com/series/build-flask-apps/) \
[Miguel Grinberg's Dev Blog](https://blog.miguelgrinberg.com/category/Flask)  \
[Miguel Gringerg's Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)  \
[Nasdaq Symbol List](https://www.nasdaq.com/market-activity/stocks/screener) \
[Pandas Documentation](https://pandas.pydata.org/pandas-docs/stable/user_guide/index.html)\
[yFinance Package](https://pypi.org/project/yfinance/)

## **Special Thanks**

Thank you, Chris Thompson and Matt Phillips, for hosting the **Python Pyrates Project Cohort 1**! We greatly appreciate your guidance and support throughout the creation of this app, as well as the opportunity to experience the software lifecycle on a real-world application.


## **License**

[MIT License](https://opensource.org/licenses/MIT)

Copyright (c) 2021 Portland Python Pirates

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

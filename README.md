## **About The Project** 
We, the **python-pirates-project-cohort-1** greatly appreciate Chris Thompson and Matt Phillips for guiding us through the creation of this app and enabling us to experience the typical workflow for software development.  

This app provides an interactive dashboard for users to monitor up-to-date stock inforamtion of their choice.  Users can also choose to view historical data on stocks of their interest.

<br>

**Project Title**

*A Personal Investment App*

<br>

**Built with**

[![Python](https://img.shields.io/badge/python-3.8.5-blue.svg)](https://www.python.org/downloads/release/python-385/) &emsp;
[![Flask](https://img.shields.io/badge/flask-1.1.2-blue.svg)](https://flask.palletsprojects.com/en/1.1.x/installation/)  

<br>

## **Getting Started**

- Create virtural environment
	 
	- _Method 1_:

			conda create -n myenv python=3.8    
		
	- _Method 2_:

			python -m venv myenv

- Activate virtural environment
	- _Method 1_: 

			conda activate myenv

	- _Method 2_: 
		- Windows

				myenv\Scripts\activate.bat

		- Unix or MacOS

				source myenv/bin/activate	

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


## **License**

MIT License

Copyright (c) 2021 Portland Python Pirates

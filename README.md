## **About The Project**

**Project Title**

A Personal Investment App

**Built with**
- Python 3.8.5
- Flask 1.1.2
	
**Getting Started**

**1**. Prerequisites

- create virtural environment
	 
	- _Method 1_:  from cmd or terminal, run

			`conda create -n myenv python=3.8`.    
		_Note: python3.8 was the version used to create this app_

	- _Method 2_: from cmd or terminal, run

			`python3 -m venv myenv`.

- Activate virtural environment**

	- _Method 1_: from cmd or terminal, run 

			`conda activate myenv`

	- _Method 2_: 

		- on Windows, run 
	
			`myenv\Scripts\activate.bat`

		- on Unix or MacOS, run 

			`source myenv/bin/activate`	

**Installation**

**1**. Clone repo. From cmd or terminal, run

		git clone https://github.com/PDXPythonPirates/python-pirates-project-cohort-1/tree/main

**2**. Install requiremnets. From cmd or terminal, run  

		pip3 install -r requirements.txt


## **Features**

**1**. Annonomous users are presented with Home, Login and Signup options on the menu bar.

**2**. If a new user attempted to login, they will be directed to the signup page.

**3**. After signup, the user is directed to login page to login.  Any existing user can go diretly to the login page.

**4**. After login, the user has options for Home, Dashboard, Update and Logout pages.

**5**. On the Dashboard page, the user is presented with the curent information on stocks they selected.  The user has options to add and delete stocks (tickers).

**6**. On the Update page, the user can change username, password, email and enter stocks symbols.   The form is preloaded with username, email and any stocks in the account.  *These inforamtion was preloaded with the assumption that they typically don't change.  But if user enters new inforamtion, it will be saved.*

**7**. The user stays logged in as log as the logout option is not chosen.   

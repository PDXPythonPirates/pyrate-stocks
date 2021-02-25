## **About The Project** 
We, the **python-pirates-project-cohort-1** greatly appreciate Chris Thompson and Matt Phillips for guiding us through the creation of this app and enable us to experience the typical workflow for software development.  

This app provides an interactive dashboard for users to monitor up-to-date stocks inforamtion of their choices.  Users can also choose to plot historical data for stock of their interest.

<br>

<a href="/PDXPythonPirates/python-pirates-project-cohort-1/graphs/contributors" class="Link--primary no-underline "> <mark>Contributors</mark> &emsp;   <span title="5" class="Counter ">5</span> &emsp; </a> <mark>Star</mark> &emsp;
<a class="social-count js-social-count" href="/PDXPythonPirates/python-pirates-project-cohort-1/stargazers" aria-label="0 users starred this repository">0</a> &emsp;<span class="btn btn-sm btn-with-count disabled tooltipped tooltipped-sw" aria-label="Cannot fork because forking is disabled.">
            <svg class="octicon octicon-repo-forked" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M5 3.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm0 2.122a2.25 2.25 0 10-1.5 0v.878A2.25 2.25 0 005.75 8.5h1.5v2.128a2.251 2.251 0 101.5 0V8.5h1.5a2.25 2.25 0 002.25-2.25v-.878a2.25 2.25 0 10-1.5 0v.878a.75.75 0 01-.75.75h-4.5A.75.75 0 015 6.25v-.878zm3.75 7.378a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm3-8.75a.75.75 0 100-1.5.75.75 0 000 1.5z"></path></svg><mark>Fork</mark> &emsp; <a href="/PDXPythonPirates/python-pirates-project-cohort-1/network/members" class="social-count" aria-label="0 users forked this repository">0</a>
			
			
<br>

**Project Title**

*A Personal Investment App*

<br>

**Built with**

[![Python](https://img.shields.io/badge/python-3.8.5-blue.svg)](https://www.python.org/downloads/release/python-385/) &emsp;
[![Flask](https://img.shields.io/badge/flask-1.1.2-blue.svg)](https://flask.palletsprojects.com/en/1.1.x/installation/)  

<br>

**Getting Started**

- create virtural environment
	 
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

- Clone repo

		git clone https://github.com/PDXPythonPirates/python-pirates-project-cohort-1/tree/main

- Install requirements.txt

		pip install -r requirements.txt

<br>

## **Features**

- Anonymous users are presented with Home, Login, and Signup options .
- If a new user attempted to login, they will be directed to the signup page.
- After signup, the user is directed to the login page. Any existing users can go diretly to the login page.
- After login, the user can navigate to Home, Dashboard, Update, and Logout pages.
- On the Dashboard page, the user is presented with the curent information on stocks they selected. The user has options to add and delete stock tickers, and to plot historical data.
- On the Update page, the user can change username, password, email and enter stock symbols.  The form is preloaded with username, email and any stocks in the account. *These inforamtion was preloaded with the assumption that they typically don't change. But if user enters new inforamtion, it will be saved.*
- The user stays logged in unless logout was performed.   

## **Resources**
[Portland Python Pirates](https://github.com/PDXPythonPirates)
[Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/)
[Miguel Grinberg's Dev Blog](https://blog.miguelgrinberg.com/category/Flask)
[Miguel Gringerg's Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
[Hackers and Slackers' Flask Series](https://hackersandslackers.com/series/build-flask-apps/)


## **License**

MIT License

Copyright (c) 2021 Portland Python Pirates
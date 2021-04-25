# **Pyrate Stocks**

A simple investment application built with Flask and Python | [Explore the docs >>](https://github.com/PDXPythonPirates/python-pirates-project-cohort-1)


## **Table of Contents**

<details>
	<summary>Click to expand!</summary>

- [About the Project](https://github.com/PDXPythonPirates/python-pirates-project-cohort-1/blob/main/README.md#about-the-project)

- [Built With](https://github.com/PDXPythonPirates/python-pirates-project-cohort-1/blob/main/README.md#built-with)

- [Getting Started](https://github.com/PDXPythonPirates/python-pirates-project-cohort-1/blob/main/README.md#getting-started)
	
- [Features](https://github.com/PDXPythonPirates/python-pirates-project-cohort-1/blob/main/README.md#features)

- [Styling](https://github.com/PDXPythonPirates/python-pirates-project-cohort-1#styling)

- [Contributors](https://github.com/PDXPythonPirates/python-pirates-project-cohort-1/blob/main/README.md#contributors)

- [Resources](https://github.com/PDXPythonPirates/python-pirates-project-cohort-1/blob/main/README.md#resources)

- [Special Thanks](https://github.com/PDXPythonPirates/python-pirates-project-cohort-1/blob/main/README.md#special-thanks)

- [License](https://github.com/PDXPythonPirates/python-pirates-project-cohort-1/blob/main/README.md#license)

</details>


## **About The Project** 

This app was created by the first cohort of the Python Pyrates Project, hosted by Matt Phillips and Chris Thompson. We are entry level software developers working together to explore the Flask framework and the software development lifecycle. This app provides an interactive dashboard for users to monitor up-to-date (and historical) stock information.


## **Built with:**

* [![Python](https://img.shields.io/badge/python-3.8.5-blue.svg)](https://www.python.org/downloads/release/python-385/)
* [![Flask](https://img.shields.io/badge/flask-1.1.2-blue.svg)](https://flask.palletsprojects.com/en/1.1.x/installation/)  
* [![Bootstrap](https://img.shields.io/badge/bootstrap-v5.0-blue)](https://getbootstrap.com/docs/5.0/getting-started/introduction/)


## **Getting Started**

### **Clone repository**

    $ git clone https://github.com/PDXPythonPirates/pyrate-stocks.git

* Navigate to the project folder

      $ cd pyrate-stocks
      
### **Download Docker, Build Image, Run Container**

* **Download Docker Desktop:** In order to run the Docker container, you’ll need to install Docker then have it open on your local machine. There are versions available for Linux, Max, and Windows. Download the Docker desktop application: https://www.docker.com/get-started. 
     
     * **VSCode (Extra/Not Required)** If you’re using VScode, the docker extension can also be utilized, however, Docker Desktop will still need to run in the background in order to build the image and run the container.

     * **What is Docker?** Docker is a platform for building, running, and shipping applications. Docker packages up an application with everything it needs and allows an app to run and function the same way on any user's local machine.

* Build Docker Image

      $ docker build -t pyrate-stocks .

* Run Docker Container

      $ docker run -p 8080:5000 pyrate-stocks
    
### Run Application

* Open a web browser and go to http://localhost:8080/ \
(Note: This is a development server. Do not use it in a production deployment)

### Editing the Application

When changes are made to the application, the Docker image and container will need to be rebuilt. Note: If testing multiple changes, Run and Debug Mode is recommended for efficiency, then the container image can be rebuilt. 

* The docker container can be stopped manually via the VSCode extension or using the stop command. You will need the container ID to use the stop command.

      # Find container ID
      $ docker ps
      
      # Stop container running
      $ docker stop <ContainerID>

* After edits are madeto the application, rebuild the container image with the build command and run the container again (see "Download Docker, Build Image, Run Container" for commands).

## **Features**

- Anonymous users are presented with Home, Login, and Signup options.

- If a new user attempts to login, they will be directed to the signup page.
 
- After signup, the user is directed to the login page. Any existing users can go diretly to the login page.
 
- After login, the user can navigate to Home, Dashboard, Update, and Logout pages.

- On the Dashboard page: 
 	- The user is presented with the curent information on stocks they selected.  With any ticker the user chooses to follow, the stocks' current price, high, low, open, and close is pulled via the [yFinance](https://pypi.org/project/yfinance/) package that scrapes data from Yahoo! Finance. *Please note: Some tickers are not possible to add on the dashboard due to limitations based on the yFinance Package.*
	
	- The user has options to add and delete stock tickers, and view historical data. 
	
	- In the add ticker input field, the user is presented with recommended tickers as they type in different characters. Suggested tickers are pulled from a .csv file downloaded from [nasdaq.com](https://www.nasdaq.com/market-activity/stocks/screener). The user also has the ability to manually enter a ticker that does not appear in the suggestions.

- On the Update page, the user can change username, password, email and enter stock symbols.  The form is preloaded with username, email and any stocks in the account. *This inforamtion was preloaded with the assumption that they typically don't change. If user enters new information, it will be saved.*

- The user stays logged in until the user decides to log out.  

## **Styling**

[Bootstrap](https://getbootstrap.com/) and [LESS](http://lesscss.org/) were used for styling. Bootstrap uses class based styling and LESS is a CSS preprocessor. If you're using VSCode, download the Easy LESS extension by mrcrowl. This extension will allow you to easily work with LESS files in VSCode. If you're using another text editor, you'll want to search for a LESS compiler that will compile .less files to .css. 

- To modify the main color palette of the layout, modify the palette.less file.

- The mixins.less file holds parametric mixins. [Mixins](http://lesscss.org/#mixins) hold one or more parameters that are used to extend functionality of LESS by taking arguments and its properties and customize the mixin output when mixed into another block. Mixins also help minimize lines of repeat code. With parametric mixins, you can also create a library of your own frequently used styling, that can be used across other projects.

## **Resources**

- [Portland Python Pirates](https://github.com/PDXPythonPirates)
- [Bootstrap Documentation](https://getbootstrap.com/)
- [Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/)
- [Hackers and Slackers' Flask Series](https://hackersandslackers.com/series/build-flask-apps/)
- [Miguel Grinberg's Dev Blog](https://blog.miguelgrinberg.com/category/Flask)
- [Miguel Gringerg's Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Nasdaq Symbol List](https://www.nasdaq.com/market-activity/stocks/screener)
- [Pandas Documentation](https://pandas.pydata.org/pandas-docs/stable/user_guide/index.html)
- [yFinance Package](https://pypi.org/project/yfinance/)

## **Contributors**

- [Matthias Wheelhouse](https://www.linkedin.com/in/mattiwheels/)
- [Jessica Cassidy](https://www.linkedin.com/in/cassjs/)
- [Xuehong Liu](https://www.linkedin.com/in/xuehong-liu/)
- [Matt Griffes](https://www.linkedin.com/in/matthewgriffes/)

## **Special Thanks**

Thank you, Chris Thompson and Matt Phillips, for hosting the **Python Pyrates Project Cohort 1**! We greatly appreciate your guidance and support throughout the creation of this app, as well as the opportunity to experience the software lifecycle on a real-world application.

We encourage any interested developers - regardless of experience - to apply for the next cohort. This is was an amazing experience for all four of us.

## **License**

[MIT License](https://opensource.org/licenses/MIT)

Copyright (c) 2021 Portland Python Pirates

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

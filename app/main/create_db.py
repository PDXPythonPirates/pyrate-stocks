# create database
from views import db
db.create_all()

""" 
# create a new user
The following commands need to be issued on python command line one by one.
from views import db
from views import Account
xuehong = Account(username='xuehong', email='xuehong@example.com', password='qqq', stocks='aapl')
db.session.add(xuehong)
db.session.commit()
# check account entries
u=Account.query.filter_by(username='xuehong').first()
u.username
"""
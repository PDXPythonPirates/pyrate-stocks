
from views import db
db.create_all()

""" 
The following commands need to be issued on python command line one by one.

from views import account
xuehong = account(username='xuehong', email='xuehong@example.com',password = 'qqq', stocks = 'aapl')

db.session.add(xuehong)
db.session.commit()

# check account entries
u=account.query.filter_by(username='xuehong').first()
u.username

"""
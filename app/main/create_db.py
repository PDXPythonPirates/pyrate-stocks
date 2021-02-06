from views import db

# create the database and the db tables
db.create_all()

from views import account
xuehong = account(username='xuehong', email='xuehong@example.com',password = 'qqq', stocks = 'aapl')

# commit the changes

db.session.add(xuehong)
db.session.commit()

account.query.all()
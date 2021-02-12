from flask import Blueprint

main = Blueprint('main', __name__)
ticker = Blueprint('ticker', __name__, url_prefix='/ticker')
user = Blueprint('user', __name__, url_prefix='/user')

from app.services import views, ticker, user
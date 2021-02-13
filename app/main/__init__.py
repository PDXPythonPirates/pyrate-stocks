from flask import Blueprint

main_bp = Blueprint('main_bp', __name__)
ticker_bp = Blueprint('ticker_bp', __name__, url_prefix='/ticker')
user_bp = Blueprint('user_bp', __name__, url_prefix='/user')

from app.main import views
from app.services import ticker, user
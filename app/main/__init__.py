from flask import Blueprint

main = Blueprint('main', __name__)

from .services import user, ticker
from .services import views
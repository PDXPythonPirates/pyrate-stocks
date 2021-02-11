from app.main.services.user import user
from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from .services import user
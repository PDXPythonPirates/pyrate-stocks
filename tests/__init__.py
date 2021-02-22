from flask import Blueprint

pytest_bp = Blueprint('pytest_bp', __name__)

from app.main import views
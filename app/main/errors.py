from flask import render_template
from app import db
from app.main import main_bp

@main_bp.app_errorhandler(403)
def not_found_error(error):
    return render_template('403.html'), 403

@main_bp.app_errorhandler(404)
def forbidden_error(error):
    return render_template('404.html'), 404

@main_bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
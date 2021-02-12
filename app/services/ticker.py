from flask import redirect
from ..main import main
from . import user

@main.route('/ticker')
def ticker():
    return redirect('/user')
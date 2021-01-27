from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    submit = SubmitField('Submit')
    logout = SubmitField('Submit')

class LogoutForm(FlaskForm):
    logout = SubmitField('Submit')

# this file was grayed out after pull

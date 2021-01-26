from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
    name = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    submit = SubmitField('Submit')


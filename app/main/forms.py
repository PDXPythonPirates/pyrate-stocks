from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=2, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=2, max=15)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=20)])
    stocks = StringField('stocks', validators=[ Length(min=2, max=32)])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    submit = SubmitField('Login')

class UpdateForm(SignUpForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=2, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=2, max=15)])
    email = StringField('Email')
    update = SubmitField('Submit')

class LogoutForm(FlaskForm):
    logout = SubmitField('Submit')
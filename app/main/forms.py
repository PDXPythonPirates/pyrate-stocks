from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    submit = SubmitField('Submit')
    logout = SubmitField('Submit')

class LogoutForm(FlaskForm):
    logout = SubmitField('Submit')

class SignUpForm(FlaskForm):
    # Data fields that connect to inputs fields on signup.html in templates.
    username = StringField('Username', validators=[InputRequired(), Length(min=2, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=2, max=15)])
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=20)])
    phone = StringField('Phone')
    address = StringField('Address')
    addressLine2 = StringField('Address Line 2')
    city = StringField('City')
    state = StringField('State')
    zipcode = StringField('Zip Code')
    submit = SubmitField('Submit')
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
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=15)])
    firstname = StringField('First Name', validators=[InputRequired()])
    lastname = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=20)])
    phone = StringField('Phone', validators=[InputRequired()])
    address = StringField('Address', validators=[InputRequired()])
    apt = StringField('Apartment#', validators=[InputRequired()])
    city = StringField('City', validators=[InputRequired()])
    state = StringField('State', validators=[InputRequired()])
    zipcode = StringField('Zip Code', validators=[InputRequired()])
    # Submit Button
    submit = SubmitField('Submit')
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, InputRequired, ValidationError, Length, Email
from app.models import Account

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=2, max=15)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=30)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=2, max=15)])
    stocks = StringField('stocks', validators=[ Length(min=2, max=50)])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = Account.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = Account.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class UpdateForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=2, max=15)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=30)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=2, max=15)])
    stocks = StringField('stocks', validators=[ Length(min=2, max=50)])
    submit = SubmitField('Submit')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', 
                        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class LogoutForm(FlaskForm):
    logout = SubmitField('Submit')
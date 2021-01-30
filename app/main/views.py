from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length
from keychain import Keys

app = Flask(__name__, template_folder='../templates')

# class SignUpForm is conntected to signup.html in templates
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

# routes to index.html page in templates.
@app.route('/index')
def home():
    return render_template('index.html')

# routes to signup.html page. On click of Submit button, data renders to user.html in templates.
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.is_submitted():
        result = request.form
        return render_template('user.html', result=result)
    return render_template('signup.html', form=form)

# routes to profile.html page in templates.
@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)
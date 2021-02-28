from flask import render_template
from flask_mail import Message
from config import Config
from app.main.forms import ResetPasswordForm
from app import mail


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    print('useremail for send_password_reset_email function in email.py=', user.email)
    send_email('Reset Your Password',
               sender=Config.ADMINS[0],
               recipients=[user.email],
               text_body=render_template('reset_password.txt', user=user, token=token),
               html_body=render_template('reset_password.html', user=user, token=token, form=ResetPasswordForm()))


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
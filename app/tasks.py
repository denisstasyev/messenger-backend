from flask_mail import Message
from datetime import datetime
from sqlalchemy import and_
from flask import render_template

from app import app, celery, mail

from .models import User


@celery.task(name="send_email", time_limit=60)
def send_email(subject, recipients, body, html):
    msg = Message(
        subject,
        sender=("STD-messenger", app.config["ADMINS"][0]),
        recipients=recipients,
    )
    msg.body = body
    msg.html = html
    with app.app_context():
        mail.send(msg)


@celery.task(name="send_email_birthday")
def send_email_birthday():
    now = datetime.utcnow
    users = User.query.filter(
        and_(User.birth_date.day == now.day, User.birth_date.month == now.month)
    )
    for user in users:
        send_email.apply_async(
            (
                "Happy Birthday",
                [user.email],
                "Happy Birthday!",
                render_template("email_birthday.html", user=user),
            )
        )

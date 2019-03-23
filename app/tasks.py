from flask_mail import Message

from app import app, celery, mail


@celery.task(name="send_email")
def send_email(subject, recipients, body, html):
    msg = Message(subject, sender=("STD-messenger", app.config["ADMINS"][0]), recipients=recipients)
    msg.body = body
    msg.html = html
    with app.app_context():
        mail.send(msg)

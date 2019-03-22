from flask_mail import Message

from app import app, celery, mail


@celery.task()
def add_together(a, b):
    return a + b


# в task не передавать модели ORM


@celery.task(name="send_email")
def send_email(subject, recipients, text, html):
    msg = Message(subject, sender=app.config["ADMINS"][0], recipients=recipients)
    msg.body = text
    msg.html = html
    with app.app_context():
        mail.send(msg)

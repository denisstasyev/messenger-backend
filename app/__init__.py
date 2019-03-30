# pylint: disable=wrong-import-position

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from celery.schedules import crontab
from werkzeug.contrib.cache import MemcachedCache

# Profiler
from werkzeug.contrib.profiler import ProfilerMiddleware

from .flask_celery import make_celery

app = Flask(__name__, instance_relative_config=True)

app.config.from_object("config")
app.config.from_pyfile("development.cfg", silent=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

mail = Mail(app)

lm = LoginManager(app)

# Turn off Black formatter
# fmt: off
app.config.update(
    # Celery
    result_backend="redis://localhost:6379",
    broker_url="redis://localhost:6379",
)
celery = make_celery(app)
from .tasks import send_email_birthday
celery.conf.beat_schedule = {
    "birthday-task": {
        "task": "send_email_birthday",
        "schedule": crontab(hour=7, minute=0),
    }
}
# fmt: on

cache = MemcachedCache(["127.0.0.1:11211"])

# Profiler
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])

from .views import *
from .models import *

# pylint: disable=wrong-import-position

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager

from .flask_celery import make_celery

app = Flask(__name__, instance_relative_config=True)

app.config.from_object("config")
app.config.from_pyfile("development.cfg", silent=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

celery = make_celery(app)

mail = Mail(app)

lm = LoginManager(app)

from .views import *
from .models import *

from .tasks import *

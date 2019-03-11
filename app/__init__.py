# pylint: disable=wrong-import-position

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, instance_relative_config=True)

app.config.from_object("config")
app.config.from_pyfile("development.cfg", silent=True)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from .views import *
from .models import *

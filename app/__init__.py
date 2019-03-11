from flask import Flask
from config import *  # ProductionConfig, DevelopmentConfig, TestingConfig

from flask_jsonrpc import JSONRPC

app = Flask(__name__, instance_relative_config=True)
jsonrpc = JSONRPC(app, '/api/')

app.config.from_object(ProductionConfig)
# app.config.from_object('config.ProductionConfig')

# app.config.from_pyfile('config.py')

from .views import *
from .handlers import *

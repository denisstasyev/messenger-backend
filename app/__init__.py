from flask import Flask
# from config import ProductionConfig, DevelopmentConfig, TestingConfig

app = Flask(__name__, instance_relative_config=True)

# app.config.from_object(ProductionConfig)
app.config.from_object('config.ProductionConfig')

# app.config.from_pyfile('config.py')

from .views import *

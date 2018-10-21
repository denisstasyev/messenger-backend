from flask import Flask

app = Flask(__name__)

from config import ProductionConfig, DevelopmentConfig, TestingConfig  # импортируем файл конфигурации

app.config.from_object(ProductionConfig)

from .views import *

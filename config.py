TESTING = False
DEBUG = False

# Disable SQLAlchemy event system
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Celery
CELERY_RESULT_BACKEND = "redis://localhost:6379"
BROKER_URL = "redis://localhost:6379"

# Email server config
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = "stdmessenger"

# Email administrator list
ADMINS = ["stdmessenger@gmail.com"]

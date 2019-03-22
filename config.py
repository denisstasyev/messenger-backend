TESTING = False
DEBUG = False

# Disable SQLAlchemy event system
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Celery
CELERY_RESULT_BACKEND = "redis://localhost:6379"
BROKER_URL = "redis://localhost:6379"

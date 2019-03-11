DB_NAME = 'messanger'
DB_HOST = 'localhost'
DB_USER = 'messanger'
DB_PASS = 'messanger'  # password


class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    # DATABASE_URI = 'mysql://user@localhost/foo'
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

import os
basedir = os.path.dirname(__file__)

class Config(object):
    ENV = 'development'
    DEBUG = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:root@localhost:5432/sma"
    UPLOAD_FOLDER = os.path.join(basedir, 'upload')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class ProductionConfig(Config):
    ENV = 'Production'
    DEBUG = True

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True

from environs import Env
from distutils.util import strtobool
import logging

env = Env()
env.read_env()


class Config:
    FLASK_APP = env.str("FLASK_APP", default="server.py")
    FLASK_LOG_TYPE = env.str("FLASK_LOG_TYPE", default="console")
    SECRET_KEY = env.str("SECRET_KEY")

    # flask-sqlalchemy config
    SQLALCHEMY_DATABASE_URI = env.str("SQLALCHEMY_DATABASE_URI", default=None)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    AUTHORIZATION_KEY = env.str("AUTHORIZATION_KEY")
    FETCH_URL = env.str("FETCH_URL")

class ProductionConfig(Config):
    ENV = 'production'
    DEVELOPMENT = False
    DEBUG = False
    LOG_LEVEL = logging.DEBUG

class StagingConfig(Config):
    ENV = 'staging'
    DEVELOPMENT = True
    DEBUG = True
    LOG_LEVEL = logging.INFO

class DevConfig(Config):
    ENV = 'development'
    DEVELOPMENT = True
    DEBUG = True
    LOG_LEVEL = logging.DEBUG
    
# ---------------------------------- APP SETTING
app_settings = dict(
    production=ProductionConfig,
    staging=StagingConfig,
    development=DevConfig,
)

APP_SETTING = app_settings.get(env.str("FLASK_ENV", default="production"))

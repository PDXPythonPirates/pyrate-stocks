import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TRAP_HTTP_EXCEPTIONS=True

    MAIL_SERVER='localhost'
    MAIL_PORT=8025
    MAIL_SENDER = 'pomayi5461@nobitcoin.net'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
# 
    # the base Config class implements an empty init_app() method.
    @staticmethod
    def init_app(app):
        pass

# Different development environments - Development, Testing and Production.
# The different SQLALCHEMY_DATABASE_URI configurations allows the application to use
# a different database in each configuration so they don't interfere with eachother.
class DevelopmentConfig(Config):
    # Creates the development db located in the root
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'fin_app.sqlite3')

class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' 

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite3')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
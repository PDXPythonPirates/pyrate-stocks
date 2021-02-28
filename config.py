import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TRAP_HTTP_EXCEPTIONS=True

    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 465
    # MAIL_USE_TLS = False
    # MAIL_USE_SSL = True
    
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 465
    # MAIL_USE_TLS = False
    # MAIL_USE_SSL = True
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    MAIL_SERVER='smtp.mailtrap.io'
    MAIL_PORT = 465
    MAIL_USERNAME = 'c13b6e757c1db6'
    MAIL_PASSWORD = '614aa52c9cceb3'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    
    # MAIL_USERNAME = 'ppp.cohort1@gmail.com'
    
    #MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    #MAIL_PORT =  int(os.environ.get('MAIL_PORT',  '465'))
    #MAIL_USE_TLS =  int(os.environ.get('MAIL_USE_TLS',  False))
    #MAIL_USE_SSL = int(os.environ.get('MAIL_USE_SSL',  True))
    
        
    # the base Config class implements an empty init_app() method.
    @staticmethod
    def init_app(app):
        pass

# Different development environments - Development, Testing and Production.
# The different SQLALCHEMY_DATABASE_URI configurations allows the application to use
# a different database in each configuration so they don't interfere with eachother.
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite3')

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
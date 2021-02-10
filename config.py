import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Contains settings that are common to all configurations.
# There is functionality included that we won't need *yet*, but this
# allows for future customization of the app as needed - and provides
# a roadmap to make that happen
class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').Lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FIN_APP_MAIL_SUBJECT_PREFIX = '[Financial_Application]'
    FIN_APP_MAIL_SENDER = 'Financial Application <Fin-App@example.com>'
    FIN_APP_ADMIN = os.environ.get('FIN_APP_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Takes the application instance as instance - for now, 
    # the base Config class implements an empty init_app() method.
    @staticmethod
    def init_app(app):
        pass

# Different development environments - Development, Testing and Production.
# The different SQLALCHEMY_DATABASE_URI configurations allows the application to use
# a different database in each configuration so they don't interfere with eachother.
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' 

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
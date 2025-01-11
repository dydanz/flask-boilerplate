import logging
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    You can put global variable config for all-enviroment
    """
    # Logging Severity Level
    LOGGING_LEVEL = logging.INFO

    SECRET_KEY = os.environ.get('GLOBAL_SECRET_KEY') or 'GlobalSecretKey123'

    # Initial refresh token set for 1 week * 4.
    USER_TOKEN_EXPIRED = 604800 * 4

    DEBUG = False


class DevelopmentConfig(Config):
    """
    Only applied when using Development Configuration
    """
    DEBUG = True

    # You can load from environment variables, if failed load `default` setting.
    SECRET_KEY = os.environ.get('DevServer_SECRET_KEY') or 'DevServerSecretKey123'

    # Database SQLAlchemy Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
        'postgresql://postgres:postgres@localhost:5432/flask_marketplace')

    # Enable Write/Reading on Master/Slave DB servers
    SQLALCHEMY_BINDS = {
        'master': 'postgresql://postgres:postgres@localhost:5432/flask_marketplace',
        'read': 'postgresql://postgres:postgres@localhost:5432/flask_marketplace'
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 15


class TestingConfig(Config):
    """
    Only applied when running Test
    """
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'TestSecretKey123'
    
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
        'postgresql://postgres:postgres@localhost:5432/flask_marketplace_test')
    
    SQLALCHEMY_BINDS = {
        'master': 'postgresql://postgres:postgres@localhost:5432/flask_marketplace_test',
        'read': 'postgresql://postgres:postgres@localhost:5432/flask_marketplace_test'
    }

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('ProductionServer_SECRET_KEY') or 'ProductionServer_SECRET_KEY'

    # Database SQLAlchemy Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
        'postgresql://postgres:postgres@localhost:5432/flask_marketplace')

    # Enable Write/Reading on Master/Slave DB servers
    SQLALCHEMY_BINDS = {
        'master': 'postgresql://postgres:postgres@localhost:5432/flask_marketplace',
        'read': 'postgresql://postgres:postgres@localhost:5432/flask_marketplace'
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 15


config_by_name = {
    'development': DevelopmentConfig,
    'test': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

key = Config.SECRET_KEY

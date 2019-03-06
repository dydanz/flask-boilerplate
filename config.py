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


class LocalConfig(Config):
    """
    Only applied when using Local(host) Server Configuration
    """
    DEBUG = True

    # You can load from environment variables, if failed load `default` setting.
    ENV_SECRET_KEY = os.environ.get('LOCAL_SECRET_KEY') or 'LocalSecretKey123'

    # Database SQLAlchemy Configuration
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:password@localhost:5432/marketplace'
    SQLALCHEMY_BINDS = {
        'master': 'postgresql://admin:password@localhost:5432/marketplace',
        'read': 'postgresql://admin:password@localhost:5432/marketplace'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ANALYTICS_DATABASE_NAME = 'analytic'
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 15


class TestingConfig(Config):
    """
    Only applied when running Test
    """
    TESTING = True
    SECRET_KEY = 'TestSecretKey123'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
            'TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(
            basedir, 'data-test.sqlite'
    )
    SQLALCHEMY_BINDS = {
        'master': os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(
                basedir, 'data-test.sqlite'),
        'read': os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(
                basedir, 'data-test.sqlite')
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(Config):
    DEBUG = True

    # You can load from environment variables, if failed load `default` setting.
    SECRET_KEY = os.environ.get('DevServer_SECRET_KEY') or 'DevServerSecretKey123'
    # Database SQLAlchemy Configuration
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:password@localhost:5432/marketplace'
    # Enable Write/Reading on Master/Slave DB servers
    SQLALCHEMY_BINDS = {
        'master': 'postgresql://admin:password@localhost:5432/marketplace',
        'read': 'postgresql://admin:password@localhost-readonly:5432/marketplace'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 15


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('ProductionServer_SECRET_KEY') or 'ProductionServer_SECRET_KEY'
    # Database SQLAlchemy Configuration
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:password@localhost:5432/marketplace'
    # Enable Write/Reading on Master/Slave DB servers
    SQLALCHEMY_BINDS = {
        'master': 'postgresql://admin:password@localhost:5432/marketplace',
        'read': 'postgresql://admin:password@localhost-readonly:5432/marketplace'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 15


# Load You Multi-Environment Configuration
config = {
    'local': LocalConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

default_env = 'default'
active_config = config[default_env]

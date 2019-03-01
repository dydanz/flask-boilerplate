import logging.config
from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from os import path

from config import config

# This Global Singleton Handlers will be registered later into Flask Application Context
db = SQLAlchemy()
cors = CORS()
cache = Cache()
migrate = Migrate()

# Init and load Logging Configuration
PROJECT_ROOT = path.dirname(path.abspath(__file__))
BASE_DIR = path.dirname(PROJECT_ROOT)
log_file_path = path.join(BASE_DIR, 'logging.conf')
logging.config.fileConfig(log_file_path)


def register_blueprints(app):
    """
    Register FLask-Blueprint
    """
    from marketplace.v1 import api, api_v1_blueprint
    app.register_blueprint(api_v1_blueprint)

    from marketplace.merchant.v1.routes import ns as merchant_namespace
    api.add_namespace(merchant_namespace)


def create_app(config_name):
    """
    Initialize Logging, DB Connection, etc. within Current Application Context
    :param config_name: Server Environment, e.g. Development/Staging/Production
    :return: Flask Application
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app_logger = logging.getLogger(__name__)

    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        register_blueprints(app)
        cors.init_app(app, resources={r"/api/*": {"origins": "*"}}, send_wildcard=True)
        app_logger.setLevel(app.config['LOGGING_LEVEL'])

    return app

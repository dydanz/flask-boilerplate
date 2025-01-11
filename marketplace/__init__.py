from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restx import Api

from config import config_by_name

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    
    # Configure Swagger UI
    app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
    app.config.SWAGGER_UI_OPERATION_ID = True
    app.config.SWAGGER_UI_REQUEST_DURATION = True
    
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from marketplace.user.v1 import user_bp
    app.register_blueprint(user_bp, url_prefix='/api/v1/user')

    from marketplace.health import health_bp
    app.register_blueprint(health_bp, url_prefix='/api')

    return app

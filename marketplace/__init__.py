from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restx import Api

from config import config_by_name

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

# Create main API instance
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    }
}

api = Api(
    title='Flask Marketplace API',
    version='1.0',
    description='A simple marketplace API',
    doc='/swagger',
    authorizations=authorizations
)

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
    api.init_app(app)

    # Register blueprints and namespaces
    from marketplace.user.v1.routes import auth_ns, users_ns
    from marketplace.merchant.v1.routes import merchant_ns
    from marketplace.health.routes import health_ns

    api.add_namespace(auth_ns, path='/api/v1/user/auth')
    api.add_namespace(users_ns, path='/api/v1/user/users')
    api.add_namespace(merchant_ns, path='/api/v1/merchant')
    api.add_namespace(health_ns, path='/api/health')

    return app

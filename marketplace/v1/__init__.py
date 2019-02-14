import logging
import time

from flask import Blueprint, g, request
from flask_restplus import Api


log = logging.getLogger(__name__)
authorizations = {
    'tokenkey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-Oy-Authorization'
    },
    'userkey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-Oy-Username'
    }
}

api = Api(version='1.0', title='Marketplace Restful API',
          description='Collection of Marketplace Restful API version 1.x',
          authorizations=authorizations,
          security='tokenkey',
          doc='/swagger'
          )
api_v1_blueprint = Blueprint('api.v3', __name__, url_prefix='/api/v3')
api.init_app(api_v1_blueprint)


@api_v1_blueprint.before_request
def before_api_request():
    """
    You can do pre-process before actual request being executed, e.g. Authorization, Logging Stats, etc.

    :return:
    """
    pass


@api_v1_blueprint.after_request
def after_api_request(response):
    pass
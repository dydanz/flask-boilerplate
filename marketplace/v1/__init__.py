import logging
import time

from flask import Blueprint, g, request, session
from flask_restplus import Api

from common.authenticator.session_management import authorize_user_token
from common.http import custom_errors as errors
from marketplace.persistence.model import User

log = logging.getLogger(__name__)
authorizations = {
    'tokenkey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'auth-token-key'
    },
    'userkey': {

        'type': 'apiKey',
        'in': 'header',
        'name': 'username-key'
    }
}

api = Api(version='1.0', title='Marketplace Restful API',
          description='Collection of Marketplace Restful API version 1.x',
          authorizations=authorizations,
          security='tokenkey',
          doc='/swagger'
          )
api_v1_blueprint = Blueprint('api.v1', __name__, url_prefix='/api/v1')
api.init_app(api_v1_blueprint)

# Enable By-Pass Auth for Swagger Endpoints
NO_AUTH_ENDPOINTS = ['api.v1.doc', 'api.v1.specs', 'api.v1.user_user_auth_login_api']


def statsd_put_start_endpoint(request):
    endpoint = request.endpoint
    session['endpoint'] = endpoint
    session['start'] = time.time()


def statsd_put_end_endpoint():
    endpoint = session['endpoint']
    start = session['start']
    return endpoint, start


@api_v1_blueprint.before_request
def before_api_request():
    """
    You can do PRE-process before actual request being executed, e.g. Authorization,
    Logging Stats, etc.

    :return: None
    """
    # Start Point of a request, will count how long (miliseconds) for a request to be processed
    statsd_put_start_endpoint(request)

    # By-Pass Swagger Endpoints and Login
    if request.endpoint in NO_AUTH_ENDPOINTS:
        return

    # Get Request Header
    username_requester = request.headers.get('username-key')

    # Will Return HTTP-401 status if Username is not found
    user_account = User.query.filter(User.username == username_requester).first()
    if user_account is None:
        return errors.unauthorized('Unauthorized API access')

    # Check whether given User auth token key is valid
    user_session = authorize_user_token(request.headers.get('auth-token-key'), user_account)
    if user_session is None:
        return errors.unauthorized('Unauthorized API access')

    # Store into global variable
    g.current_session = user_session
    g.current_user = user_account

    # Logging any request information, if necessary
    str_fmt = '[username:{username}][{method}][{url}]'
    val_fmt = str_fmt.format(url=request.url, method=request.method, username=username_requester)
    log.info(val_fmt)


@api_v1_blueprint.after_request
def after_api_request(response):
    """
    And here you can do POST-process after actual request being executed, e.g.
    Logging Req Response Message, add request-latency etc.

    :return: None
    """
    # Calculate total time after processing a request
    endpoint, start = statsd_put_end_endpoint()
    log.info("[Complete Request {} Time {}s]".format(endpoint, int(time.time() - start)))
    return response

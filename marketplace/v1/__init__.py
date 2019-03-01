import time

import logging
from flask import Blueprint, request, session
from flask_restplus import Api

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

    # Get Request Header
    username_requester = request.headers.get('username-key')

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

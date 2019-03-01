from flask_restplus import abort as _flask_restplus_abort


def bad_request(message):
    _flask_restplus_abort(400, message=message)


def unauthorized(message):
    _flask_restplus_abort(401, message=message)


def forbidden(message):
    _flask_restplus_abort(403, message=message)


def not_found(message):
    _flask_restplus_abort(404, message=message)


def internal_server_error():
    response = 'Internal server error.'
    _flask_restplus_abort(500, message=response)


def internal_server_error_msg(message):
    response = 'Internal server error. reason: ' + message
    _flask_restplus_abort(500, message=response)


def abort(code, **kwargs):
    _flask_restplus_abort(code, **kwargs)

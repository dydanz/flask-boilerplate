from flask import Blueprint

user_bp = Blueprint('user_v1', __name__)

from marketplace.user.v1 import routes  # noqa

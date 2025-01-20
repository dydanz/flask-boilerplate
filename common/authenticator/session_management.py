import base64
import hashlib
import logging
import uuid

from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import exc

from marketplace.persistence.model import User, UserSession

log = logging.getLogger(__name__)


def generate_random_session_id():
    return str(uuid.uuid4().hex[:8])


def generate_user_password(phone):
    # Create password from phone and randomization
    return base64.b64encode(hashlib.sha256((phone + str(uuid.uuid4().hex[:32])).encode(
        encoding='utf-8')).hexdigest().encode()).decode('utf-8')


def generate_user_secret_key(username: str, phone_number: str):
    base_secret_key = username + phone_number + (current_app.config['SECRET_KEY'])
    random_secret_key = uuid.uuid1().hex
    user_secret_key = hashlib.sha1((base_secret_key + random_secret_key).encode(
        encoding='utf-8')).hexdigest()

    return user_secret_key


def create_access_token(username, session_id, token_secret_key):
    s = Serializer(token_secret_key,
                   expires_in=current_app.config['USER_TOKEN_EXPIRED'])
    token = s.dumps({'session_id': session_id, 'username': username}).decode('utf-8')
    return token


def parse_session_id(token_secret_key, token):
    s = Serializer(token_secret_key)
    try:
        data = s.loads(token)
    except Exception as e:
        log.error(e)
        return None
    return data['session_id']


def authorize_user_token(request_token: str, user: User):
    session = UserSession.query.filter(UserSession.username == user.username).first()

    session_id = parse_session_id(session.secret_key, request_token)

    if session_id != session.id:
        return None

    return session


def create_user_session(user: User):
    # Avoid create multiple User Session if want to manage One User = One Unique Session
    session = UserSession.query.filter(UserSession.username == User.username).first()

    # (Re)Init User Session in Database
    session = session or UserSession()
    session.username = user.username
    session.secret_key = generate_user_secret_key(user.username, user.phone)
    session.id = generate_random_session_id()

    try:
        session.save()
    except exc.SQLAlchemyError:
        return None

    # Create Authorization Token based on Their Session ID, token shouldn't be stored plainly on DB
    token = create_access_token(user.username, session.id, session.secret_key)

    return token


def delete_user_session(username: str):
    # find existing user session
    session = UserSession.query.filter(UserSession.username == username).first()

    try:
        session.delete()
    except exc.SQLAlchemyError:
        pass

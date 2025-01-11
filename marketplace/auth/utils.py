from functools import wraps
from flask import request, current_app
import jwt
from datetime import datetime, timedelta
from marketplace.persistence.model import User

def generate_token(user_id):
    """Generate JWT token for user"""
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return str(e)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return {'message': 'Token is missing'}, 401

        if not token:
            return {'message': 'Token is missing'}, 401

        try:
            payload = jwt.decode(
                token, 
                current_app.config.get('SECRET_KEY'),
                algorithms=["HS256"]
            )
            current_user = User.query.filter_by(id=payload['sub']).first()
        except jwt.ExpiredSignatureError:
            return {'message': 'Token has expired'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Invalid token'}, 401

        return f(current_user, *args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    @token_required
    def decorated(current_user, *args, **kwargs):
        if not current_user.is_admin:
            return {'message': 'Admin privilege required'}, 403
        return f(current_user, *args, **kwargs)
    return decorated 
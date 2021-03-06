from functools import wraps
from flask import request, _request_ctx_stack, current_app
from jose import jwt
from datetime import datetime, timedelta
from db.models import Role, User


class AuthError(Exception):
    ''' Base class for all auth excpetions '''

    def __init__(self, message: str, code: int):
        ''' Base class for all auth excpetions '''
        self.message = message
        self.code = code


def get_token_auth_header() -> str:
    ''' get token from current request Authorization header '''

    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError(
            "Authorization header is expected", 401)
    parts = auth.split()
    if parts[0].lower() != "bearer":
        raise AuthError(
            "Authorization header must start with Bearer", 401)
    elif len(parts) == 1:
        raise AuthError(
            "Token not found", 401)
    elif len(parts) > 2:
        raise AuthError(
            "Authorization header must be Bearer token", 401)
    token = parts[1]
    return token


def requires_auth(f):
    ''' Decorator to validate jwt on requests and to add the validated payload to _request_ctx_stack '''
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        secret_key = current_app.config['SECRET_KEY']
        try:
            payload = jwt.decode(token, secret_key, 'HS256')
        except (jwt.JWTClaimsError, jwt.ExpiredSignatureError, jwt.JWSError):
            raise AuthError('Token is invalid', 401)

        _request_ctx_stack.top.curr_user = payload
        return f(*args, **kwargs)
    return decorated


def requires_permission(required_permission: str) -> bool:
    ''' check if specific permission exists in the current user '''
    permissions = _request_ctx_stack.top.curr_user['permissions']
    return required_permission in permissions


def gen_token(secret_key: str, user: User) -> str:
    ''' Generate JWT token '''
    permissions = Role.query.get(user.role_id).permissions
    payload = {
        'sub': user.username,
        'exp': datetime.now() + timedelta(days=30),
        'permissions': [permission.name for permission in permissions]
    }
    token = jwt.encode(payload, secret_key, 'HS256')
    return str(token)

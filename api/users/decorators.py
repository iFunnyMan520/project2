from flask import request, jsonify

from api.users.utils import check_token


def with_secret_key(func):
    def wrapper(*args, **kwargs):
        secret_key = '4da5933b-120a-4108-8670-faa83ca6a43a'
        key: str = request.headers.get('secret_key', None)

        if not key or key != secret_key:
            return jsonify({'message': 'Invalid secret key'}), 400

        resp = func(*args, **kwargs)

        return resp
    return wrapper


def only_authorized(func):
    @with_secret_key
    def wrapper(*args, **kwargs):
        token: str = request.headers.get('token', None)

        if not token:
            return jsonify({'message': 'Invalid headers data'}), 400

        user = check_token(token=token)

        if not user:
            return jsonify({'message': 'User is not logged in'}), 401

        resp = func(*args, user=user, **kwargs)

        return resp
    return wrapper

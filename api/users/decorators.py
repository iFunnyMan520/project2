from flask import request, jsonify

from api.users.utils import check_token


def only_authorized(func):
    def wrapper(*args, **kwargs):
        token: str = request.headers.get('token', None)

        if not token:
            return jsonify({'message': 'Invalid headers data'}), 400

        me = check_token(token=token)

        if not me:
            return jsonify({'message': 'User is not logged in'}), 401

        resp = func(*args, me=me, **kwargs)

        return jsonify(resp)
    return wrapper

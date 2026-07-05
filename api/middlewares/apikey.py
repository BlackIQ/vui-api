from flask import request, jsonify

from api.config.db import KEY

from functools import wraps


def apiKey(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('apiKey')

        if api_key and api_key == KEY:
            return func(*args, **kwargs)
        else:
            return jsonify({'message': 'Unauthorized'}), 401

    return decorated_function

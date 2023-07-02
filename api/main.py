from flask import Flask, request, jsonify
from flask_cors import CORS

import os

from api.config.config import path
from api.functions.execute import execute

app = Flask(__name__)
CORS(app)


@app.route('/api/users', methods=['GET'])
def all_users():
    response = {'message': 'read'}

    script_path = os.path.join(path, 'scripts\\test.sh')
    execution = execute(script_path, "amir")

    print(script_path)

    status_code = 0

    if execution:
        status_code = 200
        response['status'] = 'success'
    else:
        status_code = 500
        response['status'] = 'error'

    return jsonify(response), status_code


@app.route('/api/users', methods=['POST'])
def create_user():
    response = {'message': 'create'}

    username = request.json['username']
    password = request.json['password']

    print(username, password)

    return jsonify(response)


@app.route('/api/users/<username>', methods=['PATCH'])
def update_user(username):
    response = {'message': 'update'}

    print(username)

    return jsonify(response)


@app.route('/api/users/<username>', methods=['DELETE'])
def delete_user(username):
    response = {'message': 'delete'}

    print(username)

    return jsonify(response)

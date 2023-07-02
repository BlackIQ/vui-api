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

    script_path = os.path.join(path, 'scripts/test.sh')

    success = execute(script_path, "amir")

    print(success)

    if success:
        response['status'] = 'success'
    else:
        response['status'] = 'error'

    return jsonify(response)


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

from flask import Flask, request, jsonify

from typing import any, list, optional


import pydantic from 


app = Flask(__name__)

users = {
    'admin': 'password123'
}

tokens = {}

@app.route('/api/login', methods = ['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'Error' : 'Please provide username and password'}), 400
    
    if username not in users or users[username] != password:
        return jsonify({'Error': 'Invalid credentials'}), 401

    token = 123456
    tokens[username] = token
    return jsonify({'Message': 'Authentication successful', 'token': token})

@app.route('/api/protected', methods = ['GET'])
def protected():
    token = request.headers.get('Authorization')

    if token and token in tokens.values():
        return jsonify({'Message': 'You are authorized to access this resource'})
    else:
        return jsonify({'Error': 'You are not authorized to access this resource'}), 403


if __name__ == '__main__':
    app.run(debug = True)

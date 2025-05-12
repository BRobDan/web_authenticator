# so far contains blueprint for login request

from flask import Blueprint, request, jsonify
from .tokens import generate_jwt_token
from db import get_user_info, register_user
from .hashing import hash_password, verify_password

"""
The below code contains the blueprint route for authentication
I will add more blueprint routes as necessary below the authentication route later
"""

# Define the Blueprint for authentication routes
auth_blueprint = Blueprint('auth', __name__)

# Route for login: it accepts POST requests and returns a JWT token
@auth_blueprint.route('/login', methods=['POST'])
def login():
    # Get the credentials from the POST request
    data = request.get_json()

    # check for missing fields
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Username and password are required'}), 400

    # save username and password
    username = data.get('username')
    password = data.get('password')

    # retrieve database information for user
    user_info = get_user_info(username)

    # check to see if no user was found
    if not user_info:
        return jsonify({'message': 'Invalid credentials'}), 401

    # unpack user info
    stored_username, stored_hash = user_info

    # debug statement
    print('stored:', stored_hash)

    # test validation, need to replace later
    if verify_password(stored_hash, password):
        token = generate_jwt_token(username)
        return jsonify({'token': token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401
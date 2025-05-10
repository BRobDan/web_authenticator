# so far contains blueprint for login request

from flask import Blueprint, request, jsonify
from .tokens import generate_jwt_token

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

    # test validation, need to replace later
    if username == "admin" and password == "password":
        token = generate_jwt_token(username)
        return jsonify({'token': token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401
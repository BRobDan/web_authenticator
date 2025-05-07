# so far contains blueprint for login request

from flask import Blueprint, request, jsonify
import jwt
import datetime

# Define the Blueprint for authentication routes
auth_blueprint = Blueprint('auth', __name__)

# Secret key for encoding and decoding JWT tokens
SECRET_KEY = 'your_secret_key_here' # use an environment variable later once app is working


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

def generate_jwt_token(username):
    # Current time in UTC
    current_time_utc = datetime.datetime.now(datetime.timezone.utc)

    # Payload with expiration
    payload = {
        'sub': username,  # Subject (who the token is for)
        'iat': current_time_utc,  # Issued at time
        'exp': current_time_utc + datetime.timedelta(hours=1)  # Expiration time (1 hour from now)
    }

    # Generate JWT token
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return token
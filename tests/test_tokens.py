# tests for tokens

import jwt
from auth import generate_jwt_token

# Tests the generation of jwt tokens
def test_generate_jwt_token():
    # create username of admin
    username = 'admin'

    # Secret key for encoding and decoding JWT tokens
    SECRET_KEY = 'your_secret_key_here'  # use an environment variable later once app is working

    # generate a token
    token = generate_jwt_token(username)

    # get the payload from the jwt token
    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

    assert payload['sub'] == username



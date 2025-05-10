# generates tokens

import datetime
import jwt

# Secret key for encoding and decoding JWT tokens
SECRET_KEY = 'your_secret_key_here' # use an environment variable later once app is working


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
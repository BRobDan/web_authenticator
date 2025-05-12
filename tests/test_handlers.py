# tests for handlers

import pytest
from flask import Flask
from auth import auth_blueprint
from unittest.mock import patch
from argon2 import PasswordHasher


# Set up a Flask test app for testing
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.config['TESTING'] = True
    return app


# Set up a test client for sending requests
@pytest.fixture
def client(app):
    return app.test_client()


# Tests a proper login request with valid credentials
@patch('auth.handlers.get_user_info')  # Mocking database call
def test_login_success(mock_get_user_info, client):
    # Generate the hash for 'password'
    ph = PasswordHasher(time_cost=2, memory_cost=102400, parallelism=8)
    generated_hash = ph.hash('password')

    # debug statement
    print('generated:', generated_hash)

    # Mock a valid user return
    mock_get_user_info.return_value = ('admin', generated_hash)

    response = client.post('/auth/login', json={
        'username': 'admin',
        'password': 'password'
    })

    data = response.get_json()
    assert response.status_code == 200
    assert 'token' in data  # Check if token is returned


# Tests missing fields in a request
def test_login_missing_fields(client):
    response = client.post('/auth/login', json={
        'username': 'admin'
        # Missing password
    })
    assert response.status_code == 400
    assert response.get_json()['message'] == 'Username and password are required'


# Tests incorrect credentials
@patch('auth.handlers.get_user_info')  # Mocking database call
def test_login_invalid_credentials(mock_get_user_info, client):
    # Mock a user with incorrect credentials
    mock_get_user_info.return_value = ('admin', '$argon2id$v=19$m=65536,t=3,p=4$asL46y0THsnRyYC8Jy8BOg$Afk0DGZZL8TR9y1xgQ/h+YKitxUVyh+esmlt1VzNMNE')

    response = client.post('/auth/login', json={
        'username': 'admin',
        'password': 'wrongpassword'  # This should fail verification
    })

    assert response.status_code == 401
    assert response.get_json()['message'] == 'Invalid credentials'


# Tests correct handling when no user is found
@patch('auth.handlers.get_user_info')  # Mocking database call
def test_login_no_user(mock_get_user_info, client):
    # Simulate no user found in the database
    mock_get_user_info.return_value = None

    response = client.post('/auth/login', json={
        'username': 'nonexistent_user',
        'password': 'somepassword'
    })

    assert response.status_code == 401
    assert response.get_json()['message'] == 'Invalid credentials'

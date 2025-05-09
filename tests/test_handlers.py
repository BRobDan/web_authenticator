# tests for handlers

import pytest
from flask import Flask
from auth import auth_blueprint

# Set up a Flask test app for testing
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()


def test_login_success(client):
    response = client.post('/auth/login', json={
        'username': 'admin',
        'password': 'password'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert 'token' in data


def test_login_missing_fields(client):
    response = client.post('/auth/login', json={
        'username': 'admin'
        # Missing password
    })
    assert response.status_code == 400
    assert response.get_json()['message'] == 'Username and password are required'


def test_login_invalid_credentials(client):
    response = client.post('/auth/login', json={
        'username': 'wrong',
        'password': 'wrongpass'
    })
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Invalid credentials'

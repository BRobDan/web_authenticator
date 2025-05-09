# tests for app creation

import pytest
from app import create_app  # Import your create_app function
from flask import Flask

@pytest.fixture
def app():
    # Use the create_app function to set up the app
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    # Create a test client for making requests to the app
    return app.test_client()

def test_app_creation(app):
    # Test that the app is created successfully and the blueprint is registered
    assert isinstance(app, Flask)  # Check if the app is a Flask app instance

    # Collect all route rule strings
    routes = [rule.rule for rule in app.url_map.iter_rules()]

    # Check that the expected route is among them
    assert '/auth/login' in routes

    # Check that the endpoint name exists
    assert 'auth.login' in app.view_functions
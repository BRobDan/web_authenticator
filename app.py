# app file

from flask import Flask # import flask
from auth import auth_blueprint # import blueprint for authentication


def create_app():
    app = Flask(__name__)

    # blueprint for login/POST
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app

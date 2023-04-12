from datetime import timedelta
from flask import Flask, redirect, url_for
from flask_jwt_extended import JWTManager
from avaliacao.ext import configuration

# def jwt_error_handler(jwt_header_error):
#     return redirect(url_for("webui.login"))

def minimal_app(**config):
    app = Flask(__name__)
    configuration.init_app(app, **config)
    # Substitua `app` pelo seu objeto Flask
    app.config['SECRET_KEY'] = 'chaves'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
    jwt = JWTManager(app)
    return app


def create_app(**config):
    app = minimal_app(**config)
    configuration.load_extensions(app)
    return app

"""
Este é o módulo app.py.
Ele contém a configuração do aplicativo Flask.
"""
from datetime import timedelta

from flask import Flask
from flask_jwt_extended import JWTManager

from avaliacao.ext import configuration


def minimal_app(**config):
    """
    Esta função cria e configura um aplicativo Flask mínimo.
    """
    app = Flask(__name__)
    configuration.init_app(app, **config)
    # Substitua `app` pelo seu objeto Flask
    app.config['SECRET_KEY'] = 'chaves'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
    
    # Importe e inicialize a extensão `api` aqui
    from avaliacao.blueprints.restapi import api
    api.init_app(app)
    
    return app


def create_app(**config):
    """
    Esta função cria e configura um aplicativo Flask completo.
    """
    app = minimal_app(**config)
    configuration.load_extensions(app)
    return app


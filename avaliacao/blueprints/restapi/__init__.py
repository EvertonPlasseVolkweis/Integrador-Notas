from flask import Blueprint
from flask_restful import Api
from .resources import UsuariosResource, CadastroAvaliacaoResource


## inicialização para rotas de controladora chamando classes resources

bp = Blueprint("restapi", __name__, url_prefix="/api/v1")
api = Api(bp)


def init_app(app):
    ## modelo de busca: localhost/api/v1/usuarios/
    api.add_resource(UsuariosResource, "/usuarios/")
    api.add_resource(CadastroAvaliacaoResource, "/avaliacao/cadastro")
    app.register_blueprint(bp)

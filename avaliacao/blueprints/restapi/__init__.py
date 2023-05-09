from flask import Blueprint
from flask_restful import Api
from .resources import BuscarUsuario, CadastroUsuario, DeleteAvaliacao, EditAvaliacao, LogoutResource, NotaAvaliaResource, UsuariosResource, CadastroAvaliacaoResource


## inicialização para rotas de controladora chamando classes resources

bp = Blueprint("restapi", __name__, url_prefix="/api/v1")
api = Api(bp)


def init_app(app):
    ## modelo de busca: localhost/api/v1/usuarios/
    api.add_resource(UsuariosResource, "/usuarios/")
    api.add_resource(CadastroAvaliacaoResource, "/avaliacao/cadastro")
    api.add_resource(NotaAvaliaResource, "/nota-avalia/cadastro")
    api.add_resource(BuscarUsuario, "/busca-usuario")
    api.add_resource(CadastroUsuario, "/cadastro-usuario")
    api.add_resource(LogoutResource, "/logout")
    api.add_resource(EditAvaliacao, "/nota-avalia/editar/<int:avaliacaoId>")
    api.add_resource(DeleteAvaliacao, "/nota-avalia/deletar/<int:avaliacaoId>")
    app.register_blueprint(bp)

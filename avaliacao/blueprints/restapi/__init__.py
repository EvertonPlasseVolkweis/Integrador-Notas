from flask import Blueprint
from flask_restful import Api
<<<<<<< HEAD
from .resources import NotaAvaliaResource, UsuariosResource, CadastroAvaliacaoResource
=======
from .resources import BuscarUsuario, CadastroUsuario, LogoutResource, NotaAvaliaResource, UsuariosResource, CadastroAvaliacaoResource
>>>>>>> 8e97432adb7cd84f7a1a8062ac6126d72675adf9


## inicialização para rotas de controladora chamando classes resources

bp = Blueprint("restapi", __name__, url_prefix="/api/v1")
api = Api(bp)


def init_app(app):
    ## modelo de busca: localhost/api/v1/usuarios/
    api.add_resource(UsuariosResource, "/usuarios/")
    api.add_resource(CadastroAvaliacaoResource, "/avaliacao/cadastro")
    api.add_resource(NotaAvaliaResource, "/nota-avalia/cadastro")
<<<<<<< HEAD
=======
    api.add_resource(BuscarUsuario, "/busca-usuario")
    api.add_resource(CadastroUsuario, "/cadastro-usuario")
    api.add_resource(LogoutResource, "/logout")
>>>>>>> 8e97432adb7cd84f7a1a8062ac6126d72675adf9
    app.register_blueprint(bp)

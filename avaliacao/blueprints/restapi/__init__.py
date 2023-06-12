from flask import Blueprint
from flask_restful import Api

from .resources import *

## inicialização para rotas de controladora chamando classes resources

bp = Blueprint("restapi", __name__, url_prefix="/api/v1")
api = Api(bp)


def init_app(app):
    ## modelo de busca: localhost/api/v1/usuarios/
    api.add_resource(UsuariosResource, "/usuarios/")
    api.add_resource(CadastroAvaliacaoResource, "/avaliacao/cadastro/<int:idUsuario>")
    api.add_resource(NotaAvaliaResource, "/nota-avalia/cadastro")
    api.add_resource(BuscarUsuario, "/busca-usuario")
    api.add_resource(CadastroUsuario, "/cadastro-usuario")
    api.add_resource(CadastroTurma, "/cadastro-turma")
    api.add_resource(LogoutResource, "/logout")
    api.add_resource(EditUsuario, "/usuario/editar/<int:idUsuario>")
    api.add_resource(EditAvaliacao, "/nota-avalia/editar/<int:avaliacaoId>")
    api.add_resource(DeleteAvaliacao, "/nota-avalia/deletar/<int:avaliacaoId>")
    api.add_resource(GetDisciplina, "/disciplina/")
    api.add_resource(SalvaDisciplina, "/disciplina/")
    api.add_resource(AtualizaDisciplina, "/disciplina/<int:disciplinaId>")
    api.add_resource(DeleteDisciplina, "/disciplina/<int:disciplinaId>")
    api.add_resource(GetEquipe, "/equipe/")
    api.add_resource(SalvaEquipe, "/equipe/")
    api.add_resource(AtualizaEquipe, "/equipe/<int:id>")
    api.add_resource(DeleteEquipe, "/equipe/<int:id>")
    api.add_resource(GetSala, "/sala/")
    api.add_resource(SalvaSala, "/sala/")
    api.add_resource(AtualizaSala, "/sala/<int:id>")
    api.add_resource(DeleteSala, "/sala/<int:id>")
    api.add_resource(AtualizaHabilidades, '/api/v1/habilidades/')
    api.add_resource(DeleteTurma, "/turma/<int:id>")
    app.register_blueprint(bp)

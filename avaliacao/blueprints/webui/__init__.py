from flask import Blueprint

from .views import *
bp = Blueprint("webui", __name__, template_folder="templates")

## inicialização para rotas de tela: html

bp.add_url_rule("/", view_func=home)
bp.add_url_rule("/login", view_func=login)
bp.add_url_rule('/inserir-notas', view_func=inserir_notas)
bp.add_url_rule('/cadastrar-avaliacao', view_func=cadastro_avaliacao)
bp.add_url_rule('/cadastro-turma', view_func=cadastro_turma)
bp.add_url_rule('/tabela-avaliacao-turma/<int:item_id>/<int:id_turma>', view_func=tabela_avaliacao_turma)
bp.add_url_rule('/visualiza-media', view_func=visualiza_media)
bp.add_url_rule('/visualiza-avaliacao/<int:item_id>', view_func=visualiza_avaliacao)
bp.add_url_rule('/edita-avaliacao/<int:item_id>', view_func=edita_avaliacao)
bp.add_url_rule('/edita-usuario/<int:item_id>', view_func=edita_usuario)
bp.add_url_rule('/cadastro-usuario', view_func=cadastro_usuario)
bp.add_url_rule('/boletim/<string:item_nome>/<int:id_turma>', view_func=visualiza_boletim)
bp.add_url_rule('/usuarios', view_func=visualiza_usuarios)
bp.add_url_rule('/tabela-disciplina', view_func=disciplinaView)
bp.add_url_rule('/form-disciplina', view_func=formDisciplinaView)
bp.add_url_rule('/edita-disciplina/<int:id>', view_func=edita_disciplina)
bp.add_url_rule('/visualiza-disciplina/<int:id>', view_func=visualiza_disciplina)
bp.add_url_rule('/tabela-equipe', view_func=equipeView)
bp.add_url_rule('/form-equipe', view_func=formEquipeView)
bp.add_url_rule('/edita-equipe/<int:id>', view_func=edita_equipe)
bp.add_url_rule('/visualiza-equipe/<int:id>', view_func=visualiza_equipe)
bp.add_url_rule('/tabela-sala', view_func=salaView)
bp.add_url_rule('/form-sala', view_func=formSalaView)
bp.add_url_rule('/edita-sala/<int:id>', view_func=edita_sala)
bp.add_url_rule('/visualiza-sala/<int:id>', view_func=visualiza_sala)
bp.add_url_rule('/turmas/<int:item_id>', view_func=visualiza_turmas)
bp.add_url_rule('/gerenciamento', view_func=gerenciamento)

def init_app(app):
    app.register_blueprint(bp)

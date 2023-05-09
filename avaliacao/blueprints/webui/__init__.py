from flask import Blueprint

from .views import cadastro_usuario, edita_avaliacao, home, inserir_notas, cadastro_avaliacao, tabela_avaliacao_turma, visualiza_avaliacao, visualiza_media, login, visualiza_boletim, visualiza_usuarios

bp = Blueprint("webui", __name__, template_folder="templates")

## inicialização para rotas de tela: html

bp.add_url_rule("/", view_func=home)
bp.add_url_rule("/login", view_func=login)
bp.add_url_rule('/inserir-notas', view_func=inserir_notas)
bp.add_url_rule('/cadastrar-avaliacao', view_func=cadastro_avaliacao)
bp.add_url_rule('/tabela-avaliacao-turma/<int:item_id>', view_func=tabela_avaliacao_turma)
bp.add_url_rule('/visualiza-media', view_func=visualiza_media)
bp.add_url_rule('/visualiza-avaliacao/<int:item_id>', view_func=visualiza_avaliacao)
bp.add_url_rule('/edita-avaliacao/<int:item_id>', view_func=edita_avaliacao)
bp.add_url_rule('/cadastro-usuario', view_func=cadastro_usuario)
bp.add_url_rule('/boletim/<string:item_nome>', view_func=visualiza_boletim)
bp.add_url_rule('/usuarios', view_func=visualiza_usuarios)

def init_app(app):
    app.register_blueprint(bp)

from flask import Blueprint

<<<<<<< HEAD
from .views import index, inserir_notas, cadastro_avaliacao, tabela_avaliacao_turma, visualiza_media
=======
from .views import cadastro_usuario, home, inserir_notas, cadastro_avaliacao, tabela_avaliacao_turma, visualiza_avaliacao, visualiza_media, login, visualiza_boletim
>>>>>>> 8e97432adb7cd84f7a1a8062ac6126d72675adf9

bp = Blueprint("webui", __name__, template_folder="templates")

## inicialização para rotas de tela: html
<<<<<<< HEAD

bp.add_url_rule("/", view_func=index)
bp.add_url_rule('/inserir-notas', view_func=inserir_notas)
bp.add_url_rule('/cadastrar-avaliacao', view_func=cadastro_avaliacao)
bp.add_url_rule('/tabela-avaliacao-turma', view_func=tabela_avaliacao_turma)
bp.add_url_rule('/visualiza-media', view_func=visualiza_media)


=======
>>>>>>> 8e97432adb7cd84f7a1a8062ac6126d72675adf9

bp.add_url_rule("/", view_func=home)
bp.add_url_rule("/login", view_func=login)
bp.add_url_rule('/inserir-notas', view_func=inserir_notas)
bp.add_url_rule('/cadastrar-avaliacao', view_func=cadastro_avaliacao)
bp.add_url_rule('/tabela-avaliacao-turma', view_func=tabela_avaliacao_turma)
bp.add_url_rule('/visualiza-media', view_func=visualiza_media)
bp.add_url_rule('/visualiza-avaliacao/<int:item_id>', view_func=visualiza_avaliacao)
bp.add_url_rule('/cadastro-usuario', view_func=cadastro_usuario)
bp.add_url_rule('/boletim/<string:item_nome>', view_func=visualiza_boletim)

def init_app(app):
    app.register_blueprint(bp)

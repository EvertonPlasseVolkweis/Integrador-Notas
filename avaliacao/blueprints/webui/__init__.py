from flask import Blueprint

from .views import index, inserir_notas, cadastro_avaliacao

bp = Blueprint("webui", __name__, template_folder="templates")

## inicialização para rotas de tela: html

bp.add_url_rule("/", view_func=index)
bp.add_url_rule('/inserir-notas', view_func=inserir_notas)
bp.add_url_rule('/cadastrar-avaliacao', view_func=cadastro_avaliacao)




def init_app(app):
    app.register_blueprint(bp)

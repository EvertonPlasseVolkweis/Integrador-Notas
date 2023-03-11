from flask import Blueprint

from .views import index, inserir_notas

bp = Blueprint("webui", __name__, template_folder="templates")

bp.add_url_rule("/", view_func=index)
bp.add_url_rule('/notas', view_func=inserir_notas, methods=['POST'])




def init_app(app):
    app.register_blueprint(bp)

from flask import abort, jsonify
from flask_restful import Resource

from avaliacao.models import Usuario, Avaliacao

class UsuariosResource(Resource):
    def get(self):
        ## modelo de get
        usuario = Usuario.query.all() or abort(204)
        ##
        return jsonify(
            {"usuario": "lincon"}
        )


class CadastroAvaliacaoResource(Resource):
    def post(self):
        ## modelo de psot
        avaliacao = Avaliacao.query
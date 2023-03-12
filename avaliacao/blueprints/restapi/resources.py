from flask import abort, jsonify, request
from flask_restful import Resource
from avaliacao.ext.database import db

from avaliacao.models import Usuario, Avaliacao, Turma

class UsuariosResource(Resource):
    def get(self):
        ## modelo de get
        usuarios = Usuario.query.all() or abort(204)
        ##
        return jsonify(
            {"usuario": [usuario.to_dict() for usuario in usuarios]}
        )


class CadastroAvaliacaoResource(Resource):
    ## modelo post
    def post(self):
        dados = request.get_json()
        novaAvaliacao = Avaliacao(titulo=dados['avaliacao'], descricao=dados['descricao'], data_inicio=0, data_fim=0, fk_id_usuario=1)
        db.session.add(novaAvaliacao)
        db.session.commit()
        avaliacaoSaved = Avaliacao.query.filter_by(titulo=dados['avaliacao']).first()
        turma = Turma.query.filter_by(fk_id_usuario=dados['usuario']).first() or abort(
        404, "Turma não encontrada"
        )
        turma.fk_id_avaliacao = avaliacaoSaved.id
        db.session.add(turma)
        db.session.commit()
        return avaliacaoSaved.id


class BuscarAvaliacaoResource(Resource):
    def get(self):
        avaliacoes = Avaliacao.query.all() or abort(204)
        return jsonify(
            {"avaliacao": [avaliacao.to_dict() for avaliacao in avaliacoes]}
        )


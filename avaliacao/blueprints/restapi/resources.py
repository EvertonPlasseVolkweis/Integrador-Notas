from flask import abort, jsonify, redirect, render_template, request, url_for
from flask_restful import Resource
from avaliacao.ext.database import db

from avaliacao.models import HabilidadeAtitude, NotaAvalia, Usuario, Avaliacao, Turma, Usuario


class UsuariosResource(Resource):
    def get(self):
        # modelo de get
        usuarios = Usuario.query.all() or abort(204)
        ##
        return jsonify(
            {"usuario": [usuario.to_dict() for usuario in usuarios]}
        )


class CadastroAvaliacaoResource(Resource):
    # modelo post
    def post(self):
        dados = request.get_json()
        print(dados)
        novaAvaliacao = Avaliacao(
            titulo=dados['avaliacao'], descricao=dados['descricao'], data_inicio=0, data_fim=0, fk_id_usuario=1)
        db.session.add(novaAvaliacao)
        db.session.commit()
        avaliacaoSaved = Avaliacao.query.filter_by(
            titulo=dados['avaliacao']).first()
        turma = Turma.query.filter_by(fk_id_usuario=dados['usuario']).first() or abort(
            404, "Turma não encontrada"
        )
        turma.fk_id_avaliacao = avaliacaoSaved.id
        db.session.add(turma)
        db.session.commit()
        return avaliacaoSaved.id


class NotaAvaliaResource(Resource):
    # modelo post
    def post(self):
        dados = request.get_json()
        print(dados)

        # Iterar sobre os dados recebidos e criar um objeto NotaAvalia para cada habilidade/atitude
        for nome_habilidade, valor in dados.items():
            habilidade_atitude = HabilidadeAtitude.query.filter_by(
                titulo=nome_habilidade).first()
            if habilidade_atitude is not None:
                nota_avalia = NotaAvalia(
                    fk_id_avaliacao=1, fk_id_habilidade_atitude=habilidade_atitude.id, comentario='', valor=valor)
                db.session.add(nota_avalia)

        # Commitar as mudanças no banco de dados
        db.session.commit()

        # Retornar uma resposta de sucesso
        return {'message': 'Notas salvas com sucesso.'}, 200


class BuscarAvaliacaoResource(Resource):
    def get(self):
        avaliacoes = Avaliacao.query.all() or abort(204)
        return jsonify(
            {"avaliacao": [avaliacao.to_dict() for avaliacao in avaliacoes]}
        )

class BuscarUsuario(Resource):
    def get(self):
        dados = request.get_json()
        print(dados)
        user = Usuario.query.filter_by(login=dados['usuario'], senha=dados['senha']).first() or abort(204)
        if user:
            return True
        else:
            return False
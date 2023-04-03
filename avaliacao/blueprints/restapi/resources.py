from datetime import datetime
from flask import abort, jsonify, make_response, redirect, render_template, request, url_for
from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse
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
            titulo=dados['avaliacao'], descricao=dados['descricao'], data_inicio=0, data_fim=0, fk_id_usuario=dados['usuario'])
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
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', type=str, required=True, help='Usuário é obrigatório.')
        self.parser.add_argument('senha', type=str, required=True, help='Senha é obrigatória.')

    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['senha']
        user = Usuario.query.filter_by(email=email, senha=password).first() or abort(204)
        if user:
            access_token = create_access_token(identity=email)
            response = make_response({"message": "Login bem-sucedido"}, 200)
            response.set_cookie("access_token", access_token, httponly=True)
            return response
        else:
            return {'error': 'Nome de usuário ou senha incorretos!'}, 401


class CadastroUsuario(Resource):
    def post(self):
        dados = request.get_json()
        print(dados)
        cpf = dados['cpf']
        login = dados['login']
        email = dados['email']
        senha = dados['senha']
        fk_id_grupo = dados['grupo']
        fk_id_perfil = dados['perfil']
        nome = dados['nome']
        ra = dados['ra']
        usuario = Usuario(cpf=cpf, login=login, email=email, senha=senha, fk_id_grupo=fk_id_grupo, fk_id_perfil=fk_id_perfil, data_cadastro=datetime.utcnow(), nome=nome, ra=ra)
        db.session.add(usuario)
        db.session.commit()
        response = make_response({"message": "Usuario salvo"}, 200)
        return response
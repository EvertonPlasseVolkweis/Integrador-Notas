from sqlalchemy import text
from datetime import datetime
from flask import abort, jsonify, make_response, redirect, render_template, request, url_for
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource, reqparse
from avaliacao.ext.database import db
from sqlalchemy.orm.exc import NoResultFound

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
    def post(self, idUsuario):
        dados = request.get_json()
        print(idUsuario)
        print(idUsuario)
        print(idUsuario)
        # Verifica se já existe uma avaliação com o mesmo título
        existing_avaliacao = Avaliacao.query.filter_by(titulo=dados['avaliacao']).first()
        if existing_avaliacao:
            abort(409, "Avaliação já existente com o mesmo título.")
        novaAvaliacao = Avaliacao(
            titulo=dados['avaliacao'], descricao=dados['descricao'], tipo_avaliacao=dados['tipo_avaliacao'], data_inicio=0, data_fim=0,
            fk_id_usuario=dados['usuario'], fk_id_usuario_avaliador=idUsuario, fk_id_turma=dados['turma'])
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
        idAvaliacao = dados['avaliacao']

        # Iterar sobre os dados recebidos e criar um objeto NotaAvalia para cada habilidade/atitude
        for nome_habilidade, valor in dados.items():
            habilidade_atitude = HabilidadeAtitude.query.filter_by(
                titulo=nome_habilidade).first()
            if habilidade_atitude is not None:
                print(valor)
                if valor != '':
                    nota_avalia = NotaAvalia(
                    fk_id_avaliacao=idAvaliacao, fk_id_habilidade_atitude=habilidade_atitude.id, comentario='', valor=valor)
                    db.session.add(nota_avalia)
        avaliacao = Avaliacao.query.filter_by(id=idAvaliacao).first() or abort(
            404, "Avaliação não encontrada"
        )
        avaliacao.tem_nota = True
        db.session.add(avaliacao)
        db.session.commit()
        # Commitar as mudanças no banco de dados
        db.session.commit()

        # Retornar uma resposta de sucesso
        return {'message': 'Notas salvas com sucesso.'}, 200


class BuscarAvaliacaoResource(Resource):
    def get(self):
        consulta = text("select a.titulo, a.tipo_avaliacao, u.nome, s.numero, d.titulo, e.apelido from avaliacao a left join turma t on t.fk_id_usuario in (a.fk_id_usuario) left join usuario u on u.id in (a.fk_id_usuario) left join sala s on s.id in (t.fk_id_sala) left join disciplina d on d.id in (t.fk_id_disciplina) left join equipe e on e.id in (t.fk_id_equipe)")
        execute = db.session.execute(consulta)
        result = execute.fetchall()
        print(result)
        return jsonify(
            {"avaliacao": [result.to_dict() for result in result]}
        )


from flask import abort

class BuscarUsuario(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'email', type=str, required=True, help='Usuário é obrigatório.')
        self.parser.add_argument(
            'senha', type=str, required=True, help='Senha é obrigatória.')

    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['senha']

        # Verifica se o email e a senha são fornecidos
        if not email or not password:
            abort(400, "Email e senha são obrigatórios.")
        
        # Verifica se o usuário existe
        user = Usuario.query.filter_by(email=email).first()
        if not user:
            abort(404, "Usuário não encontrado.")
        
        # Verifica se a senha corresponde ao usuário
        if user.senha != password:
            abort(401, "Senha incorreta.")
        
        access_token = create_access_token(identity=user.id)
        response = make_response({"message": "Login bem-sucedido"}, 200)
        response.set_cookie("access_token", access_token, httponly=True)
        return response



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
        usuario = Usuario(cpf=cpf, login=login, email=email, senha=senha, fk_id_grupo=fk_id_grupo,
                          fk_id_perfil=fk_id_perfil, data_cadastro=datetime.utcnow(), nome=nome, ra=ra)
        db.session.add(usuario)
        db.session.commit()
        response = make_response({"message": "Usuario salvo"}, 200)
        return response
    


class CadastroTurma(Resource):
    def post(self):
        dados = request.get_json()
        print(dados)
        turma_existente = Turma.query.filter_by(fk_id_usuario=dados['usuario'], fk_id_sala=dados['sala'], fk_id_disciplina=dados['disciplina']).first()
        if turma_existente:
            return {"message": "Usuario já matriculado na disciplina"}, 400
        nova_turma = Turma(fk_id_usuario=dados['usuario'], fk_id_sala=dados['sala'], fk_id_disciplina=dados['disciplina'], fk_id_equipe=dados['equipe'], fk_id_avaliacao=0)
        db.session.add(nova_turma)
        db.session.commit()
        response = make_response({"message": "Turma salva"}, 200)
        return response
    

class LogoutResource(Resource):
    def post(self):
        response = make_response(redirect('/login'))
        response.delete_cookie('access_token')
        return response
    

class EditAvaliacao(Resource):
    def put(self, avaliacaoId):
        print(avaliacaoId)
        data = request.get_json()
        print(data)
        notas = NotaAvalia.query.filter_by(fk_id_avaliacao=avaliacaoId).all()
        print(notas)
        for nota in notas:
            if nota.habilidade_atitude.titulo in data:
                nota.valor = data[nota.habilidade_atitude.titulo]
        
        db.session.commit()
        response = make_response({"message": "Notas editadas com sucesso"}, 200)
        return response
    

    
class EditUsuario(Resource):
    def put(self, idUsuario):
        data = request.get_json()
        usuario = Usuario.query.filter_by(id=idUsuario).first()
        
        if not usuario:
            return {"message": "Usuário não encontrado"}, 404
        
        if 'cpf' in data:
            usuario.cpf = data['cpf']
        if 'login' in data:
            usuario.login = data['login']
        if 'email' in data:
            usuario.email = data['email']
        if 'senha' in data:
            usuario.senha = data['senha']
        if 'fk_id_grupo' in data:
            usuario.fk_id_grupo = data['fk_id_grupo']
        if 'fk_id_perfil' in data:
            usuario.fk_id_perfil = data['fk_id_perfil']
        if 'nome' in data:
            usuario.nome = data['nome']
        if 'ra' in data:
            usuario.ra = data['ra']
        
        db.session.commit()
        
        response = make_response({"message": "Usuário editado com sucesso"}, 200)
        return response


class DeleteAvaliacao(Resource):
    def delete(self, avaliacaoId):
        print(avaliacaoId)
        avaliacao = Avaliacao.query.get(avaliacaoId)
        
        if avaliacao is None:
            return make_response({"message": "Avaliação não encontrada"}, 404)
        
        notas = NotaAvalia.query.filter_by(fk_id_avaliacao=avaliacaoId).all()
        
        for nota in notas:
            db.session.delete(nota)
        
        db.session.delete(avaliacao)
        db.session.commit()
        
        return make_response({"message": "Avaliação e notas deletadas com sucesso"}, 200)

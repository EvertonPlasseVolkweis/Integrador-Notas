from sqlalchemy import text
from datetime import datetime
from flask import abort, jsonify, make_response, redirect, render_template, request, url_for
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource, reqparse
from avaliacao.ext.database import db
from sqlalchemy.orm.exc import NoResultFound
from flask import abort
from avaliacao.models import *


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
        
        usuario = Usuario.query.get(idUsuario)

        usuario.cpf = data['cpf']
        usuario.login = data['login']
        usuario.email = data['email']
        usuario.senha = data['senha']
        usuario.fk_id_grupo = data['grupo']
        usuario.fk_id_perfil = data['perfil']
        usuario.nome = data['nome']
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
    
class GetDisciplina(Resource):
    def get(self):
        # modelo de get
        disciplinas = Disciplina.query.all() or abort(204)
        ##
        return jsonify(
            {"disciplinas": [disciplina.to_dict() for disciplina in disciplinas]}
        )
    
class SalvaDisciplina(Resource):
    def post(self):
        dados = request.get_json()
        titulo = dados['titulo']
        ementa = dados['ementa']

        # Check if the discipline already exists in the database
        existing_discipline = Disciplina.query.filter_by(titulo=titulo).first()
        if existing_discipline:
            return make_response({"message": "Disciplina já cadastrada!"}, 400)

        # If the discipline doesn't exist, create and save it
        disciplina = Disciplina(titulo=titulo, ementa=ementa)
        db.session.add(disciplina)
        db.session.commit()
        return make_response({"message": "Disciplina salva com sucesso!"}, 200)

    
class AtualizaDisciplina(Resource):
    def put(self, disciplinaId):
        dados = request.get_json()
        disciplina = Disciplina.query.get(disciplinaId)

        print(dados)

        disciplina.titulo = dados['titulo']
        disciplina.ementa = dados['ementa']

        db.session.commit()
        return make_response({"message": "Disciplina editada com sucesso!"}, 200)
    
class DeleteDisciplina(Resource):
    def delete(self, disciplinaId):
        disciplina = Disciplina.query.get(disciplinaId)


        if disciplina is None:
            return make_response({"message": "Disciplina não encontrada"}, 404)
        
        db.session.delete(disciplina)
        db.session.commit()

        return make_response({"message": "Disciplina deletada com sucesso!"}, 200)
    
class GetEquipe(Resource):
    def get(self):
        # modelo de get
        equipes = Equipe.query.all() or abort(204)
        ##
        return jsonify(
            {"equipes": [equipe.to_dict() for equipe in equipes]}
        )
    
class SalvaEquipe(Resource):
    def post(self):
        dados = request.get_json()
        apelido = dados['apelido']
        nome_projeto = dados['nome_projeto']

        # Verifica se a equipe já existe no banco de dados
        equipe_existente = Equipe.query.filter_by(apelido=apelido, nome_projeto=nome_projeto).first()
        if equipe_existente:
            return make_response({"message": "Equipe já existe"}, 400)

        # Cria uma nova equipe e a adiciona ao banco de dados
        equipe = Equipe(apelido=apelido, nome_projeto=nome_projeto)
        db.session.add(equipe)
        db.session.commit()

        return make_response({"message": "Equipe salva com sucesso!"}, 200)

    
class AtualizaEquipe(Resource):
    def put(self, id):
        dados = request.get_json()
        equipe = Equipe.query.get(id)

        equipe.apelido = dados['apelido']
        equipe.nome_projeto = dados['nome_projeto']

        db.session.commit()
        return make_response({"message": "Equipe editada com sucesso!"}, 200)
    
class DeleteEquipe(Resource):
    def delete(self, id):
        equipe = Equipe.query.get(id)

        if equipe is None:
            return make_response({"message": "Equipe não encontrada"}, 404)
        
        db.session.delete(equipe)
        db.session.commit()

        return make_response({"message": "Equipe deletada com sucesso!"}, 200)
    
class GetSala(Resource):
    def get(self):
        # modelo de get
        salas = Sala.query.all() or abort(204)
        ##
        return jsonify(
            {"salas": [sala.to_dict() for sala in salas]}
        )
    
class SalvaSala(Resource):
    def post(self):
        dados = request.get_json()
        numero_sala = dados['numero']

        # Check if the room already exists
        existing_sala = Sala.query.filter_by(numero=numero_sala).first()
        if existing_sala:
            return make_response({"message": "Sala já cadastrada"}, 400)

        # Room does not exist, create and save it
        sala = Sala(numero=numero_sala, turno='')
        db.session.add(sala)
        db.session.commit()
        return make_response({"message": "Sala salva com sucesso!"}, 200)
    
class AtualizaSala(Resource):
    def put(self, id):
        dados = request.get_json()
        sala = Sala.query.get(id)

        sala.numero = dados['numero']
        sala.turno = ''

        db.session.commit()
        return make_response({"message": "Sala editada com sucesso!"}, 200)
    
class DeleteSala(Resource):
    def delete(self, id):
        sala = Sala.query.get(id)

        if sala is None:
            return make_response({"message": "Sala não encontrada"}, 404)
        
        db.session.delete(sala)
        db.session.commit()

        return make_response({"message": "Sala deletada com sucesso!"}, 200)
    

class AtualizaHabilidades(Resource):
    def put(self):
        dados = request.get_json()
        for chave, valor in dados.items():
            habilidade = HabilidadeAtitude.query.filter_by(titulo=chave).first()
            if habilidade:
                habilidade.fator_peso = valor
                db.session.commit()
            else:
                return make_response({"message": f"Habilidade '{chave}' não encontrada"}, 404)
        return make_response({"message": "Habilidades editadas com sucesso!"}, 200)
    

class DeleteTurma(Resource):
    def delete(self, id):
        turma = Turma.query.get(id)

        if turma is None:
            return make_response({"message": "Turma não encontrada"}, 404)
                
        db.session.delete(turma)
        
        db.session.commit()

        return make_response({"message": "Turma deletada com sucesso!"}, 200)

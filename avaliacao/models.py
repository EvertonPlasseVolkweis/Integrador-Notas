from datetime import datetime
from avaliacao.ext.database import db
from sqlalchemy_serializer import SerializerMixin


class Usuario(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(255), unique=True, nullable=False)
    login = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    fk_id_grupo = db.Column(db.Integer, db.ForeignKey('grupo.id'))
    fk_id_perfil = db.Column(db.Integer, db.ForeignKey('perfil.id'))
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    nome = db.Column(db.String(255), nullable=False)
    ra = db.Column(db.Integer, unique=True, nullable=False)
    grupo = db.relationship('Grupo', backref='usuarios')
    perfil = db.relationship('Perfil', backref='usuarios')

class Grupo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grupo = db.Column(db.String(255), nullable=False)

class Perfil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    perfil = db.Column(db.String(255), nullable=False)

class Equipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apelido = db.Column(db.String(255), nullable=False)
    nome_projeto = db.Column(db.String(255), nullable=False)

class Sala(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(255), nullable=False)
    turno = db.Column(db.String(255), nullable=False)

class Disciplina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    ementa = db.Column(db.String(255), nullable=False)

class Avaliacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False, unique=True)
    descricao = db.Column(db.String(255), nullable=False)
    data_inicio = db.Column(db.Integer, nullable=False)
    data_fim = db.Column(db.Integer, nullable=False)
    fk_id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    usuario = db.relationship('Usuario', backref='avaliacoes')

class HabilidadeAtitude(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    fator_peso = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(255), nullable=False)

class NotaAvalia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fk_id_avaliacao = db.Column(db.Integer, db.ForeignKey('avaliacao.id'), nullable=False)
    fk_id_habilidade_atitude = db.Column(db.Integer, db.ForeignKey('habilidade_atitude.id'), nullable=False)
    comentario = db.Column(db.String(255), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    avaliacao = db.relationship('Avaliacao', backref='notas_avaliacoes')
    habilidade_atitude = db.relationship('HabilidadeAtitude', backref='notas_avaliacoes')

class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fk_id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fk_id_sala = db.Column(db.Integer, db.ForeignKey('sala.id'), nullable=False)
    fk_id_disciplina = db.Column(db.Integer, db.ForeignKey('disciplina.id'), nullable=False)
    fk_id_equipe = db.Column(db.Integer, db.ForeignKey('equipe.id'))
    fk_id_avaliacao = db.Column(db.Integer, db.ForeignKey('avaliacao.id'))
    usuario = db.relationship('Usuario', backref='turmas')
    sala = db.relationship('Sala', backref='turmas')
    disciplina = db.relationship('Disciplina', backref='turmas')
    equipe = db.relationship('Equipe', backref='turmas')
    avaliacao = db.relationship('Avaliacao', backref='turmas')

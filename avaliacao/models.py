from avaliacao.ext.database import db
from sqlalchemy_serializer import SerializerMixin


class Product(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    price = db.Column(db.Numeric())
    description = db.Column(db.Text)


class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(140))
    password = db.Column(db.String(512))


class NotaAvalia(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Numeric)
    comentario = db.Column(db.String(255))
    fk_avaliacao_id = db.Column(db.Integer, db.ForeignKey('avaliacao.id'))
    fk_habilidade_atitude_id = db.Column(db.Integer, db.ForeignKey('habilidade_atitude.id'))

class Avaliacao(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(60))
    descricao = db.Column(db.String(255))
    notas = db.relationship('NotaAvalia', backref='avaliacao')

class HabilidadeAtitude(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(60))
    fator_peso = db.Column(db.Numeric)
    descricao = db.Column(db.String(255))
    notas = db.relationship('NotaAvalia', backref='habilidade_atitude')

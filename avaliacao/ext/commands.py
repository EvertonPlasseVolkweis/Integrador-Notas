import click
from avaliacao.ext.database import db
from avaliacao.ext.auth import create_user
from avaliacao.models import Avaliacao, HabilidadeAtitude, NotaAvalia
from avaliacao.ext.main import MATRIZ_AVALIACAO

habilidades_atitudes = MATRIZ_AVALIACAO[1][1]
def insert_habilidade():
    for secao in MATRIZ_AVALIACAO:
        if secao[0] == "Habilidades e Atitudes":
            for habilidade in secao[1]:
                nova_habilidade = HabilidadeAtitude(titulo=habilidade, fator_peso=secao[1][habilidade], descricao="")
                db.session.add(nova_habilidade)
            for avaliacao_360 in secao[3]:
                nova_avaliacao_360 = HabilidadeAtitude(titulo=avaliacao_360, fator_peso=secao[3][avaliacao_360], descricao="")
                db.session.add(nova_avaliacao_360)
        else:
            for conhecimento in secao[1]:
                novo_conhecimento = HabilidadeAtitude(titulo=conhecimento, fator_peso=secao[1][conhecimento], descricao="")
                db.session.add(novo_conhecimento)
    db.session.commit()


def create_db():
    """Creates database"""
    db.create_all()


def drop_db():
    """Cleans database"""
    db.drop_all()

def populate_db():
    nova_avaliacao = Avaliacao(titulo='Avaliação 1', descricao='Primeira Avaliação', 
        data_inicio=20220310, data_fim=20220315, fk_id_usuario=1)
    db.session.add(nova_avaliacao)
    db.session.commit()

def insert_nota():
    avaliacao = Avaliacao.query.first()
    habilidade_atitude = HabilidadeAtitude.query.first()

    nova_nota = NotaAvalia(
        fk_id_avaliacao=avaliacao.id,
        fk_id_habilidade_atitude=habilidade_atitude.id,
        comentario="Comentário da nota",
        valor=8.5
    )

    db.session.add(nova_nota)
    db.session.commit()

def init_app(app):
    # add a single command
    @app.cli.command()
    @click.option('--username', '-u')
    @click.option('--password', '-p')
    def add_user(username, password):
        """Adds a new user to the database"""
        return create_user(username, password)
    
    @app.cli.command()
    def db_create():
        return create_db()
    
    @app.cli.command()
    def db_clear():
        return drop_db()

    @app.cli.command()
    def db_populate():
        return populate_db()
    
    @app.cli.command()
    def db_habilidade():
        return insert_habilidade()

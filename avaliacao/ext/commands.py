from datetime import datetime

import click
from sqlalchemy import null

from avaliacao.ext.auth import create_user
from avaliacao.ext.database import db
from avaliacao.ext.main import MATRIZ_AVALIACAO
from avaliacao.models import (Avaliacao, Disciplina, Equipe, Grupo,
                              HabilidadeAtitude, NotaAvalia, Perfil, Sala,
                              Turma, Usuario)

habilidades_atitudes = MATRIZ_AVALIACAO[1][1]
def insert_habilidade():
    for secao in MATRIZ_AVALIACAO:
        for item in secao[1]:
            nova_habilidade = HabilidadeAtitude(titulo=item, fator_peso=secao[1][item], descricao="")
            db.session.add(nova_habilidade)
    db.session.commit()


def insert_equipe():
    nova_equipe = Equipe(apelido='Equipe 2', nome_projeto='Projeto II')
    db.session.add(nova_equipe)
    db.session.commit()

def insert_disciplina():
    nova_disciplina = Disciplina(titulo='Projeto II', ementa='Projeto II')
    db.session.add(nova_disciplina)
    db.session.commit()

def insert_sala():
    nova_sala = Sala(numero='201', turno='Noturno')
    db.session.add(nova_sala)
    db.session.commit()

def insert_grupo():
    grupo_professores = Grupo(grupo='Professores')
    novo_grupo = Grupo(grupo='Alunos')
    db.session.add(grupo_professores)
    db.session.add(novo_grupo)
    db.session.commit()

def insert_perfil():
    perfil_admin = Perfil(perfil='admin')
    perfil_professor = Perfil(perfil='professor')
    perfil_aluno = Perfil(perfil='aluno')
    db.session.add(perfil_admin)
    db.session.add(perfil_professor)
    db.session.add(perfil_aluno)
    db.session.commit()

def insert_usuario():
    data_cadastro = datetime(2022, 3, 12)
    usuario_profesoor = Usuario(cpf='12345678900', login='Professor Linguiça', email='a@a', senha='123123', fk_id_grupo=1, fk_id_perfil=1, data_cadastro=data_cadastro, nome='Professor Linguiça', ra=111111)
    usuario_aluno = Usuario(cpf='11111111100', login='Lincola', email='l@l', senha='123123', fk_id_grupo=2, fk_id_perfil=3, data_cadastro=data_cadastro, nome='Lincola', ra=222222)
    db.session.add(usuario_profesoor)
    db.session.add(usuario_aluno)
    db.session.commit()

def insert_turma():
    nova_turma = Turma(fk_id_usuario=1, fk_id_sala=1, fk_id_disciplina=1, fk_id_equipe=1, fk_id_avaliacao=0)
    db.session.add(nova_turma)
    db.session.commit()

def create_db():
    """Creates database"""
    db.create_all()


def drop_db():
    """Cleans database"""
    db.drop_all()


def populate_db():
    """Populate db with sample data"""
    data = [
        Sala(
            id=1, numero="1", turno="a"
        ),
        Sala(id=2, numero="2", turno="a"),
        Sala(id=3, numero="3", turno="a"),
    ]
    db.session.bulk_save_objects(data)
    db.session.commit()
    return Sala.query.all()

def insert_avaliacao():
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
    def db_avaliacao():
        return insert_avaliacao()
    
    @app.cli.command()
    def db_habilidade():
        return insert_habilidade()
    
    @app.cli.command()
    def db_equipe():
        return insert_equipe()
    
    @app.cli.command()
    def db_disciplina():
        return insert_disciplina()
    
    @app.cli.command()
    def db_sala():
        return insert_sala()
    
    @app.cli.command()
    def db_perfil():
        return insert_perfil()
    
    @app.cli.command()
    def db_grupo():
        return insert_grupo()
    
    @app.cli.command()
    def db_usuario():
        return insert_usuario()
    
    @app.cli.command()
    def db_turma():
        return insert_turma()

import click
from sqlalchemy import null
from avaliacao.ext.database import db
from avaliacao.ext.auth import create_user
from avaliacao.models import Avaliacao, Disciplina, Equipe, Grupo, HabilidadeAtitude, NotaAvalia, Perfil, Sala, Usuario, Turma
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
    novo_grupo = Grupo(grupo='Grupo 2')
    db.session.add(grupo_professores)
    db.session.add(novo_grupo)
    db.session.commit()

def insert_perfil():
    perfil_professor = Perfil(perfil='Professor')
    perfil_aluno = Perfil(perfil='Aluno')
    db.session.add(perfil_professor)
    db.session.add(perfil_aluno)
    db.session.commit()

def insert_usuario():
    usuario_profesoor = Usuario(cpf='12345678900', login='Professor', email='usuario@professor.com', senha='12345678', fk_id_grupo=1, fk_id_perfil=1, data_cadastro=20220312, nome='Professor', ra=111111)
    usuario_aluno = Usuario(cpf='11111111100', login='Aluno', email='usuario@aluno.com', senha='12345678', fk_id_grupo=2, fk_id_perfil=2, data_cadastro=20220312, nome='Aluno', ra=222222)
    db.session.add(usuario_profesoor)
    db.session.add(usuario_aluno)
    db.session.commit()

def insert_turma():
    nova_turma = Turma(fk_id_usuario=2, fk_id_sala=1, fk_id_disciplina=1, fk_id_equipe=1, fk_id_avaliacao=0)
    db.session.add(nova_turma)
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

from flask import abort, render_template, request
from avaliacao.ext.main import MATRIZ_AVALIACAO, calcular_media
from avaliacao.models import Avaliacao, HabilidadeAtitude, NotaAvalia, Usuario, Turma, Sala, Disciplina, Equipe
from avaliacao.ext.database import db


def index():
    return render_template("index.html")

def inserir_notas():
    matriz = MATRIZ_AVALIACAO
    return render_template("inserir.html", matriz_avaliacao = matriz)

def cadastro_avaliacao():
    usuario = Usuario.query.all()
    return render_template("cadastro-avaliacao.html", usuarios=usuario)

def tabela_avaliacao_turma():
    turmas = Turma.query.all()
    lista = []
    for turma in turmas:
        usuario = Usuario.query.filter_by(id=turma.fk_id_usuario).first()
        sala = Sala.query.filter_by(id=turma.fk_id_sala).first()
        disciplina = Disciplina.query.filter_by(id=turma.fk_id_disciplina).first()
        equipe = Equipe.query.filter_by(id=turma.fk_id_equipe).first()
        avaliacao = Avaliacao.query.filter_by(id=turma.fk_id_avaliacao).first()
        lista.append({"nome": usuario.nome, "sala": sala.numero, "disciplina": disciplina.titulo, "equipe": equipe.apelido, "avaliacao": avaliacao.titulo})
    
    return render_template("tabela-avaliacao-turma.html", data=lista)




from flask import abort, render_template, request
from avaliacao.ext.main import MATRIZ_AVALIACAO, calcular_media, MATRIZ_AVALIACAO_TESTE
from avaliacao.models import Avaliacao, HabilidadeAtitude, NotaAvalia, Usuario, Turma, Sala, Disciplina, Equipe
from avaliacao.ext.database import db


def index():
    return render_template("index.html")

def login():
    return render_template("login-teste.html")

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

def visualiza_media():
    todas_notas = []
    avaliacao_id = 1  # a fk_id_avaliacao desejada
    notas_avaliacao = NotaAvalia.query.filter_by(fk_id_avaliacao=avaliacao_id).all()
    notas = [int(nota.valor) for nota in notas_avaliacao]


    sub_listas = []
    sub_lista = []
    contagem = 0
    for elemento in notas:
        if contagem == 13:
            sub_listas.append(sub_lista)
            sub_lista = []
            contagem = 0
        sub_lista.append(elemento)
        contagem += 1
    sub_listas.append(sub_lista)
    
    for notinha in sub_listas:
        newNotas = []
        for categoria in MATRIZ_AVALIACAO:
            notas_categoria = []
            for criterio, peso in categoria[1].items():
                nota = float(notinha.pop(0))
                notas_categoria.append(nota)
            newNotas.append(notas_categoria)
        todas_notas.append(newNotas)
    print(todas_notas)
    soma_total = 0
    n_total = 0
    for notas in todas_notas:
        notas_total = sum(sum(categoria) for categoria in notas)
        peso_total = sum(categoria[2] for categoria in MATRIZ_AVALIACAO)
        media = notas_total / peso_total
        soma_total += media
        n_total += 1
    media_final = soma_total / n_total

    return render_template("inserido.html", media_final=media_final)



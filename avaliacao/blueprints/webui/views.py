from flask import abort, render_template, request
from avaliacao.ext.main import MATRIZ_AVALIACAO, calcular_media


def index():
    return render_template("index.html")

def inserir_notas():
    matriz = MATRIZ_AVALIACAO
    return render_template("inserir.html", matriz_avaliacao = matriz)

def cadastro_avaliacao():
    return render_template("cadastro-avaliacao.html")




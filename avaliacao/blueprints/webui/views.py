from flask import abort, render_template, request
from avaliacao.ext.main import MATRIZ_AVALIACAO, calcular_media


def index():
    matriz = MATRIZ_AVALIACAO
    return render_template("inserir.html", matriz_avaliacao = matriz)

def inserir_notas():
    todas_notas = []

    notas = []
    for categoria in MATRIZ_AVALIACAO:
        notas_categoria = []
        for criterio, peso in categoria[1].items():
            nota = float(request.form[f"{categoria[0]}-{criterio}"])
            notas_categoria.append(nota)
        notas.append(notas_categoria)
        if len(categoria) > 2 and isinstance(categoria[2], dict):
            avaliacoes_360 = {}
            for avaliador, peso in categoria[2].items():
                nota = float(request.form[f"{categoria[0]}-{avaliador}"])
                avaliacoes_360[avaliador] = nota
            notas[-1].append(avaliacoes_360)

    todas_notas.append(notas)
    media_total = calcular_media(todas_notas)

    print(media_total)

    return render_template("inserido.html", media_total=media_total)



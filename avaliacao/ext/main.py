from flask import Flask, render_template, request
import json

app = Flask(__name__)

MATRIZ_AVALIACAO_TESTE = {
    'Conhecimentos': {
        'porcentagem': 70,
        'Avaliação objetiva': 15,
        'Unidades de Aprendizagem (Uas)': 10,
        'Avaliação dissertativa': 30,
        'Entrega': 15
    },
    'Habilidades e Atitudes': {
        'porcentagem': 30,
        'Habilidades': {
            'Comunicação Oral e Escrita': 10,
            'Cognitivo': 10
        },
        'Atitudes': {
            'Autogestão': 2.5,
            'Autonomia': 2.5,
            'Protagonismo': 2.5,
            'Interação': 2.5
        }
    },
}

<<<<<<< HEAD
    # 'Avaliação 360º': {
    #     'porcentagem': 30,
    #     'Autoavaliação': 3,
    #     'Avaliação da equipe': 3,
    #     'Avaliação do professor': 24
    # }

# Define a matriz de avaliação como constante
=======

# # Define a matriz de avaliação como constante
# MATRIZ_AVALIACAO = [
#     # Conhecimentos
#     ["Conhecimentos", {"Avaliação objetiva": 0.15, "Unidades de Aprendizagem (Uas)": 0.1, "Avaliação dissertativa": 0.3, "Entrega": 0.15}, 0.7],
    
#     # Habilidades e Atitudes
#     ["Habilidades e Atitudes", 
#      {"Comunicação Oral e Escrita": 0.1, "Cognitivo": 0.1, "Autogestão": 0.025, "Autonomia": 0.025, "Protagonismo": 0.025, "Interação": 0.025},
#      0.3,
#      # Avaliação 360º
#      {"Autoavaliação": 0.03, "Equipe": 0.03, "Professor": 0.24}
#     ]
# ]

>>>>>>> 8e97432adb7cd84f7a1a8062ac6126d72675adf9
MATRIZ_AVALIACAO = [
    # Conhecimentos
    ["Conhecimentos", {"Avaliação objetiva": 0.15, "Unidades de Aprendizagem (Uas)": 0.1, "Avaliação dissertativa": 0.3, "Entrega": 0.15}, 0.7],
    
    # Habilidades e Atitudes
    ["Habilidades e Atitudes", {"Comunicação Oral e Escrita": 0.1, "Cognitivo": 0.1, "Autogestão": 0.025, "Autonomia": 0.025, "Protagonismo": 0.025, "Interação": 0.025}, 0.3]
]

# Define uma função para calcular a média das notas
def calcular_media(todas_notas):
    soma_total = 0
    n_total = 0
    for notas in todas_notas:
        notas_total = sum(sum(categoria) for categoria in notas)
        peso_total = sum(categoria[2] for categoria in MATRIZ_AVALIACAO)
        media = notas_total / peso_total
        soma_total += media
        n_total += 1

    media_total = soma_total / n_total
    return media_total

# Define uma função para salvar as notas em um arquivo JSON
def salvar_notas_json(todas_notas):
    with open("notas.json", "w") as f:
        json.dump(todas_notas, f)

# Define uma função para carregar as notas de um arquivo JSON
def carregar_notas_json():
    try:
        with open("notas.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Define a rota raiz para a página de inserção de notas
@app.route('/notas', methods=['GET', 'POST'])
def inserir_notas():
    if request.method == 'POST':
        todas_notas = carregar_notas_json()

        notas = []
        for categoria in MATRIZ_AVALIACAO:
            notas_categoria = []
            for criterio, peso in categoria[1].items():
                nota = float(request.form[f"{categoria[0]}-{criterio}"])
                notas_categoria.append(nota)
            notas.append(notas_categoria)
            if len(categoria) > 2:
                avaliacoes_360 = {}
                for avaliador, peso in categoria[3].items():
                    nota = float(request.form[f"{categoria[0]}-{avaliador}"])
                    avaliacoes_360[avaliador] = nota
                notas[-1].append(avaliacoes_360)

        todas_notas.append(notas)
        media_total = calcular_media(todas_notas)

        print(media_total)

        salvar_notas_json(todas_notas)

        return render_template("inserido.html", media_total=media_total)

if __name__ == '_main_':
    app.run()
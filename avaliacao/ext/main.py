# from reportlab.pdfgen import canvas

# Definindo a matriz de avaliação
matriz_avaliacao = [
    # Conhecimentos
    ["Conhecimentos", {"Avaliação objetiva": 0.15,
    "Unidades de Aprendizagem (Uas)": 0.1, "Avaliação dissertativa": 0.3, "Entrega": 0.15}, 0.7],

    # Habilidades e Atitudes
    ["Habilidades e Atitudes",
        {"Comunicação Oral e Escrita": 0.1, "Cognitivo": 0.1, "Autogestão": 0.025,
        "Autonomia": 0.025, "Protagonismo": 0.025, "Interação": 0.025},
        0.3,
        # Avaliação 360º
        {"Autoavaliação": 0.03, "Equipe": 0.03, "Professor": 0.24}
    ]
]

# Lista para armazenar todas as notas inseridas
todas_notas = []

# Loop para permitir que o usuário insira as notas várias vezes
while True:
    notas = []
    for categoria in matriz_avaliacao:
        print(f"Avaliação para a categoria: {categoria[0]}")
        notas_categoria = []
        for criterio, peso in categoria[1].items():
            while True:
                nota = float(input(f"Informe a nota de 0 a 10 para o critério '{criterio}' (peso {peso*100}%): "))
                if nota <= 10:
                    break
                print("Entrada inválida, tente novamente.")
            print("Entrada aceita:", nota)
            notas_categoria.append(nota)
        notas.append(notas_categoria)
        print()
    todas_notas.append(notas)

    # Pergunta se o usuário quer inserir mais notas
    continuar = input("Deseja inserir mais notas? (s/n): ")
    if continuar.lower() != "s":
        break

# Cálculo da média total
soma_total = 0
n_total = 0
for notas in todas_notas:
    notas_total = sum(sum(categoria) for categoria in notas)
    peso_total = sum(categoria[2] for categoria in matriz_avaliacao)
    media = notas_total / peso_total
    soma_total += media
    n_total += 1

media_total = soma_total / n_total

print(f"A média total das notas é: {media_total:.2f}")
# # Crie um arquivo PDF
# pdf = canvas.Canvas("exemplo.pdf")

# # Escreva o texto no PDF
# pdf.drawString(100, 750, "Exemplo de texto em PDF com Python")

# # Salve o PDF
# pdf.save()

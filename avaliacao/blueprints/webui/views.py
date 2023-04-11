from functools import wraps
from flask import abort, redirect, render_template, request
from flask_jwt_extended import decode_token, get_jwt_identity, jwt_required, verify_jwt_in_request
from avaliacao.ext.main import MATRIZ_AVALIACAO, calcular_media, MATRIZ_AVALIACAO_TESTE
from avaliacao.models import Avaliacao, Grupo, HabilidadeAtitude, NotaAvalia, Perfil, Usuario, Turma, Sala, Disciplina, Equipe
from avaliacao.ext.database import db
from sqlalchemy import text
import json



def login_required(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            return redirect("/login")

        return view_function(*args, **kwargs)

    return decorated_function


def login():
    return render_template("login-teste.html")


@login_required
def home():
    return render_template("index.html")


@login_required
def cadastro_usuario():
    grupos = Grupo.query.all()
    perfis = Perfil.query.all()
    equipe = Equipe.query.all()
    sala = Sala.query.all()
    disciplina = Disciplina.query.all()
    return render_template("cadastro-usuario.html", grupos=grupos, perfis=perfis, equipe=equipe, sala=sala, disciplina=disciplina)


@login_required
def inserir_notas():
    verify_jwt_in_request()
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    grupo = Grupo.query.filter_by(id=user.fk_id_grupo).first()
    avaliacao = Avaliacao.query.filter_by(tem_nota=False).all()
    matriz = MATRIZ_AVALIACAO
    return render_template("inserir.html", matriz_avaliacao=matriz, grupo=grupo, avaliacao=avaliacao)


@login_required
def cadastro_avaliacao():
    usuario = Usuario.query.all()
    verify_jwt_in_request()
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    grupo = Grupo.query.filter_by(id=user.fk_id_grupo).first()
    return render_template("cadastro-avaliacao.html", usuarios=usuario, grupo=grupo)


@login_required
def tabela_avaliacao_turma():
    turmas = Turma.query.all()
    print(turmas)
    lista = []
    for turma in turmas:
        usuario = Usuario.query.filter_by(id=turma.fk_id_usuario).first()
        sala = Sala.query.filter_by(id=turma.fk_id_sala).first()
        disciplina = Disciplina.query.filter_by(
            id=turma.fk_id_disciplina).first()
        equipe = Equipe.query.filter_by(id=turma.fk_id_equipe).first()
        avaliacao = Avaliacao.query.filter_by(id=turma.fk_id_avaliacao).first()
        if usuario and sala and disciplina and equipe and avaliacao:
            lista.append({"tipo_avaliacao": avaliacao.tipo_avaliacao, "nome": usuario.nome, "sala": sala.numero, "disciplina": disciplina.titulo,
                         "equipe": equipe.apelido, "avaliacao": avaliacao.titulo, "id": avaliacao.id})
    return render_template("tabela-avaliacao-turma.html", data=lista)


@login_required
def visualiza_media():
    todas_notas = []
    avaliacao_id = 1  # a fk_id_avaliacao desejada
    notas_avaliacao = NotaAvalia.query.filter_by(
        fk_id_avaliacao=avaliacao_id).all()
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


@login_required
def visualiza_avaliacao(item_id):
    print(item_id)
    verify_jwt_in_request()
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    grupo = Grupo.query.filter_by(id=user.fk_id_grupo).first()
    matriz = MATRIZ_AVALIACAO
    avaliacao = Avaliacao.query.filter_by(id=item_id).first()
    notaAvalia = NotaAvalia.query.filter_by(fk_id_avaliacao=avaliacao.id).all()
    print(notaAvalia)
    return render_template("inserir.html", matriz_avaliacao=matriz, grupo=grupo, notaAvalia=notaAvalia, visualizando=True)

@login_required
def visualiza_boletim(item_nome):
    usuario = Usuario.query.filter_by(nome=item_nome).first()
    consulta = text("select av.titulo, av.descricao, av.tipo_avaliacao, JSON_GROUP_ARRAY(json_object('titulo', ha.titulo, 'nota', na.valor, 'fator_peso', ha.fator_peso)) AS notas from avaliacao av left join nota_avalia na on na.fk_id_avaliacao = av.id  left join habilidade_atitude ha on ha.id = na.fk_id_habilidade_atitude left join usuario us on us.id = av.fk_id_usuario left join grupo g on g.id = us.fk_id_grupo where av.fk_id_usuario = :idUsuario group by av.id")
    parametros = {'idUsuario': usuario.id} 
    execute = db.session.execute(consulta, parametros)
    result = execute.fetchall()

    array = []
    
    # Cria um dicionário para armazenar as médias de cada avaliação
    medias = {}

    # Armazena a soma total das notas de todas as avaliações
    soma_total = 0

    # Percorre cada avaliação na lista de dados
    for avaliacao in result:
        # Converte a string em um dicionário
        aval_dict = json.loads(avaliacao[3])
        
        # Calcula a média da avaliação
        media = sum([a['nota'] * a['fator_peso'] for a in aval_dict]) / sum([a['fator_peso'] for a in aval_dict])
        
        # Armazena a média no dicionário medias
        medias[avaliacao[0]] = media
        
        # Arredonda a média para duas casas decimais
        media_arredondada = round(media, 2)

        array.append({"titulo": avaliacao[0], "descricao": avaliacao[1], "tipo": avaliacao[2], "media": media_arredondada})
        
        # Adiciona a nota total ao somatório
        soma_total += sum([a['nota'] for a in aval_dict])
    
    soma_total = round(soma_total / len(result), 2)


    return render_template("boletim.html", data=array, media_total=soma_total)

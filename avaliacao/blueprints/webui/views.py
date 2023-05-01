from functools import wraps
from flask import abort, redirect, render_template, request
from flask_jwt_extended import decode_token, get_jwt_identity, jwt_required, verify_jwt_in_request
from avaliacao.ext.main import MATRIZ_AVALIACAO, calcular_media, MATRIZ_AVALIACAO_TESTE
from avaliacao.models import Avaliacao, Grupo, HabilidadeAtitude, NotaAvalia, Perfil, Usuario, Turma, Sala, Disciplina, Equipe
from avaliacao.ext.database import db
from sqlalchemy import text
from flask import flash, redirect, url_for
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
    usuario = []
    verify_jwt_in_request()
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    grupo = Grupo.query.filter_by(id=user.fk_id_grupo).first()
    if grupo.grupo == "Alunos":
        consulta = text("""
            SELECT u.nome, t.fk_id_equipe, u.id
            FROM usuario u
            LEFT JOIN turma t ON t.fk_id_usuario = u.id
            WHERE t.fk_id_equipe = (
                SELECT t2.fk_id_equipe
                FROM usuario u2
                JOIN turma t2 ON t2.fk_id_usuario = u2.id
                WHERE u2.nome = :idUsuario
            );"""
        )
        parametros = {'idUsuario': user.nome}
        execute = db.session.execute(consulta, parametros)
        result = execute.fetchall()
        usuario = result
    else:
        usuario = Usuario.query.all()
    return render_template("cadastro-avaliacao.html", usuarios=usuario, grupo=grupo)


@login_required
def tabela_avaliacao_turma():
    # turmas = Turma.query.all()
    # print(turmas)
    # lista = []
    # for turma in turmas:
    #     usuario = Usuario.query.filter_by(id=turma.fk_id_usuario).first()
    #     sala = Sala.query.filter_by(id=turma.fk_id_sala).first()
    #     disciplina = Disciplina.query.filter_by(
    #         id=turma.fk_id_disciplina).first()
    #     equipe = Equipe.query.filter_by(id=turma.fk_id_equipe).first()
    #     avaliacao = Avaliacao.query.filter_by(id=turma.fk_id_avaliacao).first()
    #     if usuario and sala and disciplina and equipe and avaliacao:
    #         lista.append({"tipo_avaliacao": avaliacao.tipo_avaliacao, "nome": usuario.nome, "sala": sala.numero, "disciplina": disciplina.titulo,
    #                      "equipe": equipe.apelido, "avaliacao": avaliacao.titulo, "id": avaliacao.id})
    consulta = text("select a.titulo, a.tipo_avaliacao, u.nome, s.numero, d.titulo, e.apelido, a.id from avaliacao a left join turma t on t.fk_id_usuario in (a.fk_id_usuario) left join usuario u on u.id in (a.fk_id_usuario) left join sala s on s.id in (t.fk_id_sala) left join disciplina d on d.id in (t.fk_id_disciplina) left join equipe e on e.id in (t.fk_id_equipe)")
    execute = db.session.execute(consulta)
    result = execute.fetchall()
    print(result)
    return render_template("tabela-avaliacao-turma.html", data=result)


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
def visualiza_usuarios():
    usuarios = Usuario.query.all()
    return render_template("usuario.html", usuarios=usuarios)


@login_required
def visualiza_boletim(item_nome):
    usuario = Usuario.query.filter_by(nome=item_nome).first()
    consulta = text("select av.titulo, av.descricao, av.tipo_avaliacao, JSON_GROUP_ARRAY(json_object('titulo', ha.titulo, 'nota', na.valor, 'fator_peso', ha.fator_peso)) AS notas from avaliacao av left join nota_avalia na on na.fk_id_avaliacao = av.id  left join habilidade_atitude ha on ha.id = na.fk_id_habilidade_atitude left join usuario us on us.id = av.fk_id_usuario left join grupo g on g.id = us.fk_id_grupo where av.fk_id_usuario = :idUsuario group by av.id")
    consulta2 = text("SELECT SUM(total_porcentagem_nota) AS total_porcentagem_nota FROM (SELECT tipo_avaliacao, SUM(porcentagem_nota) AS total_porcentagem_nota FROM (SELECT tipo_avaliacao, habilidade_titulo, nota_percentual, CASE WHEN tipo_avaliacao = 'aluno' THEN nota_percentual * 0.8 WHEN tipo_avaliacao = 'colega' THEN nota_percentual * 0.1 WHEN tipo_avaliacao = 'auto' THEN nota_percentual * 0.1 ELSE nota_percentual END AS porcentagem_nota FROM (SELECT CASE WHEN ha.titulo IN ('Unidades de Aprendizagem (Uas)', 'Entrega', 'Avaliação objetiva', 'Avaliação dissertativa') THEN 'conhecimento' ELSE av.tipo_avaliacao END AS tipo_avaliacao, ha.titulo AS habilidade_titulo, (SUM(summed_na.valor_total) / COUNT(DISTINCT av.id)) * ha.fator_peso AS nota_percentual, ha.fator_peso FROM avaliacao av LEFT JOIN (SELECT fk_id_avaliacao, fk_id_habilidade_atitude, SUM(valor) AS valor_total FROM nota_avalia GROUP BY fk_id_avaliacao, fk_id_habilidade_atitude) summed_na ON summed_na.fk_id_avaliacao = av.id LEFT JOIN habilidade_atitude ha ON ha.id = summed_na.fk_id_habilidade_atitude LEFT JOIN usuario us ON us.id = av.fk_id_usuario LEFT JOIN grupo g ON g.id = us.fk_id_grupo WHERE av.fk_id_usuario = :idUsuario GROUP BY tipo_avaliacao, ha.titulo) subquery) subquery_porcentagem GROUP BY tipo_avaliacao) subquery_total")
    parametros = {'idUsuario': usuario.id}
    execute = db.session.execute(consulta, parametros)
    execute2 = db.session.execute(consulta2, parametros)
    result = execute.fetchall()
    result2 = execute2.fetchall()
    print(result)
    print(result2)
    if not result:  # Verifica se result2 é uma lista vazia
        flash("Não há avaliações disponíveis para este usuário.", "error")
        return redirect(url_for("webui.visualiza_usuarios"))  # Redireciona para a página desejada
    else:
        print(result2)
        array = []
        
        # Cria um dicionário para armazenar as médias de cada avaliação
        medias = {}

        # Armazena a soma total das notas de todas as avaliações
        soma_total = 0
        media_final = 0

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
        
        soma_total = round(soma_total / len(result), 2)
        for avaliacao in result2:
            print(avaliacao[0])
            media_final = avaliacao[0]

        return render_template("boletim.html", data=array, media_total=media_final)

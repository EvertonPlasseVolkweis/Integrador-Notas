from functools import wraps
from flask import abort, redirect, render_template, request
from flask_jwt_extended import decode_token, get_jwt_identity, jwt_required, verify_jwt_in_request
from avaliacao.ext.main import MATRIZ_AVALIACAO, calcular_media, MATRIZ_AVALIACAO_TESTE
from avaliacao.models import Avaliacao, Grupo, HabilidadeAtitude, NotaAvalia, Perfil, Usuario, Turma, Sala, Disciplina, Equipe
from avaliacao.ext.database import db
from sqlalchemy import text
from flask import flash, redirect, url_for
from flask import jsonify
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


def admin_required(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            idUsuario = get_jwt_identity()
            user = Usuario.query.filter_by(id=idUsuario).first()
            perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()

            if perfil.perfil != "admin":
                return redirect("/")

        except Exception as e:
            return redirect("/")

        return view_function(*args, **kwargs)

    return decorated_function


def professor_required(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            idUsuario = get_jwt_identity()
            user = Usuario.query.filter_by(id=idUsuario).first()
            perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()

            if perfil.perfil != "professor" and perfil.perfil != "admin":
                return redirect("/")

        except Exception as e:
            return redirect("/")

        return view_function(*args, **kwargs)

    return decorated_function


def login():
    return render_template("login-teste.html")


@login_required
def home():
    verify_jwt_in_request()
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
    return render_template("index.html", perfil=perfil)


@login_required
@admin_required
def cadastro_usuario():
    verify_jwt_in_request()
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
    grupos = Grupo.query.all()
    perfis = Perfil.query.all()
    equipe = Equipe.query.all()
    sala = Sala.query.all()
    disciplina = Disciplina.query.all()
    return render_template("cadastro-usuario.html", grupos=grupos, perfis=perfis, equipe=equipe, sala=sala, disciplina=disciplina, perfil=perfil)


@login_required
def inserir_notas():
    verify_jwt_in_request()
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    grupo = Grupo.query.filter_by(id=user.fk_id_grupo).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
    avaliacao = Avaliacao.query.filter_by(tem_nota=False, fk_id_usuario=idUsuario).all()
    matriz = MATRIZ_AVALIACAO
    matriz = MATRIZ_AVALIACAO
    return render_template("inserir.html", matriz_avaliacao=matriz, grupo=grupo, avaliacao=avaliacao, perfil=perfil, editando=False)


@login_required
def cadastro_avaliacao():
    usuario = []
    verify_jwt_in_request()
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    grupo = Grupo.query.filter_by(id=user.fk_id_grupo).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
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
    return render_template("cadastro-avaliacao.html", usuarios=usuario, grupo=grupo, perfil=perfil)


@login_required
def tabela_avaliacao_turma(item_id):
    verify_jwt_in_request()
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    usuario = Usuario.query.filter_by(id=item_id).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
    consulta = text("""
    SELECT a.titulo, a.tipo_avaliacao, u.nome, s.numero, d.titulo, e.apelido, a.id
    FROM avaliacao a
    LEFT JOIN turma t ON t.fk_id_usuario IN (a.fk_id_usuario)
    LEFT JOIN usuario u ON u.id IN (a.fk_id_usuario)
    LEFT JOIN sala s ON s.id IN (t.fk_id_sala)
    LEFT JOIN disciplina d ON d.id IN (t.fk_id_disciplina)
    LEFT JOIN equipe e ON e.id IN (t.fk_id_equipe)
    WHERE u.id = :idUsuario""")
    parametros = {'idUsuario': item_id}
    execute = db.session.execute(consulta, parametros)
    result = execute.fetchall()
    if not result:  # Verifica se result2 é uma lista vazia
        flash("Não há avaliações disponíveis para este usuário.", "error")
        print('ife1')
        return jsonify({"error": True})
    else:
        if perfil.perfil != 'professor' and perfil.perfil != 'admin' and user.id != usuario.id:
            flash("Você não tem permissão para acessar este boletim.", "error")
            print('ife2')
            return redirect(url_for('webui.visualiza_usuarios'))
        else:
            print('eles')
            return render_template("tabela-avaliacao-turma.html", data=result, perfil=perfil)


@login_required
@professor_required
def visualiza_media():
    verify_jwt_in_request()
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
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
    soma_total = 0
    n_total = 0
    for notas in todas_notas:
        notas_total = sum(sum(categoria) for categoria in notas)
        peso_total = sum(categoria[2] for categoria in MATRIZ_AVALIACAO)
        media = notas_total / peso_total
        soma_total += media
        n_total += 1
    media_final = soma_total / n_total

    return render_template("inserido.html", media_final=media_final, perfil=perfil)


@login_required
@professor_required
def visualiza_avaliacao(item_id):
    verify_jwt_in_request()
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    grupo = Grupo.query.filter_by(id=user.fk_id_grupo).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
    matriz = MATRIZ_AVALIACAO
    avaliacao = Avaliacao.query.filter_by(id=item_id).first()
    notaAvalia = NotaAvalia.query.filter_by(fk_id_avaliacao=avaliacao.id).all()
    return render_template("inserir.html", matriz_avaliacao=matriz, grupo=grupo, notaAvalia=notaAvalia, visualizando=True, perfil=perfil)


@login_required
@professor_required
def edita_avaliacao(item_id):
    verify_jwt_in_request()
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    grupo = Grupo.query.filter_by(id=user.fk_id_grupo).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
    matriz = MATRIZ_AVALIACAO
    avaliacao = Avaliacao.query.filter_by(id=item_id).first()
    notaAvalia = NotaAvalia.query.filter_by(fk_id_avaliacao=avaliacao.id).all()
    return render_template("inserir.html", matriz_avaliacao=matriz, grupo=grupo, notaAvalia=notaAvalia, visualizando=False, editando=True, perfil=perfil, avaliacaoId=item_id)


@login_required
def visualiza_usuarios():
    verify_jwt_in_request()
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()

    if perfil.perfil == 'professor' or perfil.perfil == 'admin':
        usuarios = Usuario.query.all()
    else:
        usuarios = [user]

    return render_template("usuario.html", usuarios=usuarios, perfil=perfil)


@login_required
def visualiza_boletim(item_nome):
    verify_jwt_in_request()
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
    usuario = Usuario.query.filter_by(nome=item_nome).first()
    consulta = text("select av.titulo, av.descricao, av.tipo_avaliacao, JSON_GROUP_ARRAY(json_object('titulo', ha.titulo, 'nota', na.valor, 'fator_peso', ha.fator_peso)) AS notas from avaliacao av left join nota_avalia na on na.fk_id_avaliacao = av.id  left join habilidade_atitude ha on ha.id = na.fk_id_habilidade_atitude left join usuario us on us.id = av.fk_id_usuario left join grupo g on g.id = us.fk_id_grupo where av.fk_id_usuario = :idUsuario group by av.id")
    consulta2 = text("SELECT SUM(total_porcentagem_nota) AS total_porcentagem_nota FROM (SELECT tipo_avaliacao, SUM(porcentagem_nota) AS total_porcentagem_nota FROM (SELECT tipo_avaliacao, habilidade_titulo, nota_percentual, CASE WHEN tipo_avaliacao = 'aluno' THEN nota_percentual * 0.8 WHEN tipo_avaliacao = 'colega' THEN nota_percentual * 0.1 WHEN tipo_avaliacao = 'auto' THEN nota_percentual * 0.1 ELSE nota_percentual END AS porcentagem_nota FROM (SELECT CASE WHEN ha.titulo IN ('Unidades de Aprendizagem (Uas)', 'Entrega', 'Avaliação objetiva', 'Avaliação dissertativa') THEN 'conhecimento' ELSE av.tipo_avaliacao END AS tipo_avaliacao, ha.titulo AS habilidade_titulo, (SUM(summed_na.valor_total) / COUNT(DISTINCT av.id)) * ha.fator_peso AS nota_percentual, ha.fator_peso FROM avaliacao av LEFT JOIN (SELECT fk_id_avaliacao, fk_id_habilidade_atitude, SUM(valor) AS valor_total FROM nota_avalia GROUP BY fk_id_avaliacao, fk_id_habilidade_atitude) summed_na ON summed_na.fk_id_avaliacao = av.id LEFT JOIN habilidade_atitude ha ON ha.id = summed_na.fk_id_habilidade_atitude LEFT JOIN usuario us ON us.id = av.fk_id_usuario LEFT JOIN grupo g ON g.id = us.fk_id_grupo WHERE av.fk_id_usuario = :idUsuario GROUP BY tipo_avaliacao, ha.titulo) subquery) subquery_porcentagem GROUP BY tipo_avaliacao) subquery_total")
    parametros = {'idUsuario': usuario.id}
    execute = db.session.execute(consulta, parametros)
    execute2 = db.session.execute(consulta2, parametros)
    result = execute.fetchall()
    result2 = execute2.fetchall()
    if not result:  # Verifica se result2 é uma lista vazia
        flash("Não há avaliações disponíveis para este usuário.", "error")
        return jsonify({"error": True})
    else:
        if perfil.perfil != 'professor' and perfil.perfil != 'admin' and user.id != usuario.id:
            flash("Você não tem permissão para acessar este boletim.", "error")
            return redirect(url_for('webui.visualiza_usuarios'))
        else:
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
                media = sum([a['nota'] * a['fator_peso'] for a in aval_dict]
                            ) / sum([a['fator_peso'] for a in aval_dict])

                # Armazena a média no dicionário medias
                medias[avaliacao[0]] = media

                # Arredonda a média para duas casas decimais
                media_arredondada = round(media, 2)

                array.append({"titulo": avaliacao[0], "descricao": avaliacao[1],
                            "tipo": avaliacao[2], "media": media_arredondada})

            soma_total = round(soma_total / len(result), 2)
            for avaliacao in result2:
                media_final = avaliacao[0]

            return render_template("boletim.html", data=array, media_total=media_final, perfil=perfil)

from collections import Counter
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
    avaliacoes = Avaliacao.query.all()

    # Mapear os tipos de avaliação para novas descrições
    tipos_para_descricoes = {
        "aluno": "Avaliação de Aluno",
        "colega": "Avaliação de Equipe",
        "auto": "Auto Avaliação",
    }

    # Contar a quantidade de cada tipo de avaliacao
    tipos_avaliacao = [avaliacao.tipo_avaliacao for avaliacao in avaliacoes]
    contagem_avaliacoes = Counter(tipos_avaliacao)

    # Passar os dados para o template, usando as novas descrições
    labels = [tipos_para_descricoes[tipo] for tipo in contagem_avaliacoes.keys()]
    data = list(contagem_avaliacoes.values())
    print(labels)
    print(data)
    return render_template("index.html", perfil=perfil, user=user, labels=labels, data=data)



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
@admin_required
def cadastro_turma():
    verify_jwt_in_request()
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
    usuarios = Usuario.query.all()
    equipe = Equipe.query.all()
    sala = Sala.query.all()
    disciplina = Disciplina.query.all()
    return render_template("cadastro-turma.html", equipe=equipe, sala=sala, disciplina=disciplina, usuarios=usuarios, perfil=perfil)



@login_required
def inserir_notas():
    verify_jwt_in_request()
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    grupo = Grupo.query.filter_by(id=user.fk_id_grupo).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
    print(idUsuario)
    avaliacao = Avaliacao.query.filter_by(tem_nota=False, fk_id_usuario_avaliador=idUsuario).all()
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
    disciplinas = Disciplina.query.all()
    turmas = Turma.query.all()
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
    return render_template("cadastro-avaliacao.html", usuarios=usuario, grupo=grupo, perfil=perfil, disciplinas=disciplinas, turmas=turmas, idUsuario=idUsuario)


@login_required
def tabela_avaliacao_turma(item_id, id_turma):
    verify_jwt_in_request()
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    usuario = Usuario.query.filter_by(id=item_id).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
    consulta = text("""
    SELECT a.titulo, a.tipo_avaliacao, u.nome, a.id, a.tem_nota
    FROM avaliacao a
    LEFT JOIN usuario u ON u.id IN (a.fk_id_usuario)
    WHERE u.id = :idUsuario  AND a.fk_id_turma = :idTurma AND a.tem_nota = 1""")
    parametros = {'idUsuario': item_id, 'idTurma': id_turma}
    execute = db.session.execute(consulta, parametros)
    result = execute.fetchall()
    print(result)
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
def edita_disciplina(id):
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
    disciplina = Disciplina.query.filter_by(id=id).first()
    return render_template("form-disciplina.html", visualizando=False, editando=True, dados=disciplina, id=disciplina.id, perfil=perfil)

@login_required
def visualiza_disciplina(id):
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
    disciplina = Disciplina.query.filter_by(id=id).first()
    return render_template("form-disciplina.html", visualizando=True, editando=False, dados=disciplina, perfil=perfil)

@login_required
def edita_equipe(id):
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
    equipe = Equipe.query.filter_by(id=id).first()
    return render_template("form-equipe.html", visualizando=False, editando=True, dados=equipe, perfil=perfil)

@login_required
def visualiza_equipe(id):
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
    equipe = Equipe.query.filter_by(id=id).first()
    return render_template("form-equipe.html", visualizando=True, editando=False, dados=equipe, perfil=perfil)

@login_required
def edita_sala(id):
    sala = Sala.query.filter_by(id=id).first()
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
    return render_template("form-sala.html", visualizando=False, editando=True, dados=sala, perfil=perfil)

@login_required
def visualiza_sala(id):
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
    sala = Sala.query.filter_by(id=id).first()
    return render_template("form-sala.html", visualizando=True, editando=False, dados=sala, perfil=perfil)


@login_required
@admin_required
def edita_usuario(item_id):
    verify_jwt_in_request()
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    grupo = Grupo.query.filter_by(id=user.fk_id_grupo).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
    grupos = Grupo.query.all()
    perfis = Perfil.query.all()
    matriz = MATRIZ_AVALIACAO
    usuario = Usuario.query.filter_by(id=item_id).first()
    return render_template("cadastro-usuario.html", grupos=grupos, perfis=perfis, usuario=usuario, matriz_avaliacao=matriz, grupo=grupo, visualizando=False, editando=True, perfil=perfil, idUsuario=item_id)


@login_required
def visualiza_usuarios():
    verify_jwt_in_request()
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
    grupos = Grupo.query.all()
    if perfil.perfil == 'professor' or perfil.perfil == 'admin':
        usuarios = Usuario.query.all()
    else:
        usuarios = [user]

    return render_template("usuario.html", usuarios=usuarios, perfil=perfil, grupos=grupos)


@login_required
def visualiza_turmas(item_id):
    verify_jwt_in_request()
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
    consulta = text("""
    SELECT u.id, u.nome, s.numero, d.titulo, e.apelido, t.id as id_turma
    FROM turma t
    LEFT JOIN usuario u ON u.id IN (t.fk_id_usuario)
    LEFT JOIN sala s ON s.id IN (t.fk_id_sala)
    LEFT JOIN disciplina d ON d.id IN (t.fk_id_disciplina)
    LEFT JOIN equipe e ON e.id IN (t.fk_id_equipe)
    WHERE u.id = :idUsuario
    """)
    parametros = {'idUsuario': item_id}
    execute = db.session.execute(consulta, parametros)
    result = execute.fetchall()
    if not result:  # Verifica se result é uma lista vazia
        flash("Usuário não está matriculado em nenhuma disciplina.", "error")
        return jsonify({"error": True})
    else:
        return render_template("turmas.html", turmas=result, perfil=perfil)


@login_required
def visualiza_boletim(item_nome, id_turma):
    verify_jwt_in_request()
    print(id_turma)
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
    usuario = Usuario.query.filter_by(nome=item_nome).first()
    nomeUsuario = usuario.nome
    print(nomeUsuario)
    consulta = text("""
    SELECT av.titulo, av.descricao, av.tipo_avaliacao, 
    JSON_GROUP_ARRAY(json_object('titulo', ha.titulo, 'nota', na.valor, 'fator_peso', ha.fator_peso)) AS notas 
    FROM avaliacao av 
    LEFT JOIN nota_avalia na ON na.fk_id_avaliacao = av.id  
    LEFT JOIN habilidade_atitude ha ON ha.id = na.fk_id_habilidade_atitude 
    LEFT JOIN usuario us ON us.id = av.fk_id_usuario 
    LEFT JOIN grupo g ON g.id = us.fk_id_grupo 
    WHERE av.fk_id_usuario = :idUsuario AND av.tem_nota = 1
    GROUP BY av.id 
    """)
    consulta2 = text("SELECT SUM(total_porcentagem_nota) AS total_porcentagem_nota FROM (SELECT tipo_avaliacao, SUM(porcentagem_nota) AS total_porcentagem_nota FROM (SELECT tipo_avaliacao, habilidade_titulo, nota_percentual, CASE WHEN tipo_avaliacao = 'aluno' THEN nota_percentual * 0.8 WHEN tipo_avaliacao = 'colega' THEN nota_percentual * 0.1 WHEN tipo_avaliacao = 'auto' THEN nota_percentual * 0.1 ELSE nota_percentual END AS porcentagem_nota FROM (SELECT CASE WHEN ha.titulo IN ('Unidades de Aprendizagem (Uas)', 'Entrega', 'Avaliação objetiva', 'Avaliação dissertativa') THEN 'conhecimento' ELSE av.tipo_avaliacao END AS tipo_avaliacao, ha.titulo AS habilidade_titulo, (SUM(summed_na.valor_total) / COUNT(DISTINCT av.id)) * ha.fator_peso AS nota_percentual, ha.fator_peso FROM avaliacao av LEFT JOIN (SELECT fk_id_avaliacao, fk_id_habilidade_atitude, SUM(valor) AS valor_total FROM nota_avalia GROUP BY fk_id_avaliacao, fk_id_habilidade_atitude) summed_na ON summed_na.fk_id_avaliacao = av.id LEFT JOIN habilidade_atitude ha ON ha.id = summed_na.fk_id_habilidade_atitude LEFT JOIN usuario us ON us.id = av.fk_id_usuario LEFT JOIN grupo g ON g.id = us.fk_id_grupo WHERE av.fk_id_usuario = :idUsuario and av.fk_id_turma = :idTurma GROUP BY tipo_avaliacao, ha.titulo) subquery) subquery_porcentagem GROUP BY tipo_avaliacao) subquery_total")
    parametros = {'idUsuario': usuario.id}
    parametros2 = {'idUsuario': usuario.id, 'idTurma': id_turma}
    execute = db.session.execute(consulta, parametros)
    execute2 = db.session.execute(consulta2, parametros2)
    result = execute.fetchall()
    result2 = execute2.fetchall()
    if not result or result2 == [(None,)]:  # Verifica se result2 é uma lista vazia
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
                media = sum([a.get('nota', 0) * a.get('fator_peso', 0) for a in aval_dict if a.get('nota') is not None and a.get('fator_peso') is not None]) / sum([a.get('fator_peso', 0) for a in aval_dict if a.get('fator_peso') is not None])

                # Armazena a média no dicionário medias
                medias[avaliacao[0]] = media

                # Arredonda a média para duas casas decimais
                media_arredondada = round(media, 2)

                array.append({"titulo": avaliacao[0], "descricao": avaliacao[1],
                            "tipo": avaliacao[2], "media": media_arredondada})

            soma_total = round(soma_total / len(result), 2)
            for avaliacao in result2:
                media_final = avaliacao[0]

            return render_template("boletim.html", data=array, media_total=media_final, perfil=perfil, nomeUsuario=nomeUsuario)
        
@login_required
def disciplinaView():
    verify_jwt_in_request()
    disciplina = Disciplina.query.all()
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
    return render_template("tabela-disciplina.html", disciplina=disciplina, perfil=perfil)

@login_required
def formDisciplinaView():
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
    return render_template("form-disciplina.html", perfil=perfil)

@login_required
def equipeView():
    verify_jwt_in_request()
    equipe = Equipe.query.all()
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
    return render_template("tabela-equipe.html", equipe=equipe, perfil=perfil)

@login_required
def formEquipeView():
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
    return render_template("form-equipe.html", perfil=perfil)

@login_required
def salaView():
    verify_jwt_in_request()
    sala = Sala.query.all()
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
    return render_template("tabela-sala.html", sala=sala, perfil=perfil)

@login_required
def formSalaView():
    idUsuario = get_jwt_identity()
    user = Usuario.query.filter_by(id=idUsuario).first()
    perfil = Perfil.query.filter_by(id=user.fk_id_perfil).first()
    return render_template("form-sala.html", perfil=perfil)

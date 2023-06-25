from flask import url_for
import pytest
from faker import Faker

from avaliacao.ext.database import db
from avaliacao.models import Disciplina, Equipe, Perfil, Sala, Usuario

# Cria um gerador de dados falsos
fake = Faker(['pt_BR'])

def test_create_user(client):
    # Teste de criação de usuário
    response = client.post('/api/v1/cadastro-usuario', json={
        'cpf': fake.cpf(), # Gera um CPF aleatório
        'nome': fake.name(), # Gera um nome aleatório
        'email': fake.email(), # Gera um email aleatório
        'ra': fake.random_number(digits=6, fix_len=True), # Gera um RA aleatório
        'login': fake.user_name(), # Gera um nome de usuário aleatório
        'senha': fake.password(), # Gera uma senha aleatória
        'grupo': fake.random_element(elements=(1,2,3,4,5)), # Gera um grupo aleatório
        'perfil': fake.random_element(elements=(1,2,3,4,5)), # Gera um perfil aleatório
    })

    assert response.status_code == 200


def test_create_avaliacao(client):
    response = client.post('/api/v1/avaliacao/cadastro-teste', json={
        'titulo': ' '.join(fake.words(nb=5)),  # Gera um título aleatório
        'descricao': ' '.join(fake.words(nb=15)),  # Gera uma descrição aleatória
        'tipo_avaliacao': ' '.join(fake.words(nb=3)),  # Gera um tipo de avaliação aleatório
        'data_inicio': fake.date_between(start_date='-30d', end_date='today').isoformat(),  # Gera uma data de início aleatória
        'data_fim': fake.date_between(start_date='today', end_date='+30d').isoformat(),  # Gera uma data de término aleatória
        'tem_nota': fake.pybool(),  # Gera um valor booleano aleatório
        'fk_id_usuario': fake.random_number(digits=5),  # Gera um ID de usuário aleatório
        'fk_id_usuario_avaliador': fake.random_number(digits=5),  # Gera um ID de avaliador aleatório
        'fk_id_turma': fake.random_number(digits=5),  # Gera um ID de turma aleatório
    })

    assert response.status_code == 200

def test_create_equipe(client):
    response = client.post('/api/v1/equipe/', json={
        'apelido': fake.name(),
        'nome_projeto': fake.name()
    })

    assert response.status_code == 200

def test_create_sala(client):
    response = client.post('/api/v1/sala/', json={
        'numero': fake.random_number(digits=5),
        'turno': fake.words(nb=10)
        
    })

    assert response.status_code == 200

def test_create_disciplina(client):
    response = client.post('/api/v1/disciplina/', json={
        'titulo': fake.name(),
        'ementa': fake.name()
    })

    assert response.status_code == 200

def test_atualiza_equipe(client):
    data = {
        "apelido": "Novo Apelido",
        "nome_projeto": "Novo Nome do Projeto"
    }
    response = client.put('/api/v1/equipe/1', json=data)
    assert response.status_code == 200

def test_atualiza_disciplina(client):
    dado = {
        "titulo": "Novo Título",
        "ementa": "Nova ementa"
    }
    response = client.put('/api/v1/disciplina/1', json=dado)
    assert response.status_code == 200

def test_atualiza_sala(client):
    dados = {
        "numero": "123",
        "turno": "Novo Turno"
    }
    response = client.put('/api/v1/sala/1', json=dados)
    assert response.status_code == 200

def test_edit_usuario(client):
    dados = {
        'cpf': fake.cpf(), # Gera um CPF aleatório
        'nome': fake.name(), # Gera um nome aleatório
        'email': fake.email(), # Gera um email aleatório
        'ra': fake.random_number(digits=6, fix_len=True), # Gera um RA aleatório
        'login': fake.user_name(), # Gera um nome de usuário aleatório
        'senha': fake.password(), # Gera uma senha aleatória
        'grupo': fake.random_element(elements=(1,2,3,4,5)), # Gera um grupo aleatório
        'perfil': fake.random_element(elements=(1,2,3,4,5)), # Gera um perfil aleatório
    }
    response = client.put('/api/v1/usuario/editar/1', json=dados)
    assert response.status_code == 200

def test_edit_avaliacao(client):
    dados = {
        'titulo': ' '.join(fake.words(nb=5)),  # Gera um título aleatório
        'descricao': ' '.join(fake.words(nb=15)),  # Gera uma descrição aleatória
        'tipo_avaliacao': ' '.join(fake.words(nb=3)),  # Gera um tipo de avaliação aleatório
        'data_inicio': fake.date_between(start_date='-30d', end_date='today').isoformat(),  # Gera uma data de início aleatória
        'data_fim': fake.date_between(start_date='today', end_date='+30d').isoformat(),  # Gera uma data de término aleatória
        'tem_nota': fake.pybool(),  # Gera um valor booleano aleatório
        'fk_id_usuario': fake.random_number(digits=5),  # Gera um ID de usuário aleatório
        'fk_id_usuario_avaliador': fake.random_number(digits=5),  # Gera um ID de avaliador aleatório
        'fk_id_turma': fake.random_number(digits=5),  # Gera um ID de turma aleatório
    }
    response = client.put('/api/v1/nota-avalia/editar/1', json=dados)
    assert response.status_code == 200


# def test_visualiza_boletim(client, mocker):
#     # primeiro precisamos criar alguns objetos de teste para simular a situação real.
#     test_user = Usuario(
#         id=fake.random_number(digits=5),
#         cpf=fake.word(),
#         nome=fake.name(),
#         email=fake.email(),
#         ra=fake.random_number(digits=6, fix_len=True),
#         login=fake.user_name(),
#         senha=fake.password(),
#         grupo=fake.random_element(elements=(1,2,3,4,5)),
#         perfil=fake.random_element(elements=(1,2,3,4,5))
#     )  # adicione outros campos necessários para o objeto Usuario.
#     test_perfil = Perfil(id=1, perfil="admin")
#     db.session.add(test_user)
#     db.session.add(test_perfil)
#     db.session.commit()

#     # podemos então mockar as funções que interagem com recursos externos, como os serviços JWT
#     mocker.patch("your_flask_app.routes.verify_jwt_in_request")  # substitua por seu próprio módulo
#     mocker.patch("your_flask_app.routes.get_jwt_identity", return_value=test_user.id)

#     # vamos mockar a consulta ao banco de dados
#     mock_result = mocker.MagicMock()
#     mock_result.fetchall.return_value = []  # retorna vazio para forçar o erro
#     mocker.patch("flask_sqlalchemy._QueryProperty.__get__").return_value.execute.return_value = mock_result

#     response = client.get(url_for('visualiza_boletim', item_nome="test_user", id_turma=1))

#     # verificar se o flash message é o esperado
#     with client.session_transaction() as session:
#         flash_message = dict(session["_flashes"]).get("error")
#     assert flash_message == "Não há avaliações disponíveis para este usuário."

# @pytest.fixture
# def preparar_dados():
#     usuario = Usuario(
#         id=fake.random_number(digits=5),
#         cpf=fake.word(),
#         nome=fake.name(),
#         email=fake.email(),
#         ra=fake.random_number(digits=6, fix_len=True),
#         login=fake.user_name(),
#         senha=fake.password(),
#         grupo=fake.random_element(elements=(1,2,3,4,5)),
#         perfil=fake.random_element(elements=(1,2,3,4,5))
#     )
#     sala = Sala(id=fake.random_number(digits=5), numero=fake.word(), turno=fake.word())
#     disciplina = Disciplina(id=fake.random_number(digits=5), titulo=fake.word(), ementa=fake.word())
#     equipe = Equipe(id=fake.random_number(digits=5), apelido=fake.word(), nome_projeto=fake.word())
    
#     db.session.add(usuario)
#     db.session.add(sala)
#     db.session.add(disciplina)
#     db.session.add(equipe)
#     db.session.commit()
    
#     return {
#         'usuario': usuario.id,
#         'sala': sala.id,
#         'disciplina': disciplina.id,
#         'equipe': equipe.id
#     }

# def test_create_turma(client, preparar_dados):
#     response = client.post('/api/v1/cadastro-turma/', json=preparar_dados)

#     assert response.status_code == 200
#     json_data = response.get_json()
#     assert json_data['message'] == 'Turma salva'

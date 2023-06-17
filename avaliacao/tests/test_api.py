from faker import Faker

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

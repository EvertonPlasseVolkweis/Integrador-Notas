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

def test_create_user2(client):
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

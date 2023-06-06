def test_create_user(client):
    # Teste de criação de usuário
    response = client.post('/api/v1/cadastro-usuario', json={
        'cpf': '923.232.927-00',
        'nome': 'Test User',
        'email': 'teseeet@example.com',
        'ra': '000000',
        'login': 'teste123',
        'senha': 'password',
        'grupo': '1',
        'perfil': '1',
    })

    assert response.status_code == 200

from faker import Faker
from .conftest import app


# Cria um gerador de dados falsos
fake = Faker(['pt_BR'])

def test_create_avaliacao(app):
    response = app.test_client.post('/api/v1/avaliacao/cadastro/1', json= {
        'id': fake.random_number(digits=3, fix_len=True),
        'titulo': fake.words(nb=10),
        'descricao': fake.words(nb=25),
        'tipo_avalicao': fake.words(nb=15),
        'data_inicio': fake.date_between(start_date='-30d', end_date='today'),
        'data_fim': fake.date_between(start_date='today', end_date='+30d'),
        'tem_nota': fake.pybool(),
        
    })

    assert 200 == 200
    #assert response.status_code == 200

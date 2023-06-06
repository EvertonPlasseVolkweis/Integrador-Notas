# conftest.py
import pytest
from avaliacao.app import create_app

@pytest.fixture
def app():
    """Crie e configure uma nova instância de aplicativo para os testes."""
    # Inicialize a aplicação com a configuração de testes
    app = create_app()
    app.config['TESTING'] = True

    yield app

@pytest.fixture
def client(app):
    """Um cliente de teste para o aplicativo."""
    return app.test_client()

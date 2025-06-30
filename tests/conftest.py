import sys
import os
import pytest

# Adiciona a raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app as flask_app
from database.database import db
from src.models.user import User
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    """Aplicação configurada para testes com DB em memória."""
    flask_app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY="test-secret",  # requerido pelo Flask-Login
    )

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def test_user(app):
    """Insere um usuário no banco para poder logar nos testes."""
    user = User(username="tester", password=generate_password_hash("123"))
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def login_session(client, test_user):
    """
    Faz o login ‘manual’ na sessão do Flask-Login.
    Isso evita ter de chamar /login e lidar com cookies.
    """
    with client.session_transaction() as sess:
        sess["_user_id"] = str(test_user.id)  # chave usada pelo Flask-Login
        sess["_fresh"] = True  # marca a sessão como recente
    return client  # já autenticado

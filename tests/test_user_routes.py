import bcrypt

from src.models.user import User
from database.database import db


def test_login(login_session, app):
    with app.app_context():
        admin = User(username="admin", password="123", role="admin")
        hashed_password = bcrypt.hashpw(admin.password.encode(), bcrypt.gensalt())
        admin.password = hashed_password
        db.session.add(admin)
        db.session.commit()

        admin_id = admin.id

    with login_session.session_transaction() as sess:
        sess["_user_id"] = str(admin.id)
        sess["_fresh"] = True

    payload = {
        "username": "admin",
        "password": "123"
    }

    response = login_session.post(f"/login", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Autenticação realizada com sucesso"


def test_login_invalid(login_session, app):
    with app.app_context():
        admin = User(username="admin", password="123", role="admin")
        hashed_password = bcrypt.hashpw(admin.password.encode(), bcrypt.gensalt())
        admin.password = hashed_password
        db.session.add(admin)
        db.session.commit()

        admin_id = admin.id

    with login_session.session_transaction() as sess:
        sess["_user_id"] = str(admin.id)
        sess["_fresh"] = True

    payload = {
        "username": "admin",
        "password": "1234"
    }

    response = login_session.post(f"/login", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data["message"] == "Credenciais inválidas"


def test_logout(login_session, app):
    with app.app_context():
        admin = User(username="admin", password="123", role="admin")
        db.session.add(admin)
        db.session.commit()

        admin_id = admin.id

    with login_session.session_transaction() as sess:
        sess["_user_id"] = str(admin.id)
        sess["_fresh"] = True

    response = login_session.get(f"/logout")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Logout realizado com sucesso!"


def test_admin_create_user(login_session, app):
    with app.app_context():
        admin = User(username="admin", password="123", role="admin")
        db.session.add(admin)
        db.session.commit()

        admin_id = admin.id

    with login_session.session_transaction() as sess:
        sess["_user_id"] = str(admin.id)
        sess["_fresh"] = True

    user = {
        "username": "test",
        "password": "1234",
        "role": "user"
    }

    response = login_session.post(f"/user", json=user)
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Usuário cadastrado com sucesso"


def test_admin_create_user_fail(login_session, app):
    with app.app_context():
        admin = User(username="admin", password="123", role="admin")
        db.session.add(admin)
        db.session.commit()

        admin_id = admin.id

    with login_session.session_transaction() as sess:
        sess["_user_id"] = str(admin.id)
        sess["_fresh"] = True

    user = {
        "password": "1234",
        "role": "user"
    }

    response = login_session.post(f"/user", json=user)
    assert response.status_code == 400
    data = response.get_json()
    assert data["message"] == "Dados inválidos"


def test_read_user(login_session, app):
    with app.app_context():
        admin = User(username="admin", password="123", role="admin")
        db.session.add(admin)
        db.session.commit()

        admin_id = admin.id

    with login_session.session_transaction() as sess:
        sess["_user_id"] = str(admin.id)
        sess["_fresh"] = True

    response = login_session.get(f"/user/{admin_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["username"] == f"{admin.username}"


def test_read_user_not_found(login_session, app):
    with app.app_context():
        admin = User(username="admin", password="123", role="admin")
        db.session.add(admin)
        db.session.commit()

        admin_id = admin.id

    with login_session.session_transaction() as sess:
        sess["_user_id"] = str(admin.id)
        sess["_fresh"] = True

    response = login_session.get(f"/user/9999")
    assert response.status_code == 404
    data = response.get_json()
    assert data["message"] == "Usuário não encontrado"


def test_admin_cannot_delete_self(login_session, app):
    with app.app_context():
        admin = User(username="admin", password="123", role="admin")
        db.session.add(admin)
        db.session.commit()

        admin_id = admin.id

    with login_session.session_transaction() as sess:
        sess["_user_id"] = str(admin.id)
        sess["_fresh"] = True

    response = login_session.delete(f"/user/{admin_id}")
    assert response.status_code == 403
    data = response.get_json()
    assert data["message"] == "Deleção não permitida"


def test_user_cannot_delete(login_session, app):
    with app.app_context():
        user = User(username="user", password="123", role="user")
        db.session.add(user)
        db.session.commit()

        user_id = user.id

    with login_session.session_transaction() as sess:
        sess["_user_id"] = str(user.id)
        sess["_fresh"] = True

    response = login_session.delete(f"/user/{user_id}")
    assert response.status_code == 403
    data = response.get_json()
    assert data["message"] == "Operação não permitida"


def test_user_update(login_session, app):
    with app.app_context():
        admin = User(username="admin", password="123", role="admin")
        db.session.add(admin)
        db.session.commit()

        admin_id = admin.id

    with login_session.session_transaction() as sess:
        sess["_user_id"] = str(admin.id)
        sess["_fresh"] = True

    payload = {
        "password": "1234",
    }

    response = login_session.put(f"/user/{admin_id}", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == f"Usuário {admin_id} atualizado com sucesso."


def test_user_update_not_found(login_session, app):
    with app.app_context():
        admin = User(username="admin", password="123", role="admin")
        db.session.add(admin)
        db.session.commit()

        admin_id = admin.id

    with login_session.session_transaction() as sess:
        sess["_user_id"] = str(admin.id)
        sess["_fresh"] = True

    payload = {
        "password": "1234",
    }

    response = login_session.put(f"/user/9999", json=payload)
    assert response.status_code == 404
    data = response.get_json()
    assert data["message"] == f"Usuário não encontrado"


def test_user_cannot_update(login_session, app):
    with app.app_context():
        admin = User(username="admin", password="123", role="admin")
        user = User(username="user", password="123", role="user")
        db.session.add(user)
        db.session.add(admin)
        db.session.commit()

        user_id = user.id
        admin_id = admin.id

    with login_session.session_transaction() as sess:
        sess["_user_id"] = str(user.id)
        sess["_fresh"] = True

    payload = {
        "password": "1234",
    }

    response = login_session.put(f"/user/{admin_id}", json=payload)
    assert response.status_code == 403
    data = response.get_json()
    assert data["message"] == "Operação não permitida"


def test_admin_delete_user(login_session, app):
    with app.app_context():
        admin = User(username="admin", password="123", role="admin")
        user = User(username="user", password="123", role="user")
        db.session.add(user)
        db.session.add(admin)
        db.session.commit()

        user_id = user.id
        admin_id = admin.id

    with login_session.session_transaction() as sess:
        sess["_user_id"] = str(admin.id)
        sess["_fresh"] = True

    response = login_session.delete(f"/user/{user_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == f"Usuário {user_id} deletado com sucesso"


def test_admin_delete_user_not_found(login_session, app):
    with app.app_context():
        admin = User(username="admin", password="123", role="admin")
        db.session.add(admin)
        db.session.commit()

        admin_id = admin.id

    with login_session.session_transaction() as sess:
        sess["_user_id"] = str(admin.id)
        sess["_fresh"] = True

    response = login_session.delete(f"/user/99999")
    assert response.status_code == 404
    data = response.get_json()
    assert data["message"] == f"Usuário não encontrado"

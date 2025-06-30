from src.models.diary import Diary
from database.database import db


def test_create_meal_route(login_session, app):
    payload = {
        "name": "Almoço",
        "description": "Arroz integral e frango",
        "in_diet": True
    }

    response = login_session.post("/refeicoes", json=payload)

    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Refeição cadastrada com sucesso!"

    with app.app_context():
        saved = db.session.get(Diary, data["id"])
        assert saved is not None
        with login_session.session_transaction() as sess:
            user_id = int(sess["_user_id"])

        assert saved.user_id == user_id


def test_create_meal_route_fail(login_session, app):
    payload = {
        "description": "Arroz integral e frango",
        "in_diet": True
    }

    response = login_session.post("/refeicoes", json=payload)

    assert response.status_code == 400
    data = response.get_json()
    assert data["name"] == [
        "Missing data for required field."
    ]


def test_get_meals_route(login_session, app):
    with app.app_context():
        with login_session.session_transaction() as sess:
            user_id = int(sess["_user_id"])

        meal1 = Diary(name="Café da manhã", description="Ovos", in_diet=True, user_id=user_id)
        meal2 = Diary(name="Almoço", description="Arroz e frango", in_diet=False, user_id=user_id)
        db.session.add_all([meal1, meal2])
        db.session.commit()

    response = login_session.get("/refeicoes")

    assert response.status_code == 200
    data = response.get_json()

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Café da manhã"
    assert data[1]["name"] == "Almoço"


def test_get_meal_by_id_route(login_session, app):
    with app.app_context():
        with login_session.session_transaction() as sess:
            user_id = int(sess["_user_id"])

        meal = Diary(
            name="Lanche da tarde",
            description="Iogurte com frutas",
            in_diet=True,
            user_id=user_id
        )
        db.session.add(meal)
        db.session.commit()

        meal_id = meal.id

    response = login_session.get(f"/refeicoes/{meal_id}")

    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Lanche da tarde"
    assert data["description"] == "Iogurte com frutas"
    assert data["in_diet"] is True
    assert data["id"] == meal_id


def test_get_meal_by_id_route_fail(login_session, app):
    with app.app_context():
        with login_session.session_transaction() as sess:
            user_id = int(sess["_user_id"])

        meal = Diary(
            name="Lanche da tarde",
            description="Iogurte com frutas",
            in_diet=True,
            user_id=user_id
        )
        db.session.add(meal)
        db.session.commit()

    response = login_session.get(f"/refeicoes/9999")

    assert response.status_code == 404
    data = response.get_json()
    assert data["message"] == "Refeição não encontrada"


def test_update_meal_route(login_session, app):
    with app.app_context():
        with login_session.session_transaction() as sess:
            user_id = int(sess["_user_id"])

        meal = Diary(
            name="Lanche da tarde",
            description="Iogurte com frutas",
            in_diet=True,
            user_id=user_id
        )
        db.session.add(meal)
        db.session.commit()

        meal_id = meal.id

    updated_data = {
        "name": "Jantar",
        "description": "Sopa de legumes",
        "in_diet": True
    }

    response = login_session.put(f"/refeicoes/{meal_id}", json=updated_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Refeição atualizada com sucesso."


def test_update_meal_route_fail(login_session, app):
    with app.app_context():
        with login_session.session_transaction() as sess:
            user_id = int(sess["_user_id"])

        meal = Diary(
            name="Lanche da tarde",
            description="Iogurte com frutas",
            in_diet=True,
            user_id=user_id
        )
        db.session.add(meal)
        db.session.commit()

    updated_data = {
        "name": "Jantar",
        "description": "Sopa de legumes",
        "in_diet": True
    }

    response = login_session.put(f"/refeicoes/9999", json=updated_data)
    assert response.status_code == 404
    data = response.get_json()
    assert data["message"] == "Refeição não encontrada"


def test_delete_meal_route(login_session, app):
    with app.app_context():
        with login_session.session_transaction() as sess:
            user_id = int(sess["_user_id"])

        meal = Diary(
            name="Lanche da tarde",
            description="Iogurte com frutas",
            in_diet=True,
            user_id=user_id
        )
        db.session.add(meal)
        db.session.commit()

        meal_id = meal.id

    response = login_session.delete(f"/refeicoes/{meal_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Refeição deletada com sucesso."


def test_delete_meal_route_fail(login_session, app):
    with app.app_context():
        with login_session.session_transaction() as sess:
            user_id = int(sess["_user_id"])

        meal = Diary(
            name="Lanche da tarde",
            description="Iogurte com frutas",
            in_diet=True,
            user_id=user_id
        )
        db.session.add(meal)
        db.session.commit()


    response = login_session.delete(f"/refeicoes/9999")
    assert response.status_code == 404
    data = response.get_json()
    assert data["message"] == "Refeição não encontrada"
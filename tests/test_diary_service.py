from src.services.diary_service import DiaryService
from src.models.diary import Diary


def test_create_meal(app):
    data = {
        "name": "Café da manhã",
        "description": "Ovos e tapioca",
        "in_diet": True
    }
    user_id = 1

    with app.app_context():
        meal = DiaryService.create_meal(user_id=user_id, data=data)

        assert isinstance(meal, Diary)
        assert meal.name == "Café da manhã"
        assert meal.description == "Ovos e tapioca"
        assert meal.in_diet is True
        assert meal.user_id == 1

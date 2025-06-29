from datetime import datetime

from src.models.diary import Diary
from database.database import db


class DiaryService:
    @staticmethod
    def create_meal(user_id, data):
        meal = Diary(
            name=data.get("name", None),
            description=data.get("description", None),
            date=datetime.now(),
            in_diet=data.get("in_diet", None),
            user_id=user_id,
        )
        db.session.add(meal)
        db.session.commit()
        return meal

    @staticmethod
    def list_meals(user_id):
        return Diary.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_meal(user_id, meal_id):
        return Diary.query.filter_by(id=meal_id, user_id=user_id).first()

    @staticmethod
    def update_meal(user_id, meal_id, data):
        meal = Diary.query.filter_by(id=meal_id, user_id=user_id).first()
        if not meal:
            return None

        meal.name = data["name"]
        meal.description = data["description"]
        meal.date = datetime.now()
        meal.in_diet = data["in_diet"]
        db.session.commit()

        return meal

    @staticmethod
    def delete_meal(user_id, meal_id):
        meal = Diary.query.filter_by(id=meal_id, user_id=user_id).first()
        if not meal:
            return False

        db.session.delete(meal)
        db.session.commit()
        return True

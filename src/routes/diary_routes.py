from flask import jsonify, request, Blueprint
from flask_login import current_user, login_required

from src.schemas.diary_schema import DiarySchema
from src.services.diary_service import DiaryService
from src.logger import logger

diary_bp = Blueprint("diary", __name__)
diary_schema = DiarySchema()
diaries_schema = DiarySchema(many=True)


@diary_bp.route("/refeicoes", methods=["POST"])
@login_required
def create_meal():
    data = request.get_json()

    errors = diary_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    meal = DiaryService.create_meal(current_user.id, data)
    logger.info(f"Refeição cadastrada com sucesso! - {meal.name}")
    return jsonify({"message": "Refeição cadastrada com sucesso!", "id": meal.id}), 201


@diary_bp.route("/refeicoes", methods=["GET"])
@login_required
def get_meals():
    meals = DiaryService.list_meals(current_user.id)
    return jsonify([meal.to_dict() for meal in meals])


@diary_bp.route("/refeicoes/<int:meal_id>", methods=["GET"])
@login_required
def get_meal(meal_id):
    meal = DiaryService.get_meal(current_user.id, meal_id)
    if not meal:
        return jsonify({"message": "Refeição não encontrada"}), 404
    return jsonify(meal.to_dict())


@diary_bp.route("/refeicoes/<int:meal_id>", methods=["PUT"])
@login_required
def update_meal(meal_id):
    data = request.get_json()
    meal = DiaryService.update_meal(current_user.id, meal_id, data)
    if not meal:
        return jsonify({"message": "Refeição não encontrada"}), 404
    return jsonify({"message": "Refeição atualizada com sucesso."}), 200


@diary_bp.route("/refeicoes/<int:meal_id>", methods=["DELETE"])
@login_required
def delete_meal(meal_id):
    sucess = DiaryService.delete_meal(current_user.id, meal_id)
    if not sucess:
        return jsonify({"message": "Refeição não encontrada"}), 404
    return jsonify({"message": "Refeição deletada com sucesso."}), 200

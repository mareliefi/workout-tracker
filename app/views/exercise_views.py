from app.models import Exercise, db
from app.utils.authorisation import token_required
from flask import jsonify

from . import api_bp


@api_bp.route("/exercises", methods=["GET"])
@token_required
def list_exercises(current_user):
    exercises = db.session.query(Exercise).all()
    if not exercises:
        return jsonify({"message": "No exercises found"}), 404

    return jsonify(
        [{"id": e.id, "name": e.name, "category": e.category} for e in exercises]
    ), 200


@api_bp.route("/exercises/<int:exercise_id>", methods=["GET"])
@token_required
def get_exercise(current_user, exercise_id):
    exercise = (
        db.session.query(Exercise).filter(Exercise.id == exercise_id).one_or_none()
    )
    if not exercise:
        return jsonify({"message": "Exercise not found"}), 404

    return jsonify(
        {
            "id": exercise.id,
            "name": exercise.name,
            "description": exercise.description,
            "category": exercise.category,
            "muscle_group": exercise.muscle_group,
        }
    ), 200

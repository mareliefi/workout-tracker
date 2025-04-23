from flask import jsonify
from utils.authorisation import token_required
from models import db, WorkoutPlan
from . import api_bp


@api_bp.route("/workout-plans", methods=["GET"])
@token_required
def list_workouts(current_user):
    workout_plans = (
        db.session.query(WorkoutPlan)
        .filter(WorkoutPlan.user_id == current_user.id)
        .order_by(WorkoutPlan.created_at.desc())
        .all()
    )
    if not workout_plans:
        return jsonify({"message": "No workout plans found for the user."}), 404

    return jsonify(
        [
            {"id": wp.id, "name": wp.name, "created_at": wp.created_at}
            for wp in workout_plans
        ]
    ), 200


@api_bp.route("/workout-plans/<int:workout_plan_id>", methods=["GET"])
@token_required
def get_workout(current_user, workout_plan_id):
    workout_plan = (
        db.session.query(WorkoutPlan)
        .filter(
            WorkoutPlan.user_id == current_user.id, WorkoutPlan.id == workout_plan_id
        )
        .order_by(WorkoutPlan.created_at.desc())
        .one_or_none()
    )
    if not workout_plan:
        return jsonify(
            {"message": f"No workout plan with id {workout_plan_id} for this user."}
        ), 404

    return jsonify(
        [
            {
                "workout": {
                    "workout_plan_id": workout_plan.id,
                    "name": workout_plan.name,
                    "created_at": workout_plan.created_at,
                    "updated_at": workout_plan.updated_at,
                    "exercises": [
                        {
                            "id": wp_ex.exercise_id,
                            "name": wp_ex.exercise.name,
                            "target_sets": wp_ex.target_sets,
                            "target_reps": wp_ex.target_reps,
                            "target_weight": wp_ex.target_weight,
                        }
                        for wp_ex in workout_plan.workout_plan_exercises
                    ],
                }
            }
        ]
    ), 200

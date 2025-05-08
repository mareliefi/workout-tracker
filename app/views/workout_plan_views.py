from app.models import Exercise, WorkoutPlan, WorkoutPlanExercise, db
from app.utils.authorisation import token_required
from app.utils.validation_functions import validate_field
from flask import jsonify, request

from . import api_bp


@api_bp.route("/workout-plans", methods=["GET"])
@token_required
def list_workouts(current_user):
    workout_plans = WorkoutPlan.get_user_workout_plan(user_id=current_user.id)
    if not workout_plans:
        return jsonify({"message": "No workout plans found for the user."}), 200

    return jsonify(
        [
            {"id": wp.id, "name": wp.name, "created_at": wp.created_at}
            for wp in workout_plans
        ]
    ), 200


@api_bp.route("/workout-plans/<int:workout_plan_id>", methods=["GET"])
@token_required
def get_workout(current_user, workout_plan_id):
    workout_plan = WorkoutPlan.get_user_workout_plan(
        user_id=current_user.id, workout_plan_id=workout_plan_id
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


@api_bp.route("/workout-plans/<int:workout_plan_id>", methods=["DELETE"])
@token_required
def delete_workout(current_user, workout_plan_id):
    workout_plan = WorkoutPlan.get_user_workout_plan(
        user_id=current_user.id, workout_plan_id=workout_plan_id
    )
    if workout_plan:
        db.session.delete(workout_plan)
        db.session.commit()
        return jsonify(
            {"message": f"Workout plan with id {workout_plan_id} succesfully deleted."}
        ), 200
    else:
        return jsonify(
            {"message": f"No workout plan with id {workout_plan_id} for this user."}
        ), 404


@api_bp.route("/workout-plans/<int:workout_plan_id>", methods=["PATCH"])
@token_required
def update_workout_plan(current_user, workout_plan_id):
    data = request.get_json()
    errors = {}

    workout_plan = WorkoutPlan.get_user_workout_plan(
        user_id=current_user.id, workout_plan_id=workout_plan_id
    )

    if not workout_plan:
        return jsonify(
            {"message": f"No workout plan with id {workout_plan_id} for this user."}
        ), 404

    # Update name if provided
    if "name" in data:
        workout_plan.name = data["name"]

    # Update exercises if provided
    if "exercises" in data:
        existing_exercises = {
            wp_ex.exercise_id: wp_ex for wp_ex in workout_plan.workout_plan_exercises
        }

        for exercise_data in data.get("exercises", []):
            for field, type in [
                ("exercise_id", "int"),
                ("target_sets", "int"),
                ("target_reps", "int"),
                ("target_weight", "float"),
            ]:
                error = validate_field(data, field, type)
                if error:
                    errors[field] = error
            if errors:
                return {"status": "error", "errors": errors}, 400

            exercise_id = data.get("exercise_id")
            exercise = Exercise.get_by_id(exercise_id)
            if exercise is None:
                return jsonify(
                    {"message": f"Exercise with id {exercise_id} does not exist."}
                ), 400

            if exercise_id in existing_exercises:
                # Exercise already exists → update it
                wp_ex = existing_exercises[exercise_id]
                wp_ex.target_sets = exercise_data.get("target_sets", wp_ex.target_sets)
                wp_ex.target_reps = exercise_data.get("target_reps", wp_ex.target_reps)
                wp_ex.target_weight = exercise_data.get(
                    "target_weight", wp_ex.target_weight
                )
            else:
                # Exercise does not exist → create new one
                new_wp_ex = WorkoutPlanExercise(
                    exercise_id=exercise_id,
                    target_sets=exercise_data.get("target_sets", 1),
                    target_reps=exercise_data.get("target_reps", 1),
                    target_weight=exercise_data.get("target_weight", 1.0),
                )
                workout_plan.workout_plan_exercises.append(new_wp_ex)
    try:
        db.session.commit()
    except Exception:
        return jsonify({"message": "An error occurred while saving the data."}), 500

    return jsonify({"message": "Workout plan updated successfully"}), 200


@api_bp.route("/workout-plans", methods=["POST"])
@token_required
def create_workout_plan(current_user):
    data = request.get_json()
    errors = {}

    # Name must be provided
    if "name" in data:
        workout_plan = WorkoutPlan(user_id=current_user.id, name=data["name"])
        db.session.add(workout_plan)
    else:
        return jsonify({"message": "Workout plan name must be provided."}), 400

    # Add exercises, if provided
    if "exercises" in data:
        for exercise_data in data.get("exercises", []):
            for field, type in [
                ("exercise_id", "int"),
                ("target_sets", "int"),
                ("target_reps", "int"),
                ("target_weight", "float"),
            ]:
                error = validate_field(data, field, type)
                if error:
                    errors[field] = error
            if errors:
                return {"status": "error", "errors": errors}, 400

            exercise_id = data.get("exercise_id")
            exercise = Exercise.get_by_id(exercise_id)
            if exercise is None:
                return jsonify(
                    {"message": f"Exercise with id {exercise_id} does not exist."}
                ), 400

            new_wp_ex = WorkoutPlanExercise(
                exercise_id=exercise_id,
                target_sets=exercise_data.get("target_sets", 1),
                target_reps=exercise_data.get("target_reps", 1),
                target_weight=exercise_data.get("target_weight", 1.0),
            )
            workout_plan.workout_plan_exercises.append(new_wp_ex)

    try:
        db.session.commit()
    except Exception:
        return jsonify({"message": "An error occurred while saving the data."}), 500

    return jsonify(
        {"message": f"Workout plan added successfully with id {workout_plan.id}"}
    ), 200

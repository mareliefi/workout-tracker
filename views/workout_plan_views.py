from flask import jsonify, request
from utils.authorisation import token_required
from models import db, Exercise, WorkoutPlan, WorkoutPlanExercise
from . import api_bp


@api_bp.route("/workout-plans", methods=["GET"])
@token_required
def list_workouts(current_user):
    workout_plans = WorkoutPlan.get_user_workout_plan(user_id=current_user.id)
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
            {"message": f"Workoutplan with id {workout_plan_id} succesfully deleted."}
        ), 200
    else:
        return jsonify(
            {"message": f"No workout plan with id {workout_plan_id} for this user."}
        ), 404


@api_bp.route("/workout-plans/<int:workout_plan_id>", methods=["PATCH"])
@token_required
def update_workout_plan(current_user, workout_plan_id):
    data = request.get_json()

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
            try:
                exercise_id = int(exercise_data.get("exercise_id"))
            except (ValueError, TypeError):
                return jsonify(
                    {
                        "message": f"""Invalid exercise_id: {exercise_data.get("exercise_id")}.
                        Must be an integer."""
                    }
                ), 400

            exercise = Exercise.get_by_id(exercise_id)
            if exercise is None:
                return jsonify(
                    {"message": f"Exercise with id {exercise_id} does not exist."}
                ), 400

            try:
                target_sets = exercise_data.get("target_sets")
                target_reps = exercise_data.get("target_reps")
                target_weight = exercise_data.get("target_weight")

                if target_sets is not None:
                    target_sets = int(target_sets)
                if target_reps is not None:
                    target_reps = int(target_reps)
                if target_weight is not None:
                    target_weight = float(target_weight)

            except (ValueError, TypeError):
                return jsonify(
                    {
                        "message": """All target sets and reps must be integers and weights
                        must be floats."""
                    }
                ), 400

            if exercise_id in existing_exercises:
                # Exercise already exists → update it
                wp_ex = existing_exercises[exercise_id]
                try:
                    wp_ex.target_sets = exercise_data.get(
                        "target_sets", wp_ex.target_sets
                    )
                    wp_ex.target_reps = exercise_data.get(
                        "target_reps", wp_ex.target_reps
                    )
                    wp_ex.target_weight = exercise_data.get(
                        "target_weight", wp_ex.target_weight
                    )
                except Exception:
                    return jsonify(
                        {
                            "message": """All target sets and reps must be integers and weights
                            must be floats."""
                        }
                    ), 400
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

    # Name must be provided
    if "name" in data:
        workout_plan = WorkoutPlan(user_id=current_user.id, name=data["name"])
        db.session.add(workout_plan)
    else:
        return jsonify({"message": "Workout plan name must be provided."}), 400

    # Add exercises, if provided
    if "exercises" in data:
        for exercise_data in data.get("exercises", []):
            # Exercise id must be an integer
            try:
                exercise_id = int(exercise_data.get("exercise_id"))
            except (ValueError, TypeError):
                return jsonify(
                    {
                        "message": f"""Invalid exercise_id: {exercise_data.get("exercise_id")}.
                        Must be an integer."""
                    }
                ), 400

            # Exercise id must exist in Exercise table
            exercise = Exercise.get_by_id(exercise_id)
            if exercise is None:
                return jsonify(
                    {"message": f"Exercise with id {exercise_id} does not exist."}
                ), 400

            # Sets and reps must be int and weight must be float
            try:
                target_sets = exercise_data.get("target_sets")
                target_reps = exercise_data.get("target_reps")
                target_weight = exercise_data.get("target_weight")

                if target_sets is not None:
                    target_sets = int(target_sets)
                if target_reps is not None:
                    target_reps = int(target_reps)
                if target_weight is not None:
                    target_weight = float(target_weight)

            except (ValueError, TypeError):
                return jsonify(
                    {
                        "message": """All target sets and reps must be integers and weights
                        must be floats."""
                    }
                ), 400

            new_wp_ex = WorkoutPlanExercise(
                exercise_id=exercise_id,
                target_sets=target_sets if target_sets is not None else 1,
                target_reps=target_reps if target_reps is not None else 1,
                target_weight=target_weight if target_weight is not None else 1.0,
            )
            workout_plan.workout_plan_exercises.append(new_wp_ex)

    try:
        db.session.commit()
    except Exception:
        return jsonify({"message": "An error occurred while saving the data."}), 500

    return jsonify(
        {"message": f"Workout plan added successfully with id {workout_plan.id}"}
    ), 200

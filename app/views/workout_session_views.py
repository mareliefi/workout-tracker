from app.models import (
    SessionExercise,
    WorkoutPlan,
    WorkoutPlanExercise,
    WorkoutSession,
    db,
)
from app.utils.authorisation import token_required
from app.utils.validation_functions import validate_field
from flask import jsonify, request

from . import api_bp


@api_bp.route(
    "/workout-sessions",
    methods=["GET"],
)
@token_required
def list_workout_sessions(current_user):
    workout_plans = WorkoutPlan.get_user_workout_plan(user_id=current_user.id)
    if not workout_plans:
        return jsonify({"message": "No workout plans found for the user."}), 200
    elif not workout_plans.workout_sessions:
        return jsonify({"message": "No workout sessions found for the user."}), 200

    return jsonify(
        [
            {
                "id": ws.id,
                "workout_plan_id": ws.workout_plan_id,
                "scheduled_at": ws.scheduled_at,
            }
            for ws in workout_plans.workout_sessions
        ]
    ), 200


@api_bp.route(
    "/workout-sessions/<int:workout_plan_id>/<int:workout_session_id>", methods=["GET"]
)
@token_required
def get_workout_session(current_user, workout_plan_id, workout_session_id):
    workout_session = WorkoutSession.get_session_for_user_plan(
        current_user.id, workout_plan_id, workout_session_id
    )
    if not workout_session:
        return jsonify(
            {
                "message": f"No workout session with id {workout_session_id} for this user."
            }
        ), 404

    return jsonify(
        [
            {
                "workout_session": {
                    "workout_session_id": workout_session.id,
                    "workout_plan_id": workout_session.workout_plan_id,
                    "scheduled_at": workout_session.scheduled_at,
                    "started_at": workout_session.started_at,
                    "completed_at": workout_session.completed_at,
                    "session_exercises": [
                        {
                            "id": ws_ex.workout_plan_exercise_id,
                            "actual_sets": ws_ex.actual_sets,
                            "actual_reps": ws_ex.actual_reps,
                            "actual_weight": ws_ex.actual_weight,
                            "notes": ws_ex.notes,
                        }
                        for ws_ex in workout_session.session_exercises
                    ],
                }
            }
        ]
    ), 200


@api_bp.route(
    "/workout-sessions/<int:workout_plan_id>/<int:workout_session_id>",
    methods=["DELETE"],
)
@token_required
def delete_workout_session(current_user, workout_plan_id, workout_session_id):
    workout_session = WorkoutSession.get_session_for_user_plan(
        user_id=current_user.id,
        workout_plan_id=workout_plan_id,
        session_id=workout_session_id,
    )
    if workout_session:
        db.session.delete(workout_session)
        db.session.commit()
        return jsonify(
            {
                "message": f"Workout session with id {workout_session_id} succesfully deleted."
            }
        ), 200
    else:
        return jsonify(
            {
                "message": f"No workout session with id {workout_session_id} for this user."
            }
        ), 404


@api_bp.route(
    "/workout-sessions/<int:workout_plan_id>/<int:workout_session_id>",
    methods=["PATCH"],
)
@token_required
def update_workout_session(current_user, workout_plan_id, workout_session_id):
    data = request.get_json()
    errors = {}

    workout_session = WorkoutSession.get_session_for_user_plan(
        user_id=current_user.id,
        workout_plan_id=workout_plan_id,
        session_id=workout_session_id,
    )

    if not workout_session:
        return jsonify(
            {
                "message": f"No workout session with id {workout_session_id} for this user."
            }
        ), 404

    for field, type in [
        ("scheduled_at", "datetime"),
        ("started_at", "datetime"),
        ("completed_at", "datetime"),
    ]:
        error = validate_field(data, field, type)
        if error:
            errors[field] = error
    if errors:
        return {"status": "error", "errors": errors}, 400

    workout_session.scheduled_at = data.get(
        "scheduled_at", workout_session.scheduled_at
    )
    workout_session.started_at = data.get("started_at", workout_session.started_at)
    workout_session.completed_at = data.get("completed_at", workout_session.started_at)

    # Update exercises if provided
    if "exercises" in data:
        existing_session_exercises = {
            ws_ex.id: ws_ex for ws_ex in workout_session.session_exercises
        }

        for exercise_data in data.get("exercises", []):
            for field, type in [
                ("workout_plan_exercise_id", "int"),
                ("actual_sets", "int"),
                ("actual_reps", "int"),
                ("actual_weight", "float"),
            ]:
                error = validate_field(data, field, type)
                if error:
                    errors[field] = error
            if errors:
                return {"status": "error", "errors": errors}, 400

            workout_plan_exercise_id = exercise_data.get("workout_plan_exercise_id")
            exercise = WorkoutPlanExercise.get_by_workout_id_exercise_id(
                id=workout_plan_exercise_id, workout_plan_id=workout_plan_id
            )
            if exercise is None:
                return jsonify(
                    {
                        "message": f"""Exercise with id {workout_plan_exercise_id} does not exist
                        in workout plan. Add exercise to workout plan first."""
                    }
                ), 400

            if exercise in existing_session_exercises:
                # Exercise already exists → update it
                ws_ex = existing_session_exercises[exercise]
                ws_ex.actual_sets = exercise_data.get("actual_sets", ws_ex.actual_sets)
                ws_ex.actual_reps = exercise_data.get("actual_reps", ws_ex.actual_reps)
                ws_ex.actual_weight = exercise_data.get(
                    "actual_weight", ws_ex.actual_weight
                )
                ws_ex.notes = ws_ex.get("notes", ws_ex.notes)
            else:
                # Exercise does not exist → create new one
                new_ws_ex = SessionExercise(
                    workout_session_id=workout_session.id,
                    workout_plan_exercise_id=workout_plan_exercise_id,
                    actual_sets=exercise_data.get("actual_sets", 1),
                    actual_reps=exercise_data.get("actual_reps", 1),
                    actual_weight=exercise_data.get("actual_weight", 1.0),
                    notes=exercise_data.get("notes", ""),
                )
            try:
                new_ws_ex.save()
                workout_session.session_exercises.append(new_ws_ex)
            except Exception as e:
                return jsonify(
                    {
                        "message": f"An error occurred while processing the exercise: {str(e)}"
                    }
                ), 400
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {"message": f"An error occurred while saving the data: {str(e)}"}
        ), 500

    return jsonify({"message": "Workout session updated successfully"}), 200


@api_bp.route("/workout-sessions/<int:workout_plan_id>", methods=["POST"])
@token_required
def create_workout_session(current_user, workout_plan_id):
    data = request.get_json()
    errors = {}

    workout_plan = WorkoutPlan.get_user_workout_plan(
        user_id=current_user.id, workout_plan_id=workout_plan_id
    )

    if not workout_plan:
        return jsonify(
            {
                "message": f"""No workout plan with id {workout_plan_id} for this user -
                workout session cannot be created."""
            }
        ), 404

    for field, type in [
        ("scheduled_at", "datetime"),
        ("started_at", "datetime"),
        ("completed_at", "datetime"),
    ]:
        error = validate_field(data, field, type)
        if error:
            errors[field] = error
    if errors:
        return {"status": "error", "errors": errors}, 400

    workout_session = WorkoutSession(
        workout_plan_id=workout_plan.id,
        scheduled_at=data.get("scheduled_at"),
        started_at=data.get("started_at"),
        completed_at=data.get("completed_at"),
    )
    workout_plan.workout_sessions.append(workout_session)

    # Add exercises if provided
    if "exercises" in data:
        for exercise_data in data.get("exercises", []):
            for field, type in [
                ("workout_plan_exercise_id", "int"),
                ("actual_sets", "int"),
                ("actual_reps", "int"),
                ("actual_weight", "float"),
            ]:
                error = validate_field(data, field, type)
                if error:
                    errors[field] = error
            if errors:
                return {"status": "error", "errors": errors}, 400

            workout_plan_exercise_id = exercise_data.get("workout_plan_exercise_id")
            exercise = WorkoutPlanExercise.get_by_workout_id_exercise_id(
                id=workout_plan_exercise_id, workout_plan_id=workout_plan_id
            )
            if exercise is None:
                return jsonify(
                    {
                        "message": f"""Exercise with id {workout_plan_exercise_id} does not exist
                        in workout plan. Add exercise to workout plan first."""
                    }
                ), 400

            new_ws_ex = SessionExercise(
                workout_session_id=workout_session.id,
                workout_plan_exercise_id=workout_plan_exercise_id,
                actual_sets=exercise_data.get("actual_sets", 1),
                actual_reps=exercise_data.get("actual_reps", 1),
                actual_weight=exercise_data.get("actual_weight", 1.0),
                notes=exercise_data.get("notes", ""),
            )
            try:
                new_ws_ex.save()
                workout_session.session_exercises.append(new_ws_ex)
            except Exception as e:
                return jsonify(
                    {
                        "message": f"An error occurred while processing the exercise: {str(e)}"
                    }
                ), 400
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {"message": f"An error occurred while saving the data: {str(e)}"}
        ), 500

    return jsonify({"message": "Workout session updated successfully"}), 200

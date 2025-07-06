from flask import jsonify
from sqlalchemy.orm import joinedload

from ..models import (
    SessionExercise,
    WorkoutPlan,
    WorkoutPlanExercise,
    WorkoutSession,
    db,
)
from ..utils.authorisation import token_required
from . import api_bp


@api_bp.route("/reports/workout-plan/<int:workout_plan_id>", methods=["GET"])
@token_required
def get_workout_report(current_user, workout_plan_id):
    workout_plan = (
        db.session.query(WorkoutPlan)
        .options(
            joinedload(WorkoutPlan.workout_plan_exercises).joinedload(
                WorkoutPlanExercise.exercise
            ),
            joinedload(WorkoutPlan.workout_sessions)
            .joinedload(WorkoutSession.session_exercises)
            .joinedload(SessionExercise.workout_plan_exercise)
            .joinedload(WorkoutPlanExercise.exercise),
        )
        .filter(
            WorkoutPlan.id == workout_plan_id, WorkoutPlan.user_id == current_user.id
        )
        .one_or_none()
    )

    if not workout_plan:
        return jsonify({"message": "Workout plan not found"}), 404

    return {
        "id": workout_plan.id,
        "name": workout_plan.name,
        "exercises": [
            {
                "id": wp_ex.exercise_id,
                "name": wp_ex.exercise.name if wp_ex.exercise else None,
                "target_sets": wp_ex.target_sets,
                "target_reps": wp_ex.target_reps,
                "target_weight": wp_ex.target_weight,
            }
            for wp_ex in workout_plan.workout_plan_exercises
        ],
        "sessions": [
            {
                "id": session.id,
                "scheduled_at": session.scheduled_at.isoformat()
                if session.scheduled_at
                else None,
                "started_at": session.started_at.isoformat()
                if session.started_at
                else None,
                "completed_at": session.completed_at.isoformat()
                if session.completed_at
                else None,
                "exercises": [
                    {
                        "id": ws_ex.id,
                        "workout_plan_exercise_id": ws_ex.workout_plan_exercise_id,
                        "exercise_name": ws_ex.workout_plan_exercise.exercise.name
                        if ws_ex.workout_plan_exercise
                        and ws_ex.workout_plan_exercise.exercise
                        else None,
                        "actual_sets": ws_ex.actual_sets,
                        "actual_reps": ws_ex.actual_reps,
                        "actual_weight": ws_ex.actual_weight,
                        "notes": ws_ex.notes,
                    }
                    for ws_ex in session.session_exercises
                ]
                if session.session_exercises
                else [],
            }
            for session in workout_plan.workout_sessions
        ],
    }

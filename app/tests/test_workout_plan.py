import json

from ..models import WorkoutPlan
from .test_utils import create_jwt_token


def auth_headers(token):
    return {"HTTP_COOKIE": f"jwt_token={token}"}


def test_list_workouts(client, seed_data, app):
    user = seed_data["plan_user"]
    token = create_jwt_token(user.id, app)

    client.set_cookie(key="jwt_token", value=token, domain="localhost")
    response = client.get("/api/workout-plans")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "Full Body Plan"


def test_get_workout(client, seed_data, app):
    user = seed_data["plan_user"]
    workout = seed_data["workout_plan"]
    token = create_jwt_token(user.id, app)

    client.set_cookie(key="jwt_token", value=token, domain="localhost")
    response = client.get(f"/api/workout-plans/{workout.id}")
    assert response.status_code == 200
    data = response.get_json()[0]["workout"]
    assert data["name"] == "Full Body Plan"
    assert len(data["exercises"]) == 2


def test_get_workout_not_found(client, seed_data, app):
    user = seed_data["plan_user"]
    token = create_jwt_token(user.id, app)
    client.set_cookie(key="jwt_token", value=token, domain="localhost")
    response = client.get("/api/workout-plans/999")
    assert response.status_code == 404
    assert "No workout plan with id 999" in response.get_json()["message"]


def test_delete_workout(client, seed_data, app, session):
    user = seed_data["plan_user"]
    plan = seed_data["workout_plan"]
    token = create_jwt_token(user.id, app)
    client.set_cookie(key="jwt_token", value=token, domain="localhost")
    response = client.delete(f"/api/workout-plans/{plan.id}")
    assert response.status_code == 200
    assert (
        f"Workout plan with id {plan.id} succesfully deleted."
        in response.get_json()["message"]
    )
    deleted_plan = (
        session.query(WorkoutPlan).filter_by(id=plan.id, user_id=user.id).one_or_none()
    )
    assert deleted_plan is None


def test_create_workout_plan(client, seed_data, app, session):
    user = seed_data["plan_user"]
    exercises = seed_data["exercises"]
    token = create_jwt_token(user.id, app)

    payload = {
        "name": "New Plan",
        "exercises": [
            {
                "exercise_id": exercises[0].id,
                "target_sets": 3,
                "target_reps": 10,
                "target_weight": 0,
            }
        ],
    }

    client.set_cookie(key="jwt_token", value=token, domain="localhost")
    response = client.post(
        "/api/workout-plans", data=json.dumps(payload), content_type="application/json"
    )
    json_data = response.get_json()
    assert json_data["message"] == "Workout plan added successfully."
    workout_plan_id = json_data["workout_plan_id"]

    new_plan = (
        session.query(WorkoutPlan)
        .filter_by(user_id=user.id, id=workout_plan_id)
        .one_or_none()
    )
    assert new_plan is not None
    assert len(new_plan.workout_plan_exercises) == 1

    wp_ex = new_plan.workout_plan_exercises[0]
    assert wp_ex.exercise_id == exercises[0].id
    assert wp_ex.target_sets == 3
    assert wp_ex.target_reps == 10
    assert wp_ex.target_weight == 0


def test_update_workout_plan(client, seed_data, app, session):
    user = seed_data["plan_user"]
    plan = seed_data["workout_plan"]
    exercises = seed_data["exercises"]
    token = create_jwt_token(user.id, app)

    payload = {
        "name": "Updated Plan Name",
        "exercises": [
            {
                "exercise_id": exercises[0].id,
                "target_sets": 5,
                "target_reps": 8,
                "target_weight": 20.0,
            }
        ],
    }

    client.set_cookie(key="jwt_token", value=token, domain="localhost")
    response = client.patch(
        f"/api/workout-plans/{plan.id}",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.get_json()["message"] == "Workout plan updated successfully"

    updated_plan = (
        session.query(WorkoutPlan).filter_by(user_id=user.id, id=plan.id).one_or_none()
    )
    assert updated_plan is not None
    assert updated_plan.name == "Updated Plan Name"

    updated_ex = next(
        (
            ex
            for ex in updated_plan.workout_plan_exercises
            if ex.exercise_id == exercises[0].id
        ),
        None,
    )
    assert updated_ex is not None
    assert updated_ex.target_sets == 5
    assert updated_ex.target_reps == 8
    assert updated_ex.target_weight == 20.0

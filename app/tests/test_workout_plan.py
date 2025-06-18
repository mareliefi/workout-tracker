import json
from .test_utils import create_jwt_token 


def auth_headers(token):
    return {"HTTP_COOKIE": f"jwt_token={token}"}


def test_list_workouts(client, seed_data, app):
    user = seed_data["plan_user"]
    token = create_jwt_token(user.id, app)

    client.set_cookie(key='jwt_token', value=token, domain='localhost')
    response = client.get("/api/workout-plans")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "Full Body Plan"


def test_get_workout(client, seed_data, app):
    user = seed_data["plan_user"]
    workout = seed_data["workout_plan"]
    token = create_jwt_token(user.id, app)

    client.set_cookie(key='jwt_token', value=token, domain='localhost')
    response = client.get(f"/api/workout-plans/{workout.id}")
    assert response.status_code == 200
    data = response.get_json()[0]["workout"]
    assert data["name"] == "Full Body Plan"
    assert len(data["exercises"]) == 2


def test_get_workout_not_found(client, seed_data, app):
    user = seed_data["plan_user"]
    token = create_jwt_token(user.id, app)
    client.set_cookie(key='jwt_token', value=token, domain='localhost')
    response = client.get("/api/workout-plans/999")
    assert response.status_code == 404
    assert "No workout plan with id 999" in response.get_json()["message"]


def test_delete_workout(client, seed_data, app):
    user = seed_data["plan_user"]
    plan = seed_data["workout_plan"]
    token = create_jwt_token(user.id, app)
    client.set_cookie(key='jwt_token', value=token, domain='localhost')
    response = client.delete(f"/api/workout-plans/{plan.id}")
    assert response.status_code == 200
    assert f"Workout plan with id {plan.id} succesfully deleted." in response.get_json()["message"]


def test_create_workout_plan(client, seed_data, app):
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
        ]
    }

    client.set_cookie(key='jwt_token', value=token, domain='localhost')
    response = client.post(
        "/api/workout-plans",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 200
    assert "Workout plan added successfully" in response.get_json()["message"]


def test_update_workout_plan(client, seed_data, app):
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
        ]
    }

    client.set_cookie(key='jwt_token', value=token, domain='localhost')
    response = client.patch(
        f"/api/workout-plans/{plan.id}",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 200
    assert "Workout plan updated successfully" in response.get_json()["message"]



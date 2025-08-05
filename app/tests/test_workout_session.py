import json

from ..models import WorkoutSession
from .utils.test_utilities import create_jwt_token


def auth_headers(token):
    return {"HTTP_COOKIE": f"jwt_token={token}"}


def test_list_workout_sessions_with_sessions(client, seed_data, app):
    user = seed_data["plan_user"]
    workout_session = seed_data["workout_session"]
    token = create_jwt_token(user.id, app)

    client.set_cookie(key="jwt_token", value=token, domain="localhost")
    response = client.get("/api/workout-sessions")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == workout_session.id


def test_list_workout_sessions_no_sessions(client, seed_data, app, session):
    user = seed_data["plan_user"]
    # Remove all sessions
    session.query(WorkoutSession).delete()
    session.commit()

    token = create_jwt_token(user.id, app)
    client.set_cookie(key="jwt_token", value=token, domain="localhost")
    response = client.get("/api/workout-sessions")
    assert response.status_code == 200
    assert response.get_json()["message"] == "No workout sessions found for the user."


def test_list_workout_sessions_no_plan(client, seed_data, app):
    user = seed_data["no_plan_user"]
    token = create_jwt_token(user.id, app)
    client.set_cookie(key="jwt_token", value=token, domain="localhost")
    response = client.get("/api/workout-sessions")
    assert response.status_code == 200
    assert response.get_json()["message"] == "No workout plans found for the user."


def test_get_workout_session_found(client, seed_data, app):
    user = seed_data["plan_user"]
    plan = seed_data["workout_plan"]
    workout_session = seed_data["workout_session"]
    token = create_jwt_token(user.id, app)

    client.set_cookie(key="jwt_token", value=token, domain="localhost")
    url = f"/api/workout-sessions/{plan.id}/{workout_session.id}"
    response = client.get(url)
    assert response.status_code == 200
    data = response.get_json()[0]["workout_session"]
    assert data["workout_session_id"] == workout_session.id
    assert data["workout_plan_id"] == plan.id
    assert isinstance(data["session_exercises"], list)
    assert len(data["session_exercises"]) >= 1


def test_get_workout_session_not_found(client, seed_data, app):
    user = seed_data["plan_user"]
    plan = seed_data["workout_plan"]
    token = create_jwt_token(user.id, app)

    client.set_cookie(key="jwt_token", value=token, domain="localhost")
    url = f"/api/workout-sessions/{plan.id}/999"
    response = client.get(url)
    assert response.status_code == 404
    assert "No workout session with id 999" in response.get_json()["message"]


def test_delete_workout_session_found(client, seed_data, app, session):
    user = seed_data["plan_user"]
    plan = seed_data["workout_plan"]
    workout_session = seed_data["workout_session"]
    token = create_jwt_token(user.id, app)

    client.set_cookie(key="jwt_token", value=token, domain="localhost")
    url = f"/api/workout-sessions/{plan.id}/{workout_session.id}"
    response = client.delete(url)
    assert response.status_code == 200
    assert (
        f"Workout session with id {workout_session.id} succesfully deleted."
        in response.get_json()["message"]
    )

    deleted = (
        session.query(WorkoutSession).filter_by(id=workout_session.id).one_or_none()
    )
    assert deleted is None


def test_delete_workout_session_not_found(client, seed_data, app):
    user = seed_data["plan_user"]
    plan = seed_data["workout_plan"]
    token = create_jwt_token(user.id, app)

    client.set_cookie(key="jwt_token", value=token, domain="localhost")
    url = f"/api/workout-sessions/{plan.id}/999"
    response = client.delete(url)
    assert response.status_code == 404
    assert "No workout session with id 999" in response.get_json()["message"]


def test_create_workout_session_valid(client, seed_data, app, session):
    user = seed_data["plan_user"]
    plan = seed_data["workout_plan"]
    plan_exercise = seed_data["plan_exercises"][0]
    token = create_jwt_token(user.id, app)

    payload = {
        "scheduled_at": "2025-07-06T10:00:00",
        "started_at": "2025-07-06T10:05:00",
        "completed_at": "2025-07-06T11:00:00",
        "exercises": [
            {
                "workout_plan_exercise_id": plan_exercise.id,
                "actual_sets": 3,
                "actual_reps": 12,
                "actual_weight": 40.0,
                "notes": "Felt strong",
            }
        ],
    }

    client.set_cookie(key="jwt_token", value=token, domain="localhost")
    url = f"/api/workout-sessions/{plan.id}"
    response = client.post(
        url, data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 200
    assert "Workout session created successfully" in response.get_json()["message"]

    new_session = (
        session.query(WorkoutSession)
        .filter_by(workout_plan_id=plan.id)
        .order_by(WorkoutSession.id.desc())
        .first()
    )
    assert new_session is not None
    assert new_session.started_at is not None
    assert len(new_session.session_exercises) == 1


def test_create_workout_session_plan_not_found(client, seed_data, app):
    user = seed_data["plan_user"]
    token = create_jwt_token(user.id, app)
    payload = {"scheduled_at": "2025-07-06T10:00:00"}

    client.set_cookie(key="jwt_token", value=token, domain="localhost")
    url = "/api/workout-sessions/999"
    response = client.post(
        url, data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 404
    assert "No workout plan with id 999" in response.get_json()["message"]


def test_create_workout_session_invalid_data(client, seed_data, app):
    user = seed_data["plan_user"]
    plan = seed_data["workout_plan"]
    token = create_jwt_token(user.id, app)

    payload = {"scheduled_at": "bad-date"}
    client.set_cookie(key="jwt_token", value=token, domain="localhost")
    url = f"/api/workout-sessions/{plan.id}"
    response = client.post(
        url, data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 400
    assert response.get_json()["status"] == "error"
    assert "scheduled_at" in response.get_json()["errors"]


def test_create_workout_session_exercise_not_in_plan(client, seed_data, app):
    user = seed_data["plan_user"]
    plan = seed_data["workout_plan"]
    token = create_jwt_token(user.id, app)

    payload = {
        "scheduled_at": "2025-07-06T10:00:00",
        "exercises": [
            {
                "workout_plan_exercise_id": 999,
                "actual_sets": 3,
                "actual_reps": 12,
                "actual_weight": 40.0,
            }
        ],
    }

    client.set_cookie(key="jwt_token", value=token, domain="localhost")
    url = f"/api/workout-sessions/{plan.id}"
    response = client.post(
        url, data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 400
    assert "does not exist" in response.get_json()["message"]


def test_update_workout_session_valid(client, seed_data, app, session):
    user = seed_data["plan_user"]
    plan = seed_data["workout_plan"]
    workout_session = seed_data["workout_session"]
    plan_exercise = seed_data["plan_exercises"][0]
    token = create_jwt_token(user.id, app)

    payload = {
        "scheduled_at": "2025-07-07T10:00:00",
        "exercises": [
            {
                "workout_plan_exercise_id": plan_exercise.id,
                "actual_sets": 4,
                "actual_reps": 10,
                "actual_weight": 35.0,
                "notes": "Adjusted weight",
            }
        ],
    }

    client.set_cookie(key="jwt_token", value=token, domain="localhost")
    url = f"/api/workout-sessions/{plan.id}/{workout_session.id}"
    response = client.patch(
        url, data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 200
    assert response.get_json()["message"] == "Workout session updated successfully"

    updated = (
        session.query(WorkoutSession).filter_by(id=workout_session.id).one_or_none()
    )
    assert updated.scheduled_at.isoformat().startswith("2025-07-07")


def test_update_workout_session_not_found(client, seed_data, app):
    user = seed_data["plan_user"]
    plan = seed_data["workout_plan"]
    token = create_jwt_token(user.id, app)

    payload = {"scheduled_at": "2025-07-07T10:00:00"}
    client.set_cookie(key="jwt_token", value=token, domain="localhost")
    url = f"/api/workout-sessions/{plan.id}/999"
    response = client.patch(
        url, data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 404
    assert "No workout session with id 999" in response.get_json()["message"]


def test_update_workout_session_invalid_data(client, seed_data, app):
    user = seed_data["plan_user"]
    plan = seed_data["workout_plan"]
    workout_session = seed_data["workout_session"]
    token = create_jwt_token(user.id, app)

    payload = {"scheduled_at": "bad-date"}
    client.set_cookie(key="jwt_token", value=token, domain="localhost")
    url = f"/api/workout-sessions/{plan.id}/{workout_session.id}"
    response = client.patch(
        url, data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 400
    assert response.get_json()["status"] == "error"
    assert "scheduled_at" in response.get_json()["errors"]


def test_update_workout_session_exercise_not_in_plan(client, seed_data, app):
    user = seed_data["plan_user"]
    plan = seed_data["workout_plan"]
    workout_session = seed_data["workout_session"]
    token = create_jwt_token(user.id, app)

    payload = {
        "scheduled_at": "2025-07-07T10:00:00",
        "exercises": [
            {
                "workout_plan_exercise_id": 999,
                "actual_sets": 4,
                "actual_reps": 10,
                "actual_weight": 35.0,
            }
        ],
    }

    client.set_cookie(key="jwt_token", value=token, domain="localhost")
    url = f"/api/workout-sessions/{plan.id}/{workout_session.id}"
    response = client.patch(
        url, data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 400
    assert "does not exist" in response.get_json()["message"]


def test_create_workout_session_adds_session_exercises(client, seed_data, app, session):
    user = seed_data["plan_user"]
    plan = seed_data["workout_plan"]
    plan_exercise = seed_data["plan_exercises"][0]  # ✅ fixed key
    token = create_jwt_token(user.id, app)

    payload = {
        "scheduled_at": "2025-07-08T10:00:00",
        "started_at": "2025-07-08T10:05:00",
        "completed_at": "2025-07-08T11:00:00",
        "exercises": [
            {
                "workout_plan_exercise_id": plan_exercise.id,
                "actual_sets": 5,
                "actual_reps": 15,
                "actual_weight": 50.0,
                "notes": "New session exercise",
            }
        ],
    }

    client.set_cookie(key="jwt_token", value=token, domain="localhost")
    url = f"/api/workout-sessions/{plan.id}"
    response = client.post(
        url, data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 200
    assert "Workout session created successfully" in response.get_json()["message"]

    new_session = (
        session.query(WorkoutSession)
        .filter_by(workout_plan_id=plan.id)
        .order_by(WorkoutSession.id.desc())
        .first()
    )
    assert new_session is not None
    assert len(new_session.session_exercises) == 1

    session_ex = new_session.session_exercises[0]
    assert session_ex.workout_plan_exercise_id == plan_exercise.id
    assert session_ex.actual_sets == 5
    assert session_ex.actual_reps == 15
    assert session_ex.actual_weight == 50.0
    assert session_ex.notes == "New session exercise"

from .test_utils import create_jwt_token


def test_get_workout_report_success(client, seed_data, app):
    user = seed_data["plan_user"]
    workout_plan = seed_data["workout_plan"]
    token = create_jwt_token(user.id, app)

    client.set_cookie(key="jwt_token", value=token, domain="localhost")
    response = client.get(f"/api/reports/workout-plan/{workout_plan.id}")

    assert response.status_code == 200

    data = response.get_json()
    assert data["id"] == workout_plan.id
    assert data["name"] == workout_plan.name
    assert isinstance(data["exercises"], list)
    assert isinstance(data["sessions"], list)

    ex_ids = [ex["id"] for ex in data["exercises"]]
    plan_ex_ids = [wp_ex.exercise_id for wp_ex in workout_plan.workout_plan_exercises]
    assert set(ex_ids) == set(plan_ex_ids)

    for session in data["sessions"]:
        assert "id" in session
        assert "scheduled_at" in session
        assert "started_at" in session
        assert "completed_at" in session
        assert isinstance(session.get("exercises", []), list)
        for ex in session.get("exercises", []):
            assert "id" in ex
            assert "workout_plan_exercise_id" in ex
            assert "exercise_name" in ex
            assert "actual_sets" in ex
            assert "actual_reps" in ex
            assert "actual_weight" in ex
            assert "notes" in ex


def test_get_workout_report_not_found(client, seed_data, app):
    user = seed_data["plan_user"]
    token = create_jwt_token(user.id, app)
    client.set_cookie(key="jwt_token", value=token, domain="localhost")

    response = client.get("/api/reports/workout-plan/999999")

    assert response.status_code == 404


def test_get_workout_report_unauthorized(client):
    response = client.get("/api/reports/workout-plan/1")
    assert response.status_code == 401


def test_get_workout_report_wrong_user(client, seed_data, app):
    user = seed_data["no_plan_user"]
    workout_plan = seed_data["workout_plan"]
    token = create_jwt_token(user.id, app)

    client.set_cookie(key="jwt_token", value=token, domain="localhost")
    response = client.get(f"/api/reports/workout-plan/{workout_plan.id}")

    assert response.status_code == 404

import json
from .test_utils import create_jwt_token

def test_list_exercises(client, seed_data, app):
    """Test the list_exercises endpoint."""
    with app.app_context():
        plan_user = seed_data["plan_user"]
        exercises = seed_data["exercises"]

        token = create_jwt_token(plan_user.id, app)

        client.set_cookie(key='jwt_token', value=token, domain='localhost')
        response = client.get("/api/exercises")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == len(exercises)

        assert "id" in data[0]
        assert "name" in data[0]
        assert "category" in data[0]


def test_get_exercise(client, seed_data, app):
    """Test getting a single exercise."""
    with app.app_context():
        plan_user = seed_data["plan_user"]
        exercise = seed_data["exercises"][0]

        token = create_jwt_token(plan_user.id, app)

        client.set_cookie(key='jwt_token', value=token, domain='localhost')
        response = client.get(
            f"/api/exercises/{exercise.id}",
            environ_base={"HTTP_COOKIE": f"jwt_token={token}"},
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["id"] == exercise.id
        assert data["name"] == exercise.name
        assert data["category"] == exercise.category


def test_get_exercise_not_found(client, seed_data, app):
    """Test getting a non-existent exercise."""
    with app.app_context():
        plan_user = seed_data["plan_user"]

        token = create_jwt_token(plan_user.id, app)

        client.set_cookie(key='jwt_token', value=token, domain='localhost')
        response = client.get(
            "/api/exercises/999", 
            environ_base={"HTTP_COOKIE": f"jwt_token={token}"},
        )

        assert response.status_code == 404
        data = json.loads(response.data)
        assert data["message"] == "Exercise not found"


def test_token_missing(client):
    """Test that access is denied when token is missing."""
    # Make request without any token
    response = client.get("/api/exercises")

    assert response.status_code == 401
    data = json.loads(response.data)
    assert data["message"] == "Token is missing!"

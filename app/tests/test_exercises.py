import json
from datetime import datetime, timedelta

import jwt
import pytest
from app import create_app, db
from app.models import Exercise, User
from flask import current_app


# Helper function to create a JWT token
def create_jwt_token(user_id, app):
    payload = {"id": user_id, "exp": datetime.now() + timedelta(hours=1)}
    return jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")


def test_list_exercises(client, seed_data, app):
    """Test the list_exercises endpoint."""
    with app.app_context():
        plan_user = seed_data["plan_user"]
        exercises = seed_data["exercises"]

        # Create token within app context
        token = create_jwt_token(plan_user.id, app)

        # Make request with token in cookie
        # Use the with_cookies context manager for Flask's test client
        response = client.get(
            "/api/exercises", environ_base={"HTTP_COOKIE": f"jwt_token={token}"}
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == len(exercises)

        # Check fields
        assert "id" in data[0]
        assert "name" in data[0]
        assert "category" in data[0]


def test_get_exercise(client, seed_data, app):
    """Test getting a single exercise."""
    with app.app_context():
        plan_user = seed_data["plan_user"]
        exercise = seed_data["exercises"][0]

        # Create token within app context
        token = create_jwt_token(plan_user.id, app)

        # Make request with token in cookie
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

        # Create token within app context
        token = create_jwt_token(plan_user.id, app)

        # Make request with token in cookie
        response = client.get(
            "/api/exercises/999",  # Non-existent ID
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

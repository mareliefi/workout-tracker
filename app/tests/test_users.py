import json

from werkzeug.security import generate_password_hash

from ..models import User


def test_signup_success(client, session):
    payload = {
        "name": "John",
        "surname": "Doe",
        "email": "john@example.com",
        "password": "password123",
    }

    response = client.post(
        "/api/auth/signup", data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "registered succesfully" in data["message"].lower()

    user = session.query(User).filter_by(email="john@example.com").one_or_none()
    assert user is not None
    assert user.name == "John"
    assert user.surname == "Doe"
    assert user.email == "john@example.com"


def test_signup_existing_email(client, session, seed_data):
    # Use existing user from seed_data
    existing_user = seed_data[
        "plan_user"
    ]  # or whatever key corresponds to user with email jane@example.com

    payload = {
        "name": "Jane",
        "surname": "Smith",
        "email": existing_user.email,
        "password": "newpass",
    }
    response = client.post(
        "/api/auth/signup", data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "already exists" in data["message"].lower()


def test_login_success(client, session):
    password = "secret123"
    hashed = generate_password_hash(password)
    user = User(
        name="Sam",
        surname="Tester",
        email="sam@example.com",
        password_hash=hashed,
    )
    session.add(user)
    session.commit()

    payload = {"email": "sam@example.com", "password": password}
    response = client.post(
        "/api/auth/login", data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "logged in successfully" in data["message"].lower()


def test_login_invalid_credentials(client, session):
    # Confirm user does not exist
    user = session.query(User).filter_by(email="notfound@example.com").one_or_none()
    assert user is None

    payload = {"email": "notfound@example.com", "password": "nopass"}
    response = client.post(
        "/api/auth/login", data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 401
    data = response.get_json()
    assert "invalid credentials" in data["message"].lower()


def test_logout_clears_token(client):
    response = client.post("/api/auth/logout")
    assert response.status_code == 200
    data = response.get_json()
    assert "logged out successfully" in data["message"].lower()

    cookie_header = response.headers.get("Set-Cookie")
    assert cookie_header is not None
    # It should expire the cookie (expires=0 or expires in the past)
    assert "jwt_token=;" in cookie_header or 'jwt_token="";' in cookie_header
    assert (
        "expires=Thu, 01 Jan 1970" in cookie_header
        or "Expires=Thu, 01 Jan 1970" in cookie_header
    )
    assert "HttpOnly" in cookie_header
    assert "SameSite=Strict" in cookie_header

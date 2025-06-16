import datetime

import jwt
from ..models import User, db
from flask import current_app, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from . import api_bp


@api_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.json
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"message": "Email and password are required"}), 400

    user = db.session.query(User).filter_by(username=data["email"]).one_or_none()

    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    token = jwt.encode(
        {
            "id": user.id,
            "expiry": datetime.datetime.now() + datetime.timedelta(hours=24),
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256",
    )

    response = jsonify({"message": "Logged in successfully"}), 200
    response.set_cookie("jwt_token", token, httponly=True, samesite="Lax")

    return response


@api_bp.route("/auth/signup", methods=["POST"])
def register():
    data = request.json
    if (
        not data
        or not data.get("name")
        or not data.get("surname")
        or not data.get("email")
        or not data.get("password")
    ):
        return jsonify(
            {"message": "Name, surname, email and password are required."}
        ), 400

    existing_user = (
        db.session.query(User).filter_by(email=data.get("email")).one_or_none()
    )
    if existing_user:
        return jsonify({"message": "User already exists. Please login."}), 400

    new_user = User(
        name=data.get("name"),
        email=data.get("email"),
        password=generate_password_hash(data.get("password")),
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(
        {"message": "You have registered succesfully, please proceed to log in."}
    ), 200


@api_bp.route("/auth/logout", methods=["POST"])
def logout():
    response = jsonify({"message": "Logged out successfully"}), 200

    response.set_cookie("jwt_token", "", expires=0, httponly=True, samesite="Strict")

    return response

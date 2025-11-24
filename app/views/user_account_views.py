import datetime
import jwt
from flask import current_app, jsonify, request, make_response
from werkzeug.security import check_password_hash, generate_password_hash
from ..models import User, db
from . import api_bp

@api_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.json
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"message": "Email and password are required"}), 400
    
    user = db.session.query(User).filter_by(email=data["email"]).one_or_none()
    if not user or not check_password_hash(user.password_hash, data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401
    
    token = jwt.encode(
        {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256",
    )
    
    response = make_response(jsonify({
        "message": "Logged in successfully",
        "token": token,  # Add token to response body for localStorage
        "user": {
            "id": user.id,
            "name": user.name,
            "surname": user.surname,
            "email": user.email
        }
    }))
    
    # Also set cookie for cookie-based auth (optional, but good for flexibility)
    response.set_cookie(
        "jwt_token",
        token,
        httponly=True,
        samesite="Lax",
        secure=False,
        max_age=86400,
        path="/"
    )
    
    return response, 200


@api_bp.route("/auth/signup", methods=["POST"])
def register():
    data = request.json
    
    # DEBUG: Print what we received
    print("DEBUG - Received data:", data)
    print("DEBUG - Name:", data.get("name") if data else None)
    print("DEBUG - Surname:", data.get("surname") if data else None)
    print("DEBUG - Email:", data.get("email") if data else None)
    print("DEBUG - Password:", "***" if data and data.get("password") else None)
    
    if (
        not data
        or not data.get("name")
        or not data.get("surname")
        or not data.get("email")
        or not data.get("password")
    ):
        missing_fields = []
        if not data:
            return jsonify({"message": "No data provided"}), 400
        if not data.get("name"):
            missing_fields.append("name")
        if not data.get("surname"):
            missing_fields.append("surname")
        if not data.get("email"):
            missing_fields.append("email")
        if not data.get("password"):
            missing_fields.append("password")
        
        return jsonify({
            "message": f"Missing required fields: {', '.join(missing_fields)}"
        }), 400
    
    existing_user = (
        db.session.query(User).filter_by(email=data.get("email")).one_or_none()
    )
    if existing_user:
        return jsonify({"message": "User already exists. Please login."}), 400
    
    new_user = User(
        name=data.get("name"),
        surname=data.get("surname"),
        email=data.get("email"),
        password_hash=generate_password_hash(data.get("password")),
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(
        {"message": "You have registered successfully, please proceed to log in."}
    ), 200


@api_bp.route("/auth/logout", methods=["POST"])
def logout():
    response = make_response(jsonify({"message": "Logged out successfully"}))
    response.set_cookie(
        "jwt_token",
        "",
        expires=0,
        httponly=True,
        samesite="Lax",
        path="/"
    )
    return response, 200

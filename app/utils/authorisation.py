# app/utils/authorisation.py
from functools import wraps

import jwt
from ..models import User, db 
from flask import current_app, jsonify, request


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("jwt_token")

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            current_user = (
                db.session.query(User).filter_by(id=data.get("id")).one_or_none()
            )
            if not current_user:
                raise Exception("User not found")
        except Exception:
            return jsonify({"message": "Token is invalid!"}), 401

        return f(current_user, *args, **kwargs)

    return decorated

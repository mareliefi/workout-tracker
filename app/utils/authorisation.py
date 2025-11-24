from functools import wraps
import jwt
from flask import current_app, jsonify, request
from ..models import User, db

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Try to get token from Authorization header first (for your current frontend)
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # "Bearer <token>"
            except IndexError:
                return jsonify({"message": "Token format invalid"}), 401
        
        # If not in header, try cookie (fallback)
        if not token:
            token = request.cookies.get("jwt_token")
        
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        
        try:
            # Decode token - jwt automatically checks 'exp' claim
            data = jwt.decode(
                token, 
                current_app.config["SECRET_KEY"], 
                algorithms=["HS256"]
            )
            current_user = (
                db.session.query(User).filter_by(id=data.get("id")).one_or_none()
            )
            if not current_user:
                return jsonify({"message": "User not found"}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token is invalid"}), 401
        except Exception as e:
            return jsonify({"message": "Authentication error"}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

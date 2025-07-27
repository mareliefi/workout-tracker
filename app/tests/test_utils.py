import jwt
from datetime import datetime, timedelta

# Helper function to create a JWT token
def create_jwt_token(user_id, app):
    payload = {"id": user_id, "exp": datetime.now() + timedelta(hours=1)}
    return jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
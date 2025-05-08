from flask import Blueprint

# Create a blueprint for all views
api_bp = Blueprint("api", __name__)

# Import views to register their routes on the blueprint
from . import (
    exercise_views,
    workout_plan_views,
    workout_report_views,
    workout_session_views,
    user_account_views,
)

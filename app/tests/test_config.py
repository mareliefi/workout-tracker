# tests/conftest.py

import pytest
from app import create_app, db
from ..config_test import TestConfig
from app.models import Exercise, SessionExercise, User, WorkoutPlan, WorkoutPlanExercise, WorkoutSession 


@pytest.fixture
def app():
    app = create_app(config_class=TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def seed_data(app):
    """Populates the test DB with sample data."""
    user = User(username="testuser", email="test@example.com")
    db.session.add(user)
    db.session.flush()  # Get user.id

    wp = WorkoutPlan(name="Full Body Plan", user_id=user.id)
    db.session.add(wp)
    db.session.flush()  # Get wp.id

    exercise1 = Exercise(name="Push-Up")
    exercise2 = Exercise(name="Squat")
    db.session.add_all([exercise1, exercise2])
    db.session.flush()

    wp_ex1 = WorkoutPlanExercise(workout_plan_id=wp.id, exercise_id=exercise1.id, target_sets=3, target_reps=12, target_weight=0)
    wp_ex2 = WorkoutPlanExercise(workout_plan_id=wp.id, exercise_id=exercise2.id, target_sets=4, target_reps=10, target_weight=0)
    db.session.add_all([wp_ex1, wp_ex2])

    session = WorkoutSession(user_id=user.id, workout_plan_id=wp.id)
    db.session.add(session)
    db.session.flush()

    sess_ex1 = SessionExercise(workout_session_id=session.id, exercise_id=exercise1.id, actual_sets=3, actual_reps=12, actual_weight=0)
    sess_ex2 = SessionExercise(workout_session_id=session.id, exercise_id=exercise2.id, actual_sets=4, actual_reps=10, actual_weight=0)
    db.session.add_all([sess_ex1, sess_ex2])

    db.session.commit()

    return {
        "user": user,
        "workout_plan": wp,
        "exercises": [exercise1, exercise2],
        "workout_session": session
    }

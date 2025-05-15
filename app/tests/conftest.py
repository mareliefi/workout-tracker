from datetime import datetime, timedelta

import pytest
from app import create_app, db
from app.models import (
    Exercise,
    SessionExercise,
    User,
    WorkoutPlan,
    WorkoutPlanExercise,
    WorkoutSession,
)
from config_test import TestConfig


@pytest.fixture(scope="module")
def app():
    app = create_app(config_class=TestConfig)
    print("✅ App created in env.py")

    with app.app_context():
        # Create all tables in the test database
        db.create_all()

        yield app  # The app is yielded so it can be used in tests

        # Cleanup: drop all tables after tests
        db.session.remove()
        db.drop_all()


# Client fixture to interact with the app
@pytest.fixture
def client(app):
    return app.test_client()


# CLI runner fixture (for running custom CLI commands)
@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def seed_data(app):
    """Populates the test DB with complete sample data."""
    # Create user
    plan_user = User(
        name="Test",
        surname="User",
        email="test@example.com",
        password_hash="fakehashedpassword123",
    )
    db.session.add(plan_user)
    db.session.flush()

    no_plan_user = User(
        name="Test2",
        surname="User2",
        email="test2@example.com",
        password_hash="fakehashedpassword1234",
    )
    db.session.add(no_plan_user)
    db.session.flush()

    # Create workout plan
    wp = WorkoutPlan(name="Full Body Plan", user_id=plan_user.id)
    db.session.add(wp)
    db.session.flush()

    # Create exercises
    exercise1 = Exercise(
        name="Push-Up",
        description="Bodyweight push exercise",
        category="Strength",
        muscle_group="Chest",
    )
    exercise2 = Exercise(
        name="Squat",
        description="Bodyweight leg exercise",
        category="Strength",
        muscle_group="Legs",
    )
    db.session.add_all([exercise1, exercise2])
    db.session.flush()

    # Map exercises to plan
    wp_ex_1 = WorkoutPlanExercise(
        workout_plan_id=wp.id,
        exercise_id=exercise1.id,
        target_sets=3,
        target_reps=12,
        target_weight=0,
    )
    wp_ex_2 = WorkoutPlanExercise(
        workout_plan_id=wp.id,
        exercise_id=exercise2.id,
        target_sets=4,
        target_reps=10,
        target_weight=0,
    )
    db.session.add_all([wp_ex_1, wp_ex_2])
    db.session.flush()

    # Create a workout session
    session = WorkoutSession(
        workout_plan_id=wp.id,
        scheduled_at=datetime.now() + timedelta(days=1),
        started_at=datetime.now(),
        completed_at=datetime.now() + timedelta(hours=1),
    )
    db.session.add(session)
    db.session.flush()

    # Add exercises to session
    sess_ex_1 = SessionExercise(
        workout_session_id=session.id,
        workout_plan_exercise_id=wp_ex_1.id,
        actual_sets=3,
        actual_reps=12,
        actual_weight=0,
        notes="Felt strong",
    )
    sess_ex_2 = SessionExercise(
        workout_session_id=session.id,
        workout_plan_exercise_id=wp_ex_2.id,
        actual_sets=4,
        actual_reps=10,
        actual_weight=0,
        notes="Challenging but completed",
    )
    db.session.add_all([sess_ex_1, sess_ex_2])
    db.session.commit()

    return {
        "plan_user": plan_user,
        "no_plan_user": no_plan_user,
        "workout_plan": wp,
        "exercises": [exercise1, exercise2],
        "plan_exercises": [wp_ex_1, wp_ex_2],
        "workout_session": session,
        "session_exercises": [sess_ex_1, sess_ex_2],
    }

import pytest
from app import create_app, db
from ..config_test import TestConfig
from sqlalchemy.orm import scoped_session, sessionmaker

@pytest.fixture(scope="session")
def app():
    app = create_app(config_class=TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope="function", autouse=True)
def session(app):
    connection = db.engine.connect()
    transaction = connection.begin()

    session_factory = sessionmaker(bind=connection)
    scoped_sess = scoped_session(session_factory)

    db.session = scoped_sess

    yield scoped_sess

    scoped_sess.remove()   
    transaction.rollback()
    connection.close()


@pytest.fixture
def seed_data(session):
    """Populate the database. Session is now per-test and rolls back."""
    from datetime import datetime, timedelta
    from ..models import (
        Exercise,
        SessionExercise,
        User,
        WorkoutPlan,
        WorkoutPlanExercise,
        WorkoutSession,
    )

    # Create users
    plan_user = User(
        name="Test",
        surname="User",
        email="test@example.com",
        password_hash="fakehashedpassword123",
    )
    session.add(plan_user)

    no_plan_user = User(
        name="Test2",
        surname="User2",
        email="test2@example.com",
        password_hash="fakehashedpassword1234",
    )
    session.add(no_plan_user)
    session.flush()

    # Create workout plan
    wp = WorkoutPlan(name="Full Body Plan", user_id=plan_user.id)
    session.add(wp)
    session.flush()

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
    session.add_all([exercise1, exercise2])
    session.flush()

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
    session.add_all([wp_ex_1, wp_ex_2])
    session.flush()

    # Create a workout session
    session_obj = WorkoutSession(
        workout_plan_id=wp.id,
        scheduled_at=datetime.now() + timedelta(days=1),
        started_at=datetime.now(),
        completed_at=datetime.now() + timedelta(hours=1),
    )
    session.add(session_obj)
    session.flush()

    # Add exercises to session
    sess_ex_1 = SessionExercise(
        workout_session_id=session_obj.id,
        workout_plan_exercise_id=wp_ex_1.id,
        actual_sets=3,
        actual_reps=12,
        actual_weight=0,
        notes="Felt strong",
    )
    sess_ex_2 = SessionExercise(
        workout_session_id=session_obj.id,
        workout_plan_exercise_id=wp_ex_2.id,
        actual_sets=4,
        actual_reps=10,
        actual_weight=0,
        notes="Challenging but completed",
    )
    session.add_all([sess_ex_1, sess_ex_2])
    session.commit()

    # Re-fetch all data as session-bound
    return {
        "plan_user": session.query(User).filter_by(email="test@example.com").one(),
        "no_plan_user": session.query(User).filter_by(email="test2@example.com").one(),
        "workout_plan": session.query(WorkoutPlan).filter_by(user_id=plan_user.id).one(),
        "exercises": session.query(Exercise).all(),
        "plan_exercises": session.query(WorkoutPlanExercise).filter_by(workout_plan_id=wp.id).all(),
        "workout_session": session.query(WorkoutSession).filter_by(workout_plan_id=wp.id).one(),
        "session_exercises": session.query(SessionExercise).filter_by(workout_session_id=session_obj.id).all(),
    }



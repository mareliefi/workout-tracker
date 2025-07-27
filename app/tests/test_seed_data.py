def test_workout_session_flow(client, seed_data):
    user = seed_data["plan_user"]
    plan = seed_data["workout_plan"]
    exercises = seed_data["exercises"]
    session = seed_data["workout_session"]
    session_exercises = seed_data["session_exercises"]

    # Check user was created correctly
    assert user.email == "test@example.com"
    assert user.name == "Test"
    assert user.surname == "User"

    # Check workout plan is linked to user
    assert plan.user_id == user.id
    assert plan.name == "Full Body Plan"

    # Check exercises
    assert len(exercises) == 2
    names = [e.name for e in exercises]
    assert "Push-Up" in names
    assert "Squat" in names

    # Check session is scheduled and completed
    assert session.workout_plan_id == plan.id
    assert session.started_at is not None
    assert session.completed_at is not None

    # Check session exercises are linked and correct
    assert len(session_exercises) == 2
    notes = [se.notes for se in session_exercises]
    assert "Felt strong" in notes
    assert "Challenging but completed" in notes

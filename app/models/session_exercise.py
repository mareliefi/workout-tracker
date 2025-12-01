from . import db


class SessionExercise(db.Model):
    __tablename__ = "session_exercises"

    id = db.Column(db.Integer, primary_key=True)
    workout_session_id = db.Column(
        db.Integer,
        db.ForeignKey("workout_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    workout_plan_exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("workout_plan_exercises.id", ondelete="CASCADE"),
        nullable=False,
    )
    actual_sets = db.Column(db.Integer, default=1)
    actual_reps = db.Column(db.Integer, default=1)
    actual_weight = db.Column(db.Float, default=1.0)
    notes = db.Column(db.Text)

    # Relationships
    workout_session = db.relationship(
        "WorkoutSession", back_populates="session_exercises"
    )
    workout_plan_exercise = db.relationship(
        "WorkoutPlanExercise", back_populates="session_exercises"
    )

    def __repr__(self):
        return f"<SessionExercise {self.id}>"

    def validate(self):
        """
        Validates that the exercise and workout session belong to the same workout plan.
        Raises ValueError if validation fails.
        """
        from . import WorkoutPlanExercise

        # Check the exercise exists
        workout_exercise = (
            db.session.query(WorkoutPlanExercise)
            .filter(WorkoutPlanExercise.id == self.workout_plan_exercise_id)
            .one_or_none()
        )
        if not workout_exercise:
            raise ValueError("Invalid workout exercise.")

        # Check the workout session exists
        if not self.workout_session:
            raise ValueError("Invalid workout session.")

        # Ensure they belong to the same workout plan
        if workout_exercise.workout_plan_id != self.workout_session.workout_plan_id:
            raise ValueError("Exercise and session must belong to the same workout plan.")

    def save(self):
        """
        Validates the session exercise.
        Do not commit here; let the calling code commit all changes at once.
        """
        self.validate()
        db.session.add(self)

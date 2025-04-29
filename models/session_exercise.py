from sqlalchemy.exc import IntegrityError
from . import db, WorkoutPlanExercise, WorkoutSession


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
    workout_session = db.relationship("WorkoutSession", backref="session_exercises")
    workout_plan_exercise = db.relationship(
        "WorkoutPlanExercise", backref="session_exercises"
    )

    def __repr__(self):
        return f"<SessionExercise {self.id}>"

    def validate(self):
        """Validates that the exercise and workout session belong to the same workout plan."""
        workout_exercise = (
            db.session.query(WorkoutPlanExercise)
            .filter(WorkoutPlanExercise.id == self.workout_plan_exercise_id)
            .one_or_none()
        )
        workout_session = (
            db.session.query(WorkoutSession)
            .filter(WorkoutSession.id == self.workout_session_id)
            .one_or_none()
        )

        if not workout_exercise or not workout_session:
            raise ValueError("Invalid workout exercise or workout session.")

        if workout_exercise.workout_plan_id != workout_session.workout_plan_id:
            raise ValueError(
                "Exercise and session must belong to the same workout plan."
            )

    def save(self):
        """Saves the session exercise after validation."""
        try:
            self.validate()
            db.session.add(self)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise e

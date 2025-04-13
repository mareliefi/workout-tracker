from . import db


class WorkoutSession(db.Model):
    __tablename__ = "workout_sessions"

    id = db.Column(db.Integer, primary_key=True)
    workout_plan_id = db.Column(
        db.Integer,
        db.ForeignKey("workout_plans.id", ondelete="CASCADE"),
        nullable=False,
    )
    scheduled_at = db.Column(db.DateTime)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)

    # Relationships
    session_exercises = db.relationship(
        "SessionExercise",
        backref="workout_session",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<WorkoutSession {self.id}>"

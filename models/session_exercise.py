from . import db


class SessionExercise(db.Model):
    __tablename__ = "session_exercises"

    id = db.Column(db.Integer, primary_key=True)
    workout_session_id = db.Column(
        db.Integer,
        db.ForeignKey("workout_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    exercise_id = db.Column(
        db.Integer, db.ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False
    )
    actual_sets = db.Column(db.Integer)
    actual_reps = db.Column(db.Integer)
    actual_weight = db.Column(db.Float)
    notes = db.Column(db.Text)

    def __repr__(self):
        return f"<SessionExercise {self.id}>"

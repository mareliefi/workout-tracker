from . import db


class WorkoutPlanExercise(db.Model):
    __tablename__ = "workout_plan_exercises"

    id = db.Column(db.Integer, primary_key=True)
    workout_plan_id = db.Column(
        db.Integer,
        db.ForeignKey("workout_plans.id", ondelete="CASCADE"),
        nullable=False,
    )
    exercise_id = db.Column(
        db.Integer, db.ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False
    )
    target_sets = db.Column(db.Integer, default=1)
    target_reps = db.Column(db.Integer, default=1)
    target_weight = db.Column(db.Float, default=1.0)

    # Relationships
    exercise = db.relationship("Exercise", back_populates="workout_plan_exercises")
    session_exercises = db.relationship(
        "SessionExercise",
        back_populates="workout_plan_exercise",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<WorkoutPlanExercise {self.id}>"

    @classmethod
    def get_by_workout_id_exercise_id(cls, id, workout_plan_id):
        "Get a workout plan exercise by id and workout_plan_id."
        return (
            db.session.query(cls)
            .filter(cls.id == id, cls.workout_plan_id == workout_plan_id)
            .one_or_none()
        )

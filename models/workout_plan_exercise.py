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
    target_sets = db.Column(db.Integer)
    target_reps = db.Column(db.Integer)
    target_weight = db.Column(db.Float)

    def __repr__(self):
        return f"<WorkoutPlanExercise {self.id}>"

from . import db


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    muscle_group = db.Column(db.String(100))

    # Relationships
    workout_plan_exercises = db.relationship(
        "WorkoutPlanExercise", backref="exercise", lazy=True
    )
    session_exercises = db.relationship(
        "SessionExercise", backref="exercise", lazy=True
    )

    def __repr__(self):
        return f"<Exercise {self.name}>"

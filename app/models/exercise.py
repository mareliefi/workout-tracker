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
        "WorkoutPlanExercise", back_populates="exercise"
    )

    def __repr__(self):
        return f"<Exercise {self.name}>"

    def get_by_id(self, id):
        "Get an exercise by id."
        return db.session.query(self).filter(self.id == id).one_or_none()

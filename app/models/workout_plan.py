from sqlalchemy import func
from . import db


class WorkoutPlan(db.Model):
    __tablename__ = "workout_plans"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True,
    )

    # Relationships
    workout_plan_exercises = db.relationship(
        "WorkoutPlanExercise",
        backref="workout_plan",
        lazy=True,
        cascade="all, delete-orphan",
    )
    workout_sessions = db.relationship(
        "WorkoutSession",
        backref="workout_plan",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<WorkoutPlan {self.name}>"

    def get_user_workout_plan(self, user_id, workout_plan_id=None):
        "Get workout plan/all plans for a user."
        query = db.session.query(self).filter(self.user_id == user_id)

        if workout_plan_id is not None:
            query = query.filter(self.id == workout_plan_id)
            return query.one_or_none()
        else:
            return query.all()

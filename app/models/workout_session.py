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
        back_populates="workout_session",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<WorkoutSession {self.id}>"

    def get_by_id(self, id):
        "Get workout session by id."
        return db.session.query(self).filter(self.id == id).one_or_none()

    @classmethod
    def get_session_for_user_plan(cls, user_id, workout_plan_id, session_id):
        "Get workout session for specific workout plan and user."
        from . import WorkoutPlan

        return (
            db.session.query(cls)
            .join(WorkoutPlan, cls.workout_plan_id == WorkoutPlan.id)
            .filter(
                cls.id == session_id,
                cls.workout_plan_id == workout_plan_id,
                WorkoutPlan.user_id == user_id,
            )
            .one_or_none()
        )

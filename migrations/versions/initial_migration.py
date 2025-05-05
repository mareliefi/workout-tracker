# migrations/versions/initial_migration.py
"""Initial migration for workout tracker

Revision ID: 1a2b3c4d5e6f
Revises:
Create Date: 2025-04-13 10:00:00.000000

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic
revision = "1a2b3c4d5e6f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("surname", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

    # Create workout_plans table
    op.create_table(
        "workout_plans",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create exercises table
    op.create_table(
        "exercises",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.Column("muscle_group", sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create workout_plan_exercises table
    op.create_table(
        "workout_plan_exercises",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("workout_plan_id", sa.Integer(), nullable=False),
        sa.Column("exercise_id", sa.Integer(), nullable=False),
        sa.Column("target_sets", sa.Integer(), nullable=True, server_default="1"),
        sa.Column("target_reps", sa.Integer(), nullable=True, server_default="1"),
        sa.Column("target_weight", sa.Float(), nullable=True, server_default="1.0"),
        sa.ForeignKeyConstraint(["exercise_id"], ["exercises.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["workout_plan_id"], ["workout_plans.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create workout_sessions table
    op.create_table(
        "workout_sessions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("workout_plan_id", sa.Integer(), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["workout_plan_id"], ["workout_plans.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create session_exercises table
    op.create_table(
        "session_exercises",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("workout_session_id", sa.Integer(), nullable=False),
        sa.Column("workout_plan_exercise_id", sa.Integer(), nullable=False),
        sa.Column("actual_sets", sa.Integer(), nullable=True, server_default="1"),
        sa.Column("actual_reps", sa.Integer(), nullable=True, server_default="1"),
        sa.Column("actual_weight", sa.Float(), nullable=True, server_default="1.0"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["workout_plan_exercise_id"],
            ["workout_plan_exercises.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["workout_session_id"], ["workout_sessions.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    # Drop tables in reverse order to avoid foreign key constraint errors
    op.drop_table("session_exercises")
    op.drop_table("workout_sessions")
    op.drop_table("workout_plan_exercises")
    op.drop_table("exercises")
    op.drop_table("workout_plans")
    op.drop_table("users")

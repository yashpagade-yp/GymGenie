"""Initial GymGenie schema.

Revision ID: 20260325_0001
Revises:
Create Date: 2026-03-25 00:00:00
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "20260325_0001"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


user_role = postgresql.ENUM("member", "trainer", "owner", name="user_role", create_type=False)
auth_provider = postgresql.ENUM("email", "google", name="auth_provider", create_type=False)
goal_type = postgresql.ENUM("lose", "gain", "maintain", name="goal_type", create_type=False)
diet_preference = postgresql.ENUM("vegetarian", "non_vegetarian", name="diet_preference", create_type=False)
difficulty_level = postgresql.ENUM("beginner", "intermediate", "advanced", name="difficulty_level", create_type=False)
meal_type = postgresql.ENUM("breakfast", "lunch", "snack", "dinner", name="meal_type", create_type=False)
alert_type = postgresql.ENUM("inactive", "goal_stalled", "new_signup", "streak_broken", name="alert_type", create_type=False)
sex_type = postgresql.ENUM("female", "male", name="sex_type", create_type=False)


def upgrade() -> None:
    bind = op.get_bind()
    user_role.create(bind, checkfirst=True)
    auth_provider.create(bind, checkfirst=True)
    goal_type.create(bind, checkfirst=True)
    diet_preference.create(bind, checkfirst=True)
    difficulty_level.create(bind, checkfirst=True)
    meal_type.create(bind, checkfirst=True)
    alert_type.create(bind, checkfirst=True)
    sex_type.create(bind, checkfirst=True)

    op.create_table(
        "gyms",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("address", sa.Text(), nullable=False),
        sa.Column("logo_url", sa.Text(), nullable=True),
        sa.Column("invite_code", sa.String(length=32), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_gyms"),
        sa.UniqueConstraint("invite_code", name="uq_gyms_invite_code"),
    )
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.Text(), nullable=True),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column("auth_provider", auth_provider, nullable=False),
        sa.Column("google_id", sa.String(length=255), nullable=True),
        sa.Column("gym_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["gym_id"], ["gyms.id"], name="fk_users_gym_id_gyms", ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id", name="pk_users"),
        sa.UniqueConstraint("email", name="uq_users_email"),
        sa.UniqueConstraint("google_id", name="uq_users_google_id"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=False)
    op.create_index("ix_users_gym_id", "users", ["gym_id"], unique=False)
    op.create_index("ix_users_role", "users", ["role"], unique=False)
    op.create_index("ix_users_gym_id_role", "users", ["gym_id", "role"], unique=False)

    op.create_table(
        "member_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("height_cm", sa.Float(), nullable=False),
        sa.Column("weight_kg", sa.Float(), nullable=False),
        sa.Column("goal", goal_type, nullable=False),
        sa.Column("diet_preference", diet_preference, nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=True),
        sa.Column("sex", sex_type, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_member_profiles_user_id_users", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_member_profiles"),
        sa.UniqueConstraint("user_id", name="uq_member_profiles_user_id"),
    )
    op.create_index("ix_member_profiles_goal", "member_profiles", ["goal"], unique=False)

    op.create_table(
        "workouts",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("gym_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("video_url", sa.Text(), nullable=True),
        sa.Column("muscle_group", sa.String(length=100), nullable=False),
        sa.Column("goal_type", goal_type, nullable=False),
        sa.Column("difficulty", difficulty_level, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["gym_id"], ["gyms.id"], name="fk_workouts_gym_id_gyms", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_workouts"),
    )
    op.create_index("ix_workouts_goal_difficulty", "workouts", ["goal_type", "difficulty"], unique=False)

    op.create_table(
        "member_workout_plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("workout_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("plan_date", sa.Date(), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column("prescribed_sets", sa.Integer(), nullable=False),
        sa.Column("prescribed_reps", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_member_workout_plans_user_id_users", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["workout_id"], ["workouts.id"], name="fk_member_workout_plans_workout_id_workouts", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_member_workout_plans"),
    )
    op.create_index("ix_member_workout_plans_user_id_plan_date", "member_workout_plans", ["user_id", "plan_date"], unique=False)

    op.create_table(
        "workout_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("workout_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("sets", sa.Integer(), nullable=False),
        sa.Column("reps", sa.Integer(), nullable=False),
        sa.Column("weight_used", sa.Float(), nullable=True),
        sa.Column("is_completed", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("logged_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_workout_logs_user_id_users", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["workout_id"], ["workouts.id"], name="fk_workout_logs_workout_id_workouts", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_workout_logs"),
    )
    op.create_index("ix_workout_logs_user_id_logged_at", "workout_logs", ["user_id", "logged_at"], unique=False)

    op.create_table(
        "diet_plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("plan_date", sa.Date(), nullable=False),
        sa.Column("meal_type", meal_type, nullable=False),
        sa.Column("meal_name", sa.String(length=255), nullable=False),
        sa.Column("calories", sa.Float(), nullable=False),
        sa.Column("protein_g", sa.Float(), nullable=False),
        sa.Column("carbs_g", sa.Float(), nullable=False),
        sa.Column("fats_g", sa.Float(), nullable=False),
        sa.Column("diet_preference", diet_preference, nullable=False),
        sa.Column("goal_type", goal_type, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_diet_plans_user_id_users", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_diet_plans"),
    )
    op.create_index("ix_diet_plans_user_id_plan_date", "diet_plans", ["user_id", "plan_date"], unique=False)

    op.create_table(
        "products",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("gym_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("image_url", sa.Text(), nullable=True),
        sa.Column("in_stock", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["gym_id"], ["gyms.id"], name="fk_products_gym_id_gyms", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_products"),
    )
    op.create_index("ix_products_gym_id", "products", ["gym_id"], unique=False)

    op.create_table(
        "trainer_assignments",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("trainer_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("member_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("gym_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("assigned_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["gym_id"], ["gyms.id"], name="fk_trainer_assignments_gym_id_gyms", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["member_id"], ["users.id"], name="fk_trainer_assignments_member_id_users", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["trainer_id"], ["users.id"], name="fk_trainer_assignments_trainer_id_users", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_trainer_assignments"),
    )
    op.create_index("ix_trainer_assignments_gym_id", "trainer_assignments", ["gym_id"], unique=False)
    op.create_index(
        "ix_trainer_assignments_gym_trainer_member",
        "trainer_assignments",
        ["gym_id", "trainer_id", "member_id"],
        unique=True,
    )

    op.create_table(
        "trainer_notes",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("trainer_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("member_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("note", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["member_id"], ["users.id"], name="fk_trainer_notes_member_id_users", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["trainer_id"], ["users.id"], name="fk_trainer_notes_trainer_id_users", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_trainer_notes"),
    )
    op.create_index("ix_trainer_notes_member_id", "trainer_notes", ["member_id"], unique=False)
    op.create_index("ix_trainer_notes_trainer_id", "trainer_notes", ["trainer_id"], unique=False)

    op.create_table(
        "activity_alerts",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("gym_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("alert_type", alert_type, nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("is_read", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["gym_id"], ["gyms.id"], name="fk_activity_alerts_gym_id_gyms", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_activity_alerts_user_id_users", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_activity_alerts"),
    )
    op.create_index("ix_activity_alerts_gym_id", "activity_alerts", ["gym_id"], unique=False)
    op.create_index("ix_activity_alerts_user_id", "activity_alerts", ["user_id"], unique=False)

    op.execute(
        sa.text(
            """
            INSERT INTO workouts (id, gym_id, title, description, video_url, muscle_group, goal_type, difficulty)
            VALUES
            ('a1111111-1111-1111-1111-111111111111', NULL, 'Incline Treadmill Walk', 'Steady incline walk to improve calorie burn and endurance.', 'https://www.youtube.com/watch?v=l5U_Dfg4xIk', 'cardio', 'lose', 'beginner'),
            ('a2222222-2222-2222-2222-222222222222', NULL, 'Bodyweight Squats', 'Controlled squats focusing on depth and tempo.', 'https://www.youtube.com/watch?v=aclHkVaku9U', 'legs', 'lose', 'beginner'),
            ('a3333333-3333-3333-3333-333333333333', NULL, 'Mountain Climbers', 'Fast-paced core and cardio movement for conditioning.', 'https://www.youtube.com/watch?v=nmwgirgXLYM', 'core', 'lose', 'beginner'),
            ('b1111111-1111-1111-1111-111111111111', NULL, 'Barbell Back Squat', 'Compound lower-body lift for strength progression.', 'https://www.youtube.com/watch?v=Dy28eq2PjcM', 'legs', 'gain', 'intermediate'),
            ('b2222222-2222-2222-2222-222222222222', NULL, 'Bench Press', 'Pressing movement for chest, triceps, and shoulders.', 'https://www.youtube.com/watch?v=rT7DgCr-3pg', 'chest', 'gain', 'intermediate'),
            ('b3333333-3333-3333-3333-333333333333', NULL, 'Lat Pulldown', 'Vertical pulling movement to build upper-back strength.', 'https://www.youtube.com/watch?v=CAwf7n6Luuc', 'back', 'gain', 'beginner'),
            ('c1111111-1111-1111-1111-111111111111', NULL, 'Romanian Deadlift', 'Posterior chain exercise with focus on glutes and hamstrings.', 'https://www.youtube.com/watch?v=2SHsk9AzdjA', 'posterior_chain', 'maintain', 'intermediate'),
            ('c2222222-2222-2222-2222-222222222222', NULL, 'Dumbbell Shoulder Press', 'Balanced upper-body pressing for shoulder strength.', 'https://www.youtube.com/watch?v=B-aVuyhvLHU', 'shoulders', 'maintain', 'beginner'),
            ('c3333333-3333-3333-3333-333333333333', NULL, 'Plank Hold', 'Core stability hold with emphasis on bracing and posture.', 'https://www.youtube.com/watch?v=pSHjTRCQxIw', 'core', 'maintain', 'beginner')
            """
        )
    )


def downgrade() -> None:
    op.drop_index("ix_activity_alerts_user_id", table_name="activity_alerts")
    op.drop_index("ix_activity_alerts_gym_id", table_name="activity_alerts")
    op.drop_table("activity_alerts")
    op.drop_index("ix_trainer_notes_trainer_id", table_name="trainer_notes")
    op.drop_index("ix_trainer_notes_member_id", table_name="trainer_notes")
    op.drop_table("trainer_notes")
    op.drop_index("ix_trainer_assignments_gym_trainer_member", table_name="trainer_assignments")
    op.drop_index("ix_trainer_assignments_gym_id", table_name="trainer_assignments")
    op.drop_table("trainer_assignments")
    op.drop_index("ix_products_gym_id", table_name="products")
    op.drop_table("products")
    op.drop_index("ix_diet_plans_user_id_plan_date", table_name="diet_plans")
    op.drop_table("diet_plans")
    op.drop_index("ix_workout_logs_user_id_logged_at", table_name="workout_logs")
    op.drop_table("workout_logs")
    op.drop_index("ix_member_workout_plans_user_id_plan_date", table_name="member_workout_plans")
    op.drop_table("member_workout_plans")
    op.drop_index("ix_workouts_goal_difficulty", table_name="workouts")
    op.drop_table("workouts")
    op.drop_index("ix_member_profiles_goal", table_name="member_profiles")
    op.drop_table("member_profiles")
    op.drop_index("ix_users_gym_id_role", table_name="users")
    op.drop_index("ix_users_role", table_name="users")
    op.drop_index("ix_users_gym_id", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
    op.drop_table("gyms")

    bind = op.get_bind()
    sex_type.drop(bind, checkfirst=True)
    alert_type.drop(bind, checkfirst=True)
    meal_type.drop(bind, checkfirst=True)
    difficulty_level.drop(bind, checkfirst=True)
    diet_preference.drop(bind, checkfirst=True)
    goal_type.drop(bind, checkfirst=True)
    auth_provider.drop(bind, checkfirst=True)
    user_role.drop(bind, checkfirst=True)

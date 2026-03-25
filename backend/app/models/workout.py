import uuid

from sqlalchemy import Enum, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import DifficultyLevel, GoalType, enum_values


class Workout(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "workouts"
    __table_args__ = (Index("ix_workouts_goal_difficulty", "goal_type", "difficulty"),)

    gym_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("gyms.id", ondelete="CASCADE"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    video_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    muscle_group: Mapped[str] = mapped_column(String(100), nullable=False)
    goal_type: Mapped[GoalType] = mapped_column(
        Enum(GoalType, name="goal_type", create_type=False, values_callable=enum_values),
        nullable=False,
    )
    difficulty: Mapped[DifficultyLevel] = mapped_column(
        Enum(DifficultyLevel, name="difficulty_level", values_callable=enum_values),
        nullable=False,
    )

    plans = relationship("MemberWorkoutPlan", back_populates="workout")
    logs = relationship("WorkoutLog", back_populates="workout")

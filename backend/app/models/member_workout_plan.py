import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey, Index, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class MemberWorkoutPlan(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "member_workout_plans"
    __table_args__ = (Index("ix_member_workout_plans_user_id_plan_date", "user_id", "plan_date"),)

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    workout_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workouts.id", ondelete="CASCADE"), nullable=False)
    plan_date: Mapped[date] = mapped_column(Date, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    prescribed_sets: Mapped[int] = mapped_column(Integer, nullable=False)
    prescribed_reps: Mapped[int] = mapped_column(Integer, nullable=False)

    user = relationship("User", back_populates="workout_plans")
    workout = relationship("Workout", back_populates="plans")

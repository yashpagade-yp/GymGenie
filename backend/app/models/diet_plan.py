import uuid
from datetime import date

from sqlalchemy import Date, Enum, Float, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import DietPreference, GoalType, MealType, enum_values


class DietPlan(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "diet_plans"
    __table_args__ = (Index("ix_diet_plans_user_id_plan_date", "user_id", "plan_date"),)

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    plan_date: Mapped[date] = mapped_column(Date, nullable=False)
    meal_type: Mapped[MealType] = mapped_column(
        Enum(MealType, name="meal_type", values_callable=enum_values),
        nullable=False,
    )
    meal_name: Mapped[str] = mapped_column(String(255), nullable=False)
    calories: Mapped[float] = mapped_column(Float, nullable=False)
    protein_g: Mapped[float] = mapped_column(Float, nullable=False)
    carbs_g: Mapped[float] = mapped_column(Float, nullable=False)
    fats_g: Mapped[float] = mapped_column(Float, nullable=False)
    diet_preference: Mapped[DietPreference] = mapped_column(
        Enum(DietPreference, name="diet_preference", create_type=False, values_callable=enum_values),
        nullable=False,
    )
    goal_type: Mapped[GoalType] = mapped_column(
        Enum(GoalType, name="goal_type", create_type=False, values_callable=enum_values),
        nullable=False,
    )

    user = relationship("User", back_populates="diet_plans")

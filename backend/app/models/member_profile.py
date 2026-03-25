import uuid
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import DietPreference, GoalType, SexType, enum_values


class MemberProfile(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "member_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    height_cm: Mapped[float] = mapped_column(Float, nullable=False)
    weight_kg: Mapped[float] = mapped_column(Float, nullable=False)
    goal: Mapped[GoalType] = mapped_column(
        Enum(GoalType, name="goal_type", values_callable=enum_values),
        nullable=False,
        index=True,
    )
    diet_preference: Mapped[DietPreference] = mapped_column(
        Enum(DietPreference, name="diet_preference", values_callable=enum_values),
        nullable=False,
    )
    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)
    sex: Mapped[SexType | None] = mapped_column(Enum(SexType, name="sex_type", values_callable=enum_values), nullable=True)

    user = relationship("User", back_populates="member_profile")

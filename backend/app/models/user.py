import uuid

from sqlalchemy import Boolean, Enum, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import AuthProvider, UserRole, enum_values


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"
    __table_args__ = (Index("ix_users_gym_id_role", "gym_id", "role"),)

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str | None] = mapped_column(Text, nullable=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role", values_callable=enum_values),
        nullable=False,
        index=True,
    )
    auth_provider: Mapped[AuthProvider] = mapped_column(
        Enum(AuthProvider, name="auth_provider", values_callable=enum_values),
        nullable=False,
    )
    google_id: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    gym_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gyms.id", ondelete="RESTRICT"), nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")

    gym = relationship("Gym", back_populates="users")
    member_profile = relationship("MemberProfile", back_populates="user", uselist=False)
    assigned_members = relationship("TrainerAssignment", back_populates="trainer", foreign_keys="TrainerAssignment.trainer_id")
    assigned_trainers = relationship("TrainerAssignment", back_populates="member", foreign_keys="TrainerAssignment.member_id")
    workout_logs = relationship("WorkoutLog", back_populates="user")
    diet_plans = relationship("DietPlan", back_populates="user")
    workout_plans = relationship("MemberWorkoutPlan", back_populates="user")
    trainer_notes_written = relationship("TrainerNote", back_populates="trainer", foreign_keys="TrainerNote.trainer_id")
    trainer_notes_received = relationship("TrainerNote", back_populates="member", foreign_keys="TrainerNote.member_id")
    alerts = relationship("ActivityAlert", back_populates="user")

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDPrimaryKeyMixin


class TrainerAssignment(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "trainer_assignments"
    __table_args__ = (Index("ix_trainer_assignments_gym_trainer_member", "gym_id", "trainer_id", "member_id", unique=True),)

    trainer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    member_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    gym_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gyms.id", ondelete="CASCADE"), nullable=False, index=True)
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    trainer = relationship("User", back_populates="assigned_members", foreign_keys=[trainer_id])
    member = relationship("User", back_populates="assigned_trainers", foreign_keys=[member_id])
    gym = relationship("Gym", back_populates="assignments")

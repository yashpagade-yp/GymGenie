import uuid

from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class TrainerNote(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "trainer_notes"

    trainer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    member_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    note: Mapped[str] = mapped_column(Text, nullable=False)

    trainer = relationship("User", back_populates="trainer_notes_written", foreign_keys=[trainer_id])
    member = relationship("User", back_populates="trainer_notes_received", foreign_keys=[member_id])

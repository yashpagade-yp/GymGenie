import uuid

from sqlalchemy import Boolean, Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import AlertType, enum_values


class ActivityAlert(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "activity_alerts"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    gym_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gyms.id", ondelete="CASCADE"), nullable=False, index=True)
    alert_type: Mapped[AlertType] = mapped_column(
        Enum(AlertType, name="alert_type", values_callable=enum_values),
        nullable=False,
    )
    message: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")

    user = relationship("User", back_populates="alerts")
    gym = relationship("Gym", back_populates="alerts")

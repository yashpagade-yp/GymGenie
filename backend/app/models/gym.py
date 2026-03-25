from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Gym(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "gyms"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    logo_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    invite_code: Mapped[str | None] = mapped_column(String(32), unique=True, nullable=True)

    users = relationship("User", back_populates="gym")
    products = relationship("Product", back_populates="gym")
    assignments = relationship("TrainerAssignment", back_populates="gym")
    alerts = relationship("ActivityAlert", back_populates="gym")

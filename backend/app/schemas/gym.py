from pydantic import BaseModel, Field

from app.schemas.common import TimestampedResponse


class GymRead(TimestampedResponse):
    name: str
    address: str
    logo_url: str | None
    invite_code: str | None


class GymSettingsUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    address: str | None = Field(default=None, min_length=5)
    logo_url: str | None = None

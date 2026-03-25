from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import TimestampedResponse


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    description: str = Field(min_length=2)
    price: Decimal = Field(gt=0)
    image_url: str | None = None
    in_stock: bool = True


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    description: str | None = Field(default=None, min_length=2)
    price: Decimal | None = Field(default=None, gt=0)
    image_url: str | None = None
    in_stock: bool | None = None


class ProductRead(TimestampedResponse):
    gym_id: UUID
    name: str
    description: str
    price: Decimal
    image_url: str | None
    in_stock: bool

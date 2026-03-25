from datetime import datetime
from uuid import UUID

from pydantic import EmailStr

from app.models.enums import AuthProvider, UserRole
from app.schemas.common import ORMModel


class UserSummary(ORMModel):
    id: UUID
    email: EmailStr
    full_name: str
    role: UserRole
    gym_id: UUID
    auth_provider: AuthProvider
    is_active: bool
    created_at: datetime

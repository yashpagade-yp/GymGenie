from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.schemas.gym import GymRead
from app.schemas.member import MemberProfileRead, WorkoutLogRead
from app.schemas.trainer import ActivityAlertRead
from app.schemas.user import UserSummary


class TrainerCreateRequest(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=255)
    password: str = Field(min_length=8, max_length=128)


class TrainerAssignmentRequest(BaseModel):
    trainer_id: UUID
    member_id: UUID


class OwnerMemberDetailRead(BaseModel):
    member: UserSummary
    profile: MemberProfileRead | None
    recent_workouts: list[WorkoutLogRead]
    assigned_trainer_ids: list[UUID]


class OwnerDashboardSummary(BaseModel):
    gym: GymRead
    alerts: list[ActivityAlertRead]

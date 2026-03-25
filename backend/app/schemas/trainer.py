from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import AlertType, DietPreference, GoalType
from app.schemas.common import ORMModel
from app.schemas.member import MemberProfileRead, WorkoutLogRead


class TrainerAssignedMemberRead(BaseModel):
    user_id: UUID
    full_name: str
    email: str
    goal: GoalType | None
    diet_preference: DietPreference | None
    last_workout_at: datetime | None
    workouts_completed: int
    is_at_risk: bool


class TrainerMemberDetailRead(BaseModel):
    member: TrainerAssignedMemberRead
    profile: MemberProfileRead | None
    recent_workouts: list[WorkoutLogRead]


class TrainerNoteCreate(BaseModel):
    note: str


class TrainerNoteRead(ORMModel):
    id: UUID
    trainer_id: UUID
    member_id: UUID
    note: str
    created_at: datetime
    updated_at: datetime


class ActivityAlertRead(ORMModel):
    id: UUID
    user_id: UUID
    gym_id: UUID
    alert_type: AlertType
    message: str
    is_read: bool
    created_at: datetime
    updated_at: datetime

from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_trainer
from app.db.session import get_db_session
from app.schemas.trainer import (
    ActivityAlertRead,
    TrainerAssignedMemberRead,
    TrainerMemberDetailRead,
    TrainerNoteCreate,
    TrainerNoteRead,
)
from app.services.trainer import (
    create_trainer_note,
    get_trainer_member_detail,
    list_assigned_members,
    list_trainer_alerts,
    list_trainer_notes,
)

router = APIRouter()


@router.get("/members/assigned", response_model=list[TrainerAssignedMemberRead], summary="List assigned members")
async def get_assigned_members(
    current_trainer=Depends(get_current_trainer),
    session: AsyncSession = Depends(get_db_session),
) -> list[TrainerAssignedMemberRead]:
    return await list_assigned_members(session, current_trainer)


@router.get("/members/{member_id}", response_model=TrainerMemberDetailRead, summary="Get assigned member CRM detail")
async def get_member_detail(
    member_id: UUID,
    current_trainer=Depends(get_current_trainer),
    session: AsyncSession = Depends(get_db_session),
) -> TrainerMemberDetailRead:
    return await get_trainer_member_detail(session, current_trainer, member_id)


@router.post("/members/{member_id}/notes", response_model=TrainerNoteRead, status_code=status.HTTP_201_CREATED, summary="Add a private note for a member")
async def add_note(
    member_id: UUID,
    payload: TrainerNoteCreate,
    current_trainer=Depends(get_current_trainer),
    session: AsyncSession = Depends(get_db_session),
) -> TrainerNoteRead:
    note = await create_trainer_note(session, current_trainer, member_id, payload.note)
    return TrainerNoteRead.model_validate(note)


@router.get("/members/{member_id}/notes", response_model=list[TrainerNoteRead], summary="List private notes for a member")
async def get_notes(
    member_id: UUID,
    current_trainer=Depends(get_current_trainer),
    session: AsyncSession = Depends(get_db_session),
) -> list[TrainerNoteRead]:
    notes = await list_trainer_notes(session, current_trainer, member_id)
    return [TrainerNoteRead.model_validate(note) for note in notes]


@router.get("/alerts", response_model=list[ActivityAlertRead], summary="List trainer alerts")
async def get_alerts(
    current_trainer=Depends(get_current_trainer),
    session: AsyncSession = Depends(get_db_session),
) -> list[ActivityAlertRead]:
    alerts = await list_trainer_alerts(session, current_trainer)
    return [ActivityAlertRead.model_validate(alert) for alert in alerts]

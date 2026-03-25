from datetime import UTC, datetime, timedelta
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activity_alert import ActivityAlert
from app.models.enums import AlertType, UserRole
from app.models.member_profile import MemberProfile
from app.models.trainer_assignment import TrainerAssignment
from app.models.trainer_note import TrainerNote
from app.models.user import User
from app.models.workout_log import WorkoutLog
from app.schemas.member import MemberProfileRead, WorkoutLogRead
from app.schemas.trainer import TrainerAssignedMemberRead, TrainerMemberDetailRead


async def _ensure_assigned_member(session: AsyncSession, trainer: User, member_id: UUID) -> User:
    member = await session.scalar(
        select(User)
        .join(
            TrainerAssignment,
            (TrainerAssignment.member_id == User.id) & (TrainerAssignment.trainer_id == trainer.id),
        )
        .where(
            User.id == member_id,
            User.gym_id == trainer.gym_id,
            User.role == UserRole.MEMBER,
            User.is_active.is_(True),
        )
    )
    if member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assigned member not found")
    return member


async def list_assigned_members(session: AsyncSession, trainer: User) -> list[TrainerAssignedMemberRead]:
    last_week = datetime.now(UTC) - timedelta(days=7)
    rows = (
        await session.execute(
            select(
                User.id,
                User.full_name,
                User.email,
                MemberProfile.goal,
                MemberProfile.diet_preference,
                func.max(WorkoutLog.logged_at),
                func.count(WorkoutLog.id).filter(WorkoutLog.is_completed.is_(True)),
            )
            .join(TrainerAssignment, TrainerAssignment.member_id == User.id)
            .outerjoin(MemberProfile, MemberProfile.user_id == User.id)
            .outerjoin(WorkoutLog, WorkoutLog.user_id == User.id)
            .where(TrainerAssignment.trainer_id == trainer.id, User.gym_id == trainer.gym_id, User.is_active.is_(True))
            .group_by(User.id, MemberProfile.goal, MemberProfile.diet_preference)
            .order_by(User.full_name.asc())
        )
    ).all()

    members: list[TrainerAssignedMemberRead] = []
    for user_id, full_name, email, goal, diet_preference, last_workout_at, workouts_completed in rows:
        members.append(
            TrainerAssignedMemberRead(
                user_id=user_id,
                full_name=full_name,
                email=email,
                goal=goal,
                diet_preference=diet_preference,
                last_workout_at=last_workout_at,
                workouts_completed=workouts_completed or 0,
                is_at_risk=last_workout_at is None or last_workout_at < last_week,
            )
        )
    return members


async def create_trainer_note(session: AsyncSession, trainer: User, member_id: UUID, note: str) -> TrainerNote:
    await _ensure_assigned_member(session, trainer, member_id)
    trainer_note = TrainerNote(trainer_id=trainer.id, member_id=member_id, note=note)
    session.add(trainer_note)
    await session.commit()
    await session.refresh(trainer_note)
    return trainer_note


async def list_trainer_notes(session: AsyncSession, trainer: User, member_id: UUID) -> list[TrainerNote]:
    await _ensure_assigned_member(session, trainer, member_id)
    return (
        await session.scalars(
            select(TrainerNote)
            .where(TrainerNote.trainer_id == trainer.id, TrainerNote.member_id == member_id)
            .order_by(TrainerNote.created_at.desc())
        )
    ).all()


async def list_trainer_alerts(session: AsyncSession, trainer: User) -> list[ActivityAlert]:
    assigned_member_ids = (
        await session.scalars(
            select(TrainerAssignment.member_id).where(TrainerAssignment.trainer_id == trainer.id, TrainerAssignment.gym_id == trainer.gym_id)
        )
    ).all()
    if not assigned_member_ids:
        return []

    return (
        await session.scalars(
            select(ActivityAlert)
            .where(ActivityAlert.user_id.in_(assigned_member_ids), ActivityAlert.gym_id == trainer.gym_id)
            .order_by(ActivityAlert.created_at.desc())
        )
    ).all()


async def get_trainer_member_detail(session: AsyncSession, trainer: User, member_id: UUID) -> TrainerMemberDetailRead:
    member = await _ensure_assigned_member(session, trainer, member_id)
    members = await list_assigned_members(session, trainer)
    member_summary = next(item for item in members if item.user_id == member.id)
    profile = await session.scalar(select(MemberProfile).where(MemberProfile.user_id == member.id))
    recent_logs = (
        await session.scalars(
            select(WorkoutLog).where(WorkoutLog.user_id == member.id).order_by(WorkoutLog.logged_at.desc()).limit(10)
        )
    ).all()
    return TrainerMemberDetailRead(
        member=member_summary,
        profile=MemberProfileRead.model_validate(profile) if profile else None,
        recent_workouts=[WorkoutLogRead.model_validate(log) for log in recent_logs],
    )

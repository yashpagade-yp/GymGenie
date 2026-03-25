from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.member_profile import MemberProfile
from app.models.product import Product
from app.models.user import User
from app.models.workout_log import WorkoutLog
from app.schemas.member import MemberProfileUpsert, WorkoutLogCreate
from app.services.plan_generation import ensure_onboarded, get_or_create_diet_plan, get_or_create_workout_plan, utcnow


async def get_member_profile(session: AsyncSession, member_id) -> MemberProfile | None:
    return await session.scalar(select(MemberProfile).where(MemberProfile.user_id == member_id))


async def upsert_member_profile(session: AsyncSession, user: User, payload: MemberProfileUpsert) -> MemberProfile:
    profile = await get_member_profile(session, user.id)
    if profile is None:
        profile = MemberProfile(user_id=user.id, **payload.model_dump())
        session.add(profile)
    else:
        for field, value in payload.model_dump().items():
            setattr(profile, field, value)
    await session.commit()
    await session.refresh(profile)
    return profile


async def get_member_workout_plan(session: AsyncSession, user: User, plan_date: date):
    profile = ensure_onboarded(await get_member_profile(session, user.id))
    return await get_or_create_workout_plan(session, user, profile, plan_date)


async def get_member_diet_plan(session: AsyncSession, user: User, plan_date: date):
    profile = ensure_onboarded(await get_member_profile(session, user.id))
    return await get_or_create_diet_plan(session, user, profile, plan_date)


async def create_workout_log(session: AsyncSession, user: User, payload: WorkoutLogCreate) -> WorkoutLog:
    log = WorkoutLog(
        user_id=user.id,
        workout_id=payload.workout_id,
        sets=payload.sets,
        reps=payload.reps,
        weight_used=payload.weight_used,
        is_completed=payload.is_completed,
        logged_at=utcnow(),
    )
    session.add(log)
    await session.commit()
    await session.refresh(log)
    return log


async def list_workout_history(session: AsyncSession, user: User) -> list[WorkoutLog]:
    return (
        await session.scalars(
            select(WorkoutLog).where(WorkoutLog.user_id == user.id).order_by(WorkoutLog.logged_at.desc()).limit(50)
        )
    ).all()


async def list_gym_products(session: AsyncSession, gym_id):
    return (
        await session.scalars(
            select(Product).where(Product.gym_id == gym_id, Product.in_stock.is_(True)).order_by(Product.created_at.desc())
        )
    ).all()

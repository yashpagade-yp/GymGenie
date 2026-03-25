from datetime import UTC, datetime, timedelta
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models.activity_alert import ActivityAlert
from app.models.enums import AlertType, AuthProvider, UserRole
from app.models.gym import Gym
from app.models.member_profile import MemberProfile
from app.models.product import Product
from app.models.trainer_assignment import TrainerAssignment
from app.models.user import User
from app.models.workout_log import WorkoutLog
from app.schemas.gym import GymSettingsUpdate
from app.schemas.member import MemberProfileRead, WorkoutLogRead
from app.schemas.owner import OwnerMemberDetailRead, TrainerCreateRequest
from app.schemas.product import ProductCreate, ProductUpdate
from app.schemas.user import UserSummary


async def list_users_by_role(session: AsyncSession, gym_id, role: UserRole) -> list[User]:
    return (
        await session.scalars(
            select(User).where(User.gym_id == gym_id, User.role == role, User.is_active.is_(True)).order_by(User.full_name.asc())
        )
    ).all()


async def create_trainer(session: AsyncSession, owner: User, payload: TrainerCreateRequest) -> User:
    existing = await session.scalar(select(User).where(User.email == payload.email))
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")

    trainer = User(
        email=payload.email,
        full_name=payload.full_name,
        password_hash=get_password_hash(payload.password),
        role=UserRole.TRAINER,
        auth_provider=AuthProvider.EMAIL,
        gym_id=owner.gym_id,
    )
    session.add(trainer)
    await session.commit()
    await session.refresh(trainer)
    return trainer


async def deactivate_user(session: AsyncSession, gym_id, user_id: UUID, role: UserRole) -> None:
    user = await session.scalar(select(User).where(User.id == user_id, User.gym_id == gym_id, User.role == role))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.is_active = False
    await session.commit()


async def assign_trainer(session: AsyncSession, gym_id, trainer_id: UUID, member_id: UUID) -> None:
    trainer = await session.scalar(select(User).where(User.id == trainer_id, User.gym_id == gym_id, User.role == UserRole.TRAINER))
    member = await session.scalar(select(User).where(User.id == member_id, User.gym_id == gym_id, User.role == UserRole.MEMBER))
    if trainer is None or member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trainer or member not found")

    existing = await session.scalar(
        select(TrainerAssignment).where(
            TrainerAssignment.trainer_id == trainer_id,
            TrainerAssignment.member_id == member_id,
            TrainerAssignment.gym_id == gym_id,
        )
    )
    if existing is not None:
        return

    session.add(
        TrainerAssignment(
            trainer_id=trainer_id,
            member_id=member_id,
            gym_id=gym_id,
            assigned_at=datetime.now(UTC),
        )
    )
    session.add(
        ActivityAlert(
            user_id=member_id,
            gym_id=gym_id,
            alert_type=AlertType.NEW_SIGNUP,
            message="A trainer has been assigned to this member.",
        )
    )
    await session.commit()


async def unassign_trainer(session: AsyncSession, gym_id, trainer_id: UUID, member_id: UUID) -> None:
    assignment = await session.scalar(
        select(TrainerAssignment).where(
            TrainerAssignment.trainer_id == trainer_id,
            TrainerAssignment.member_id == member_id,
            TrainerAssignment.gym_id == gym_id,
        )
    )
    if assignment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
    await session.delete(assignment)
    await session.commit()


async def create_product(session: AsyncSession, gym_id, payload: ProductCreate) -> Product:
    product = Product(gym_id=gym_id, **payload.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


async def list_products(session: AsyncSession, gym_id) -> list[Product]:
    return (
        await session.scalars(select(Product).where(Product.gym_id == gym_id).order_by(Product.created_at.desc()))
    ).all()


async def update_product(session: AsyncSession, gym_id, product_id: UUID, payload: ProductUpdate) -> Product:
    product = await session.scalar(select(Product).where(Product.id == product_id, Product.gym_id == gym_id))
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    await session.commit()
    await session.refresh(product)
    return product


async def delete_product(session: AsyncSession, gym_id, product_id: UUID) -> None:
    product = await session.scalar(select(Product).where(Product.id == product_id, Product.gym_id == gym_id))
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    await session.delete(product)
    await session.commit()


async def refresh_inactivity_alerts(session: AsyncSession, gym_id) -> None:
    cutoff = datetime.now(UTC) - timedelta(days=7)
    members = (
        await session.scalars(select(User).where(User.gym_id == gym_id, User.role == UserRole.MEMBER, User.is_active.is_(True)))
    ).all()
    for member in members:
        last_workout_at = await session.scalar(
            select(func.max(WorkoutLog.logged_at)).where(WorkoutLog.user_id == member.id)
        )
        if last_workout_at is None or last_workout_at < cutoff:
            existing = await session.scalar(
                select(ActivityAlert).where(
                    ActivityAlert.user_id == member.id,
                    ActivityAlert.gym_id == gym_id,
                    ActivityAlert.alert_type == AlertType.INACTIVE,
                    ActivityAlert.is_read.is_(False),
                )
            )
            if existing is None:
                session.add(
                    ActivityAlert(
                        user_id=member.id,
                        gym_id=gym_id,
                        alert_type=AlertType.INACTIVE,
                        message="Member has not logged a workout in the last 7 days.",
                    )
                )
    await session.commit()


async def list_owner_alerts(session: AsyncSession, gym_id) -> list[ActivityAlert]:
    return (
        await session.scalars(
            select(ActivityAlert).where(ActivityAlert.gym_id == gym_id).order_by(ActivityAlert.created_at.desc()).limit(100)
        )
    ).all()


async def get_owner_member_detail(session: AsyncSession, gym_id, member_id: UUID) -> OwnerMemberDetailRead:
    member = await session.scalar(
        select(User).where(User.id == member_id, User.gym_id == gym_id, User.role == UserRole.MEMBER, User.is_active.is_(True))
    )
    if member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")

    profile = await session.scalar(select(MemberProfile).where(MemberProfile.user_id == member.id))
    recent_logs = (
        await session.scalars(
            select(WorkoutLog).where(WorkoutLog.user_id == member.id).order_by(WorkoutLog.logged_at.desc()).limit(10)
        )
    ).all()
    assigned_trainer_ids = (
        await session.scalars(
            select(TrainerAssignment.trainer_id).where(TrainerAssignment.member_id == member.id, TrainerAssignment.gym_id == gym_id)
        )
    ).all()
    return OwnerMemberDetailRead(
        member=UserSummary.model_validate(member),
        profile=MemberProfileRead.model_validate(profile) if profile else None,
        recent_workouts=[WorkoutLogRead.model_validate(log) for log in recent_logs],
        assigned_trainer_ids=list(assigned_trainer_ids),
    )


async def get_gym_settings(session: AsyncSession, gym_id) -> Gym:
    gym = await session.scalar(select(Gym).where(Gym.id == gym_id))
    if gym is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gym not found")
    return gym


async def update_gym_settings(session: AsyncSession, gym_id, payload: GymSettingsUpdate) -> Gym:
    gym = await get_gym_settings(session, gym_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(gym, field, value)
    await session.commit()
    await session.refresh(gym)
    return gym

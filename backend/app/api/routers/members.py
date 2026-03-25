from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_member
from app.db.session import get_db_session
from app.schemas.member import MemberProfileRead, MemberProfileUpsert, TodayDietResponse, TodayWorkoutResponse, WorkoutLogCreate, WorkoutLogRead
from app.schemas.product import ProductRead
from app.schemas.user import UserSummary
from app.services.member import (
    create_workout_log,
    get_member_diet_plan,
    get_member_profile,
    get_member_workout_plan,
    list_gym_products,
    list_workout_history,
    upsert_member_profile,
)

router = APIRouter()


@router.get("/me", response_model=UserSummary, summary="Get the current member account")
async def get_member_me(current_member=Depends(get_current_member)) -> UserSummary:
    return UserSummary.model_validate(current_member)


@router.get("/profile", response_model=MemberProfileRead | None, summary="Get the member onboarding profile")
async def get_profile(current_member=Depends(get_current_member), session: AsyncSession = Depends(get_db_session)):
    profile = await get_member_profile(session, current_member.id)
    return MemberProfileRead.model_validate(profile) if profile else None


@router.post("/onboarding", response_model=MemberProfileRead, summary="Complete member onboarding")
async def complete_onboarding(
    payload: MemberProfileUpsert,
    current_member=Depends(get_current_member),
    session: AsyncSession = Depends(get_db_session),
) -> MemberProfileRead:
    profile = await upsert_member_profile(session, current_member, payload)
    return MemberProfileRead.model_validate(profile)


@router.put("/profile", response_model=MemberProfileRead, summary="Update member onboarding profile")
async def update_profile(
    payload: MemberProfileUpsert,
    current_member=Depends(get_current_member),
    session: AsyncSession = Depends(get_db_session),
) -> MemberProfileRead:
    profile = await upsert_member_profile(session, current_member, payload)
    return MemberProfileRead.model_validate(profile)


@router.get("/workouts/today", response_model=TodayWorkoutResponse, summary="Get today's workout plan")
async def get_today_workout(
    current_member=Depends(get_current_member),
    session: AsyncSession = Depends(get_db_session),
    plan_date: date | None = Query(default=None),
) -> TodayWorkoutResponse:
    return await get_member_workout_plan(session, current_member, plan_date or date.today())


@router.get("/diet/today", response_model=TodayDietResponse, summary="Get today's diet plan")
async def get_today_diet(
    current_member=Depends(get_current_member),
    session: AsyncSession = Depends(get_db_session),
    plan_date: date | None = Query(default=None),
) -> TodayDietResponse:
    return await get_member_diet_plan(session, current_member, plan_date or date.today())


@router.post("/workouts/log", response_model=WorkoutLogRead, status_code=status.HTTP_201_CREATED, summary="Log a workout")
async def log_workout(
    payload: WorkoutLogCreate,
    current_member=Depends(get_current_member),
    session: AsyncSession = Depends(get_db_session),
) -> WorkoutLogRead:
    workout_log = await create_workout_log(session, current_member, payload)
    return WorkoutLogRead.model_validate(workout_log)


@router.get("/workouts/history", response_model=list[WorkoutLogRead], summary="Get workout history")
async def get_workout_history(
    current_member=Depends(get_current_member),
    session: AsyncSession = Depends(get_db_session),
) -> list[WorkoutLogRead]:
    logs = await list_workout_history(session, current_member)
    return [WorkoutLogRead.model_validate(log) for log in logs]


@router.get("/products", response_model=list[ProductRead], summary="Browse the gym product catalog")
async def get_products(
    current_member=Depends(get_current_member),
    session: AsyncSession = Depends(get_db_session),
) -> list[ProductRead]:
    products = await list_gym_products(session, current_member.gym_id)
    return [ProductRead.model_validate(product) for product in products]

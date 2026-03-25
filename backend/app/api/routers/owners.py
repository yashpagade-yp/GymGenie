from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_owner
from app.db.session import get_db_session
from app.models.enums import UserRole
from app.schemas.analytics import ActivityTrendPoint, GoalDistributionItem, RetentionAnalytics
from app.schemas.gym import GymRead, GymSettingsUpdate
from app.schemas.owner import OwnerMemberDetailRead, TrainerAssignmentRequest, TrainerCreateRequest
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.schemas.trainer import ActivityAlertRead
from app.schemas.user import UserSummary
from app.services.analytics import get_activity_trends, get_goal_distribution, get_retention_analytics
from app.services.owner import (
    assign_trainer,
    create_product,
    create_trainer,
    deactivate_user,
    delete_product,
    get_gym_settings,
    get_owner_member_detail,
    list_products,
    list_owner_alerts,
    list_users_by_role,
    refresh_inactivity_alerts,
    unassign_trainer,
    update_gym_settings,
    update_product,
)

router = APIRouter()


@router.get("/members", response_model=list[UserSummary], summary="List all members in the gym")
async def get_members(current_owner=Depends(get_current_owner), session: AsyncSession = Depends(get_db_session)) -> list[UserSummary]:
    members = await list_users_by_role(session, current_owner.gym_id, UserRole.MEMBER)
    return [UserSummary.model_validate(member) for member in members]


@router.get("/members/{member_id}", response_model=OwnerMemberDetailRead, summary="Get member CRM detail")
async def get_member_detail(
    member_id: UUID,
    current_owner=Depends(get_current_owner),
    session: AsyncSession = Depends(get_db_session),
) -> OwnerMemberDetailRead:
    return await get_owner_member_detail(session, current_owner.gym_id, member_id)


@router.delete("/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Deactivate a member")
async def remove_member(
    member_id: UUID,
    current_owner=Depends(get_current_owner),
    session: AsyncSession = Depends(get_db_session),
) -> Response:
    await deactivate_user(session, current_owner.gym_id, member_id, UserRole.MEMBER)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/trainers", response_model=list[UserSummary], summary="List all trainers in the gym")
async def get_trainers(current_owner=Depends(get_current_owner), session: AsyncSession = Depends(get_db_session)) -> list[UserSummary]:
    trainers = await list_users_by_role(session, current_owner.gym_id, UserRole.TRAINER)
    return [UserSummary.model_validate(trainer) for trainer in trainers]


@router.post("/trainers", response_model=UserSummary, status_code=status.HTTP_201_CREATED, summary="Create a trainer account")
async def create_trainer_account(
    payload: TrainerCreateRequest,
    current_owner=Depends(get_current_owner),
    session: AsyncSession = Depends(get_db_session),
) -> UserSummary:
    trainer = await create_trainer(session, current_owner, payload)
    return UserSummary.model_validate(trainer)


@router.delete("/trainers/{trainer_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Deactivate a trainer")
async def remove_trainer(
    trainer_id: UUID,
    current_owner=Depends(get_current_owner),
    session: AsyncSession = Depends(get_db_session),
) -> Response:
    await deactivate_user(session, current_owner.gym_id, trainer_id, UserRole.TRAINER)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/trainers/assign", status_code=status.HTTP_204_NO_CONTENT, summary="Assign a trainer to a member")
async def assign_trainer_to_member(
    payload: TrainerAssignmentRequest,
    current_owner=Depends(get_current_owner),
    session: AsyncSession = Depends(get_db_session),
) -> Response:
    await assign_trainer(session, current_owner.gym_id, payload.trainer_id, payload.member_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/trainers/unassign", status_code=status.HTTP_204_NO_CONTENT, summary="Unassign a trainer from a member")
async def unassign_trainer_from_member(
    payload: TrainerAssignmentRequest,
    current_owner=Depends(get_current_owner),
    session: AsyncSession = Depends(get_db_session),
) -> Response:
    await unassign_trainer(session, current_owner.gym_id, payload.trainer_id, payload.member_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/products", response_model=list[ProductRead], summary="List gym products")
async def get_products(current_owner=Depends(get_current_owner), session: AsyncSession = Depends(get_db_session)) -> list[ProductRead]:
    products = await list_products(session, current_owner.gym_id)
    return [ProductRead.model_validate(product) for product in products]


@router.post("/products", response_model=ProductRead, status_code=status.HTTP_201_CREATED, summary="Create a product")
async def create_product_record(
    payload: ProductCreate,
    current_owner=Depends(get_current_owner),
    session: AsyncSession = Depends(get_db_session),
) -> ProductRead:
    product = await create_product(session, current_owner.gym_id, payload)
    return ProductRead.model_validate(product)


@router.patch("/products/{product_id}", response_model=ProductRead, summary="Update a product")
async def patch_product(
    product_id: UUID,
    payload: ProductUpdate,
    current_owner=Depends(get_current_owner),
    session: AsyncSession = Depends(get_db_session),
) -> ProductRead:
    product = await update_product(session, current_owner.gym_id, product_id, payload)
    return ProductRead.model_validate(product)


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a product")
async def remove_product(
    product_id: UUID,
    current_owner=Depends(get_current_owner),
    session: AsyncSession = Depends(get_db_session),
) -> Response:
    await delete_product(session, current_owner.gym_id, product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/analytics/retention", response_model=RetentionAnalytics, summary="Get retention analytics")
async def retention_analytics(
    current_owner=Depends(get_current_owner),
    session: AsyncSession = Depends(get_db_session),
) -> RetentionAnalytics:
    await refresh_inactivity_alerts(session, current_owner.gym_id)
    return await get_retention_analytics(session, current_owner.gym_id)


@router.get("/analytics/goals", response_model=list[GoalDistributionItem], summary="Get goal distribution analytics")
async def goal_distribution(
    current_owner=Depends(get_current_owner),
    session: AsyncSession = Depends(get_db_session),
) -> list[GoalDistributionItem]:
    return await get_goal_distribution(session, current_owner.gym_id)


@router.get("/analytics/activity", response_model=list[ActivityTrendPoint], summary="Get activity trend analytics")
async def activity_analytics(
    current_owner=Depends(get_current_owner),
    session: AsyncSession = Depends(get_db_session),
) -> list[ActivityTrendPoint]:
    return await get_activity_trends(session, current_owner.gym_id)


@router.get("/alerts", response_model=list[ActivityAlertRead], summary="List owner alerts")
async def get_alerts(
    current_owner=Depends(get_current_owner),
    session: AsyncSession = Depends(get_db_session),
) -> list[ActivityAlertRead]:
    await refresh_inactivity_alerts(session, current_owner.gym_id)
    alerts = await list_owner_alerts(session, current_owner.gym_id)
    return [ActivityAlertRead.model_validate(alert) for alert in alerts]


@router.get("/gym/settings", response_model=GymRead, summary="Get gym settings")
async def read_gym_settings(
    current_owner=Depends(get_current_owner),
    session: AsyncSession = Depends(get_db_session),
) -> GymRead:
    gym = await get_gym_settings(session, current_owner.gym_id)
    return GymRead.model_validate(gym)


@router.put("/gym/settings", response_model=GymRead, summary="Update gym settings")
async def patch_gym_settings(
    payload: GymSettingsUpdate,
    current_owner=Depends(get_current_owner),
    session: AsyncSession = Depends(get_db_session),
) -> GymRead:
    gym = await update_gym_settings(session, current_owner.gym_id, payload)
    return GymRead.model_validate(gym)

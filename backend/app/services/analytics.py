from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.member_profile import MemberProfile
from app.models.enums import UserRole
from app.models.user import User
from app.models.workout_log import WorkoutLog
from app.schemas.analytics import ActivityTrendPoint, GoalDistributionItem, RetentionAnalytics


async def get_retention_analytics(session: AsyncSession, gym_id) -> RetentionAnalytics:
    total_members = await session.scalar(
        select(func.count(User.id)).where(User.gym_id == gym_id, User.role == UserRole.MEMBER, User.is_active.is_(True))
    )
    last_week = datetime.now(UTC) - timedelta(days=7)
    active_member_ids = (
        await session.scalars(
            select(WorkoutLog.user_id)
            .join(User, User.id == WorkoutLog.user_id)
            .where(User.gym_id == gym_id, WorkoutLog.logged_at >= last_week)
            .distinct()
        )
    ).all()
    active_members = len(active_member_ids)
    inactive_members = max((total_members or 0) - active_members, 0)
    return RetentionAnalytics(active_members=active_members, inactive_members=inactive_members, at_risk_members=inactive_members)


async def get_goal_distribution(session: AsyncSession, gym_id) -> list[GoalDistributionItem]:
    rows = (
        await session.execute(
            select(MemberProfile.goal, func.count(MemberProfile.id))
            .join(User, User.id == MemberProfile.user_id)
            .where(User.gym_id == gym_id, User.is_active.is_(True))
            .group_by(MemberProfile.goal)
        )
    ).all()
    return [GoalDistributionItem(goal=goal.value, count=count) for goal, count in rows]


async def get_activity_trends(session: AsyncSession, gym_id) -> list[ActivityTrendPoint]:
    trend_points: list[ActivityTrendPoint] = []
    today = datetime.now(UTC).date()
    for index in range(4):
        start = today - timedelta(days=(index + 1) * 7)
        end = today - timedelta(days=index * 7)
        workout_count = await session.scalar(
            select(func.count(WorkoutLog.id))
            .join(User, User.id == WorkoutLog.user_id)
            .where(User.gym_id == gym_id, WorkoutLog.logged_at >= start, WorkoutLog.logged_at < end)
        )
        trend_points.append(ActivityTrendPoint(label=f"{start.isoformat()} to {end.isoformat()}", workout_count=workout_count or 0))
    trend_points.reverse()
    return trend_points

from pydantic import BaseModel


class RetentionAnalytics(BaseModel):
    active_members: int
    inactive_members: int
    at_risk_members: int


class GoalDistributionItem(BaseModel):
    goal: str
    count: int


class ActivityTrendPoint(BaseModel):
    label: str
    workout_count: int

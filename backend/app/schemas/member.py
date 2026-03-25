from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.enums import DietPreference, GoalType, MealType, SexType
from app.schemas.common import ORMModel


class MemberProfileUpsert(BaseModel):
    height_cm: float = Field(gt=0, le=300)
    weight_kg: float = Field(gt=0, le=500)
    goal: GoalType
    diet_preference: DietPreference
    date_of_birth: date | None = None
    sex: SexType | None = None


class MemberProfileRead(ORMModel):
    id: UUID
    user_id: UUID
    height_cm: float
    weight_kg: float
    goal: GoalType
    diet_preference: DietPreference
    date_of_birth: date | None
    sex: SexType | None
    created_at: datetime
    updated_at: datetime


class WorkoutExerciseRead(BaseModel):
    workout_id: UUID
    title: str
    description: str
    video_url: str | None
    muscle_group: str
    prescribed_sets: int
    prescribed_reps: int
    sort_order: int


class TodayWorkoutResponse(BaseModel):
    plan_date: date
    exercises: list[WorkoutExerciseRead]


class WorkoutLogCreate(BaseModel):
    workout_id: UUID
    sets: int = Field(gt=0, le=20)
    reps: int = Field(gt=0, le=200)
    weight_used: float | None = Field(default=None, ge=0, le=500)
    is_completed: bool = True


class WorkoutLogRead(ORMModel):
    id: UUID
    workout_id: UUID
    sets: int
    reps: int
    weight_used: float | None
    is_completed: bool
    logged_at: datetime


class DietMealRead(BaseModel):
    meal_type: MealType
    meal_name: str
    calories: float
    protein_g: float
    carbs_g: float
    fats_g: float


class TodayDietResponse(BaseModel):
    plan_date: date
    total_calories: float
    total_protein_g: float
    total_carbs_g: float
    total_fats_g: float
    meals: list[DietMealRead]

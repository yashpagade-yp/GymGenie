from datetime import UTC, date, datetime

from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.diet_plan import DietPlan
from app.models.enums import DietPreference, GoalType, MealType, SexType
from app.models.member_profile import MemberProfile
from app.models.member_workout_plan import MemberWorkoutPlan
from app.models.user import User
from app.models.workout import Workout
from app.schemas.member import DietMealRead, TodayDietResponse, TodayWorkoutResponse, WorkoutExerciseRead


def _calculate_age(date_of_birth: date | None) -> int:
    if date_of_birth is None:
        return 30
    today = date.today()
    return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))


def _calculate_daily_macros(profile: MemberProfile) -> tuple[float, float, float, float]:
    age = _calculate_age(profile.date_of_birth)
    sex_adjustment = 5 if profile.sex == SexType.MALE else -161 if profile.sex == SexType.FEMALE else -78
    bmr = (10 * profile.weight_kg) + (6.25 * profile.height_cm) - (5 * age) + sex_adjustment
    tdee = bmr * 1.55
    calorie_delta = {
        GoalType.LOSE: -500,
        GoalType.GAIN: 400,
        GoalType.MAINTAIN: 0,
    }[profile.goal]
    calories = max(tdee + calorie_delta, 1200)
    protein = round(profile.weight_kg * (2.0 if profile.goal == GoalType.GAIN else 1.8), 2)
    fats = round((calories * 0.25) / 9, 2)
    carbs = round((calories - (protein * 4 + fats * 9)) / 4, 2)
    return round(calories, 2), protein, max(carbs, 0), fats


async def get_or_create_workout_plan(session: AsyncSession, user: User, profile: MemberProfile, plan_date: date) -> TodayWorkoutResponse:
    rows = (
        await session.execute(
            select(MemberWorkoutPlan, Workout)
            .join(Workout, Workout.id == MemberWorkoutPlan.workout_id)
            .where(MemberWorkoutPlan.user_id == user.id, MemberWorkoutPlan.plan_date == plan_date)
            .order_by(MemberWorkoutPlan.sort_order.asc())
        )
    ).all()
    if not rows:
        workouts = (
            await session.scalars(
                select(Workout)
                .where(
                    Workout.goal_type == profile.goal,
                    or_(Workout.gym_id == user.gym_id, Workout.gym_id.is_(None)),
                )
                .order_by(Workout.created_at.asc())
                .limit(5)
            )
        ).all()
        for index, workout in enumerate(workouts):
            session.add(
                MemberWorkoutPlan(
                    user_id=user.id,
                    workout_id=workout.id,
                    plan_date=plan_date,
                    sort_order=index,
                    prescribed_sets=4 if profile.goal == GoalType.GAIN else 3,
                    prescribed_reps=12 if profile.goal == GoalType.LOSE else 10,
                )
            )
        await session.commit()
        rows = (
            await session.execute(
                select(MemberWorkoutPlan, Workout)
                .join(Workout, Workout.id == MemberWorkoutPlan.workout_id)
                .where(MemberWorkoutPlan.user_id == user.id, MemberWorkoutPlan.plan_date == plan_date)
                .order_by(MemberWorkoutPlan.sort_order.asc())
            )
        ).all()

    exercises = [
        WorkoutExerciseRead(
            workout_id=workout.id,
            title=workout.title,
            description=workout.description,
            video_url=workout.video_url,
            muscle_group=workout.muscle_group,
            prescribed_sets=plan.prescribed_sets,
            prescribed_reps=plan.prescribed_reps,
            sort_order=plan.sort_order,
        )
        for plan, workout in rows
    ]
    return TodayWorkoutResponse(plan_date=plan_date, exercises=exercises)


async def get_or_create_diet_plan(session: AsyncSession, user: User, profile: MemberProfile, plan_date: date) -> TodayDietResponse:
    meals = (
        await session.scalars(
            select(DietPlan)
            .where(DietPlan.user_id == user.id, DietPlan.plan_date == plan_date)
            .order_by(DietPlan.meal_type.asc())
        )
    ).all()
    if not meals:
        calories, protein, carbs, fats = _calculate_daily_macros(profile)
        meal_templates = _build_meal_templates(profile.goal, profile.diet_preference)
        meal_types = [MealType.BREAKFAST, MealType.LUNCH, MealType.SNACK, MealType.DINNER]
        for meal_type, meal_name in zip(meal_types, meal_templates, strict=True):
            session.add(
                DietPlan(
                    user_id=user.id,
                    plan_date=plan_date,
                    meal_type=meal_type,
                    meal_name=meal_name,
                    calories=round(calories / 4, 2),
                    protein_g=round(protein / 4, 2),
                    carbs_g=round(carbs / 4, 2),
                    fats_g=round(fats / 4, 2),
                    diet_preference=profile.diet_preference,
                    goal_type=profile.goal,
                )
            )
        await session.commit()
        meals = (
            await session.scalars(
                select(DietPlan)
                .where(DietPlan.user_id == user.id, DietPlan.plan_date == plan_date)
                .order_by(DietPlan.meal_type.asc())
            )
        ).all()

    meal_reads = [
        DietMealRead(
            meal_type=meal.meal_type,
            meal_name=meal.meal_name,
            calories=meal.calories,
            protein_g=meal.protein_g,
            carbs_g=meal.carbs_g,
            fats_g=meal.fats_g,
        )
        for meal in meals
    ]
    return TodayDietResponse(
        plan_date=plan_date,
        total_calories=round(sum(item.calories for item in meal_reads), 2),
        total_protein_g=round(sum(item.protein_g for item in meal_reads), 2),
        total_carbs_g=round(sum(item.carbs_g for item in meal_reads), 2),
        total_fats_g=round(sum(item.fats_g for item in meal_reads), 2),
        meals=meal_reads,
    )


def _build_meal_templates(goal: GoalType, diet_preference: DietPreference) -> list[str]:
    templates = {
        DietPreference.VEGETARIAN: {
            GoalType.LOSE: ["Oats and berries", "Paneer salad bowl", "Greek yogurt and nuts", "Lentil soup with sauteed vegetables"],
            GoalType.GAIN: ["Peanut butter oats", "Paneer rice bowl", "Banana smoothie", "Tofu curry with rice"],
            GoalType.MAINTAIN: ["Fruit muesli", "Dal khichdi bowl", "Roasted chana snack", "Vegetable quinoa plate"],
        },
        DietPreference.NON_VEGETARIAN: {
            GoalType.LOSE: ["Egg white oats", "Grilled chicken salad", "Greek yogurt and nuts", "Fish with steamed vegetables"],
            GoalType.GAIN: ["Egg and toast stack", "Chicken rice bowl", "Whey banana smoothie", "Lean beef with potatoes"],
            GoalType.MAINTAIN: ["Egg veggie wrap", "Chicken quinoa plate", "Fruit and yogurt", "Fish curry with rice"],
        },
    }
    return templates[diet_preference][goal]


def ensure_onboarded(profile: MemberProfile | None) -> MemberProfile:
    if profile is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Complete onboarding before accessing plans")
    return profile


def utcnow() -> datetime:
    return datetime.now(UTC)

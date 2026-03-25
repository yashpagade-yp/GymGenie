from enum import StrEnum


def enum_values(enum_cls: type[StrEnum]) -> list[str]:
    return [item.value for item in enum_cls]


class UserRole(StrEnum):
    MEMBER = "member"
    TRAINER = "trainer"
    OWNER = "owner"


class AuthProvider(StrEnum):
    EMAIL = "email"
    GOOGLE = "google"


class GoalType(StrEnum):
    LOSE = "lose"
    GAIN = "gain"
    MAINTAIN = "maintain"


class DietPreference(StrEnum):
    VEGETARIAN = "vegetarian"
    NON_VEGETARIAN = "non_vegetarian"


class DifficultyLevel(StrEnum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class MealType(StrEnum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    SNACK = "snack"
    DINNER = "dinner"


class AlertType(StrEnum):
    INACTIVE = "inactive"
    GOAL_STALLED = "goal_stalled"
    NEW_SIGNUP = "new_signup"
    STREAK_BROKEN = "streak_broken"


class SexType(StrEnum):
    FEMALE = "female"
    MALE = "male"

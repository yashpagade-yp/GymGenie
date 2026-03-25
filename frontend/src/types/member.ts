export interface MemberProfile {
  id: string;
  user_id: string;
  height_cm: number;
  weight_kg: number;
  goal: "lose" | "gain" | "maintain";
  diet_preference: "vegetarian" | "non_vegetarian";
  date_of_birth: string | null;
  sex: "male" | "female" | null;
  created_at: string;
  updated_at: string;
}

export interface WorkoutExercise {
  workout_id: string;
  title: string;
  description: string;
  video_url: string | null;
  muscle_group: string;
  prescribed_sets: number;
  prescribed_reps: number;
  sort_order: number;
}

export interface TodayWorkoutResponse {
  plan_date: string;
  exercises: WorkoutExercise[];
}

export interface WorkoutLog {
  id: string;
  workout_id: string;
  sets: number;
  reps: number;
  weight_used: number | null;
  is_completed: boolean;
  logged_at: string;
}

export interface DietMeal {
  meal_type: "breakfast" | "lunch" | "snack" | "dinner";
  meal_name: string;
  calories: number;
  protein_g: number;
  carbs_g: number;
  fats_g: number;
}

export interface TodayDietResponse {
  plan_date: string;
  total_calories: number;
  total_protein_g: number;
  total_carbs_g: number;
  total_fats_g: number;
  meals: DietMeal[];
}

export interface OnboardingPayload {
  height_cm: number;
  weight_kg: number;
  goal: "lose" | "gain" | "maintain";
  diet_preference: "vegetarian" | "non_vegetarian";
  date_of_birth?: string | null;
  sex?: "male" | "female" | null;
}

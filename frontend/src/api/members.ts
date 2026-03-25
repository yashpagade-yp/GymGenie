import type { MemberProfile, OnboardingPayload, TodayDietResponse, TodayWorkoutResponse, WorkoutLog } from "../types/member";
import type { Product } from "../types/product";
import { apiRequest } from "./client";

export function getMemberProfile() {
  return apiRequest<MemberProfile | null>("/members/profile");
}

export function saveMemberProfile(payload: OnboardingPayload) {
  return apiRequest<MemberProfile>("/members/profile", {
    method: "PUT",
    body: JSON.stringify(payload),
  });
}

export function createOnboarding(payload: OnboardingPayload) {
  return apiRequest<MemberProfile>("/members/onboarding", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getTodayWorkout() {
  return apiRequest<TodayWorkoutResponse>("/members/workouts/today");
}

export function getTodayDiet() {
  return apiRequest<TodayDietResponse>("/members/diet/today");
}

export function getWorkoutHistory() {
  return apiRequest<WorkoutLog[]>("/members/workouts/history");
}

export function logWorkout(payload: { workout_id: string; sets: number; reps: number; weight_used?: number; is_completed: boolean }) {
  return apiRequest<WorkoutLog>("/members/workouts/log", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getMemberProducts() {
  return apiRequest<Product[]>("/members/products");
}

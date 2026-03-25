import type { UserSummary } from "../types/auth";
import type { GymSettings, OwnerMemberDetail, RetentionAnalytics, GoalDistributionItem, ActivityTrendPoint } from "../types/owner";
import type { Product, ProductPayload } from "../types/product";
import type { ActivityAlert } from "../types/trainer";
import { apiRequest } from "./client";

export function getOwnerMembers() {
  return apiRequest<UserSummary[]>("/owners/members");
}

export function getOwnerMemberDetail(memberId: string) {
  return apiRequest<OwnerMemberDetail>(`/owners/members/${memberId}`);
}

export function getOwnerTrainers() {
  return apiRequest<UserSummary[]>("/owners/trainers");
}

export function createTrainer(payload: { email: string; full_name: string; password: string }) {
  return apiRequest<UserSummary>("/owners/trainers", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function assignTrainer(payload: { trainer_id: string; member_id: string }) {
  return apiRequest<void>("/owners/trainers/assign", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getOwnerProducts() {
  return apiRequest<Product[]>("/owners/products");
}

export function createProduct(payload: ProductPayload) {
  return apiRequest<Product>("/owners/products", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function updateProduct(productId: string, payload: Partial<ProductPayload>) {
  return apiRequest<Product>(`/owners/products/${productId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export function getOwnerAlerts() {
  return apiRequest<ActivityAlert[]>("/owners/alerts");
}

export function getGymSettings() {
  return apiRequest<GymSettings>("/owners/gym/settings");
}

export function updateGymSettings(payload: Partial<Pick<GymSettings, "name" | "address" | "logo_url">>) {
  return apiRequest<GymSettings>("/owners/gym/settings", {
    method: "PUT",
    body: JSON.stringify(payload),
  });
}

export function getRetentionAnalytics() {
  return apiRequest<RetentionAnalytics>("/owners/analytics/retention");
}

export function getGoalDistribution() {
  return apiRequest<GoalDistributionItem[]>("/owners/analytics/goals");
}

export function getActivityAnalytics() {
  return apiRequest<ActivityTrendPoint[]>("/owners/analytics/activity");
}

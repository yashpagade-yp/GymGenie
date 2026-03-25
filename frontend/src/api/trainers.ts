import type { ActivityAlert, TrainerAssignedMember, TrainerMemberDetail, TrainerNote } from "../types/trainer";
import { apiRequest } from "./client";

export function getAssignedMembers() {
  return apiRequest<TrainerAssignedMember[]>("/trainers/members/assigned");
}

export function getTrainerMemberDetail(memberId: string) {
  return apiRequest<TrainerMemberDetail>(`/trainers/members/${memberId}`);
}

export function getTrainerAlerts() {
  return apiRequest<ActivityAlert[]>("/trainers/alerts");
}

export function getTrainerNotes(memberId: string) {
  return apiRequest<TrainerNote[]>(`/trainers/members/${memberId}/notes`);
}

export function createTrainerNote(memberId: string, note: string) {
  return apiRequest<TrainerNote>(`/trainers/members/${memberId}/notes`, {
    method: "POST",
    body: JSON.stringify({ note }),
  });
}

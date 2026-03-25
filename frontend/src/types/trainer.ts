import type { MemberProfile, WorkoutLog } from "./member";

export interface TrainerAssignedMember {
  user_id: string;
  full_name: string;
  email: string;
  goal: "lose" | "gain" | "maintain" | null;
  diet_preference: "vegetarian" | "non_vegetarian" | null;
  last_workout_at: string | null;
  workouts_completed: number;
  is_at_risk: boolean;
}

export interface TrainerMemberDetail {
  member: TrainerAssignedMember;
  profile: MemberProfile | null;
  recent_workouts: WorkoutLog[];
}

export interface TrainerNote {
  id: string;
  trainer_id: string;
  member_id: string;
  note: string;
  created_at: string;
  updated_at: string;
}

export interface ActivityAlert {
  id: string;
  user_id: string;
  gym_id: string;
  alert_type: "inactive" | "goal_stalled" | "new_signup" | "streak_broken";
  message: string;
  is_read: boolean;
  created_at: string;
  updated_at: string;
}

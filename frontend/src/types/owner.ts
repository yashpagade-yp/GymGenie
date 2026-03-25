import type { MemberProfile, WorkoutLog } from "./member";
import type { ActivityAlert } from "./trainer";
import type { UserSummary } from "./auth";

export interface OwnerMemberDetail {
  member: UserSummary;
  profile: MemberProfile | null;
  recent_workouts: WorkoutLog[];
  assigned_trainer_ids: string[];
}

export interface GymSettings {
  id: string;
  name: string;
  address: string;
  logo_url: string | null;
  invite_code: string | null;
  created_at: string;
  updated_at: string;
}

export interface RetentionAnalytics {
  active_members: number;
  inactive_members: number;
  at_risk_members: number;
}

export interface GoalDistributionItem {
  goal: string;
  count: number;
}

export interface ActivityTrendPoint {
  label: string;
  workout_count: number;
}

export interface OwnerDashboardData {
  alerts: ActivityAlert[];
  retention: RetentionAnalytics;
  goals: GoalDistributionItem[];
  activity: ActivityTrendPoint[];
}

export type UserRole = "member" | "trainer" | "owner";

export interface UserSummary {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  gym_id: string;
  auth_provider: "email" | "google";
  is_active: boolean;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: UserSummary;
}

export interface GoogleAuthConfig {
  enabled: boolean;
  client_id: string | null;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface RegisterPayload {
  email: string;
  password: string;
  full_name: string;
  invite_code: string;
}

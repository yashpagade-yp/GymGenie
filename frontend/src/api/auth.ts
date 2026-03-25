import type { AuthResponse, GoogleAuthConfig, LoginPayload, RegisterPayload, UserSummary } from "../types/auth";
import { apiRequest } from "./client";

export function login(payload: LoginPayload) {
  return apiRequest<AuthResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function register(payload: RegisterPayload) {
  return apiRequest<AuthResponse>("/auth/register", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function currentUser() {
  return apiRequest<UserSummary>("/auth/me");
}

export function getGoogleAuthConfig() {
  return apiRequest<GoogleAuthConfig>("/auth/google/config");
}

export function loginWithGoogle(idToken: string, inviteCode?: string) {
  const normalizedInviteCode = inviteCode?.trim().toUpperCase();
  return apiRequest<AuthResponse>("/auth/google", {
    method: "POST",
    body: JSON.stringify({
      id_token: idToken,
      ...(normalizedInviteCode ? { invite_code: normalizedInviteCode } : {}),
    }),
  });
}

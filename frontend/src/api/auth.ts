import type {
  AuthResponse,
  ForgotPasswordPayload,
  GoogleAuthConfig,
  LoginPayload,
  PasswordResetResponse,
  RegisterPayload,
  ResetPasswordPayload,
  UserSummary,
} from "../types/auth";
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

export function requestPasswordReset(payload: ForgotPasswordPayload) {
  return apiRequest<PasswordResetResponse>("/auth/forgot-password", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function resetPassword(payload: ResetPasswordPayload) {
  return apiRequest<PasswordResetResponse>("/auth/reset-password", {
    method: "POST",
    body: JSON.stringify(payload),
  });
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

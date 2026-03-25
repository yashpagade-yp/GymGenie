const ACCESS_TOKEN_KEY = "gymgenie.accessToken";
const REFRESH_TOKEN_KEY = "gymgenie.refreshToken";
const USER_KEY = "gymgenie.user";

export function setStoredAuth(accessToken: string, refreshToken: string, user: string) {
  localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
  localStorage.setItem(USER_KEY, user);
}

export function getStoredAccessToken() {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function getStoredRefreshToken() {
  return localStorage.getItem(REFRESH_TOKEN_KEY);
}

export function getStoredUser() {
  return localStorage.getItem(USER_KEY);
}

export function clearStoredAuth() {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

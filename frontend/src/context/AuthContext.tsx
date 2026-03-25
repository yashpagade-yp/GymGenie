import { createContext, startTransition, useEffect, useState } from "react";

import { currentUser, login, loginWithGoogle, register } from "../api/auth";
import type { AuthResponse, LoginPayload, RegisterPayload, UserSummary } from "../types/auth";
import { clearStoredAuth, getStoredAccessToken, getStoredUser, setStoredAuth } from "../utils/storage";

interface AuthContextValue {
  user: UserSummary | null;
  isReady: boolean;
  loginUser: (payload: LoginPayload) => Promise<AuthResponse>;
  registerUser: (payload: RegisterPayload) => Promise<AuthResponse>;
  googleLoginUser: (idToken: string, inviteCode?: string) => Promise<AuthResponse>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

export const AuthContext = createContext<AuthContextValue | null>(null);

function persistAuth(response: AuthResponse) {
  setStoredAuth(response.access_token, response.refresh_token, JSON.stringify(response.user));
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<UserSummary | null>(() => {
    const stored = getStoredUser();
    return stored ? (JSON.parse(stored) as UserSummary) : null;
  });
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    const token = getStoredAccessToken();

    if (!token) {
      setIsReady(true);
      return;
    }

    void currentUser()
      .then((resolvedUser) => {
        startTransition(() => {
          setUser(resolvedUser);
        });
      })
      .catch(() => {
        clearStoredAuth();
        setUser(null);
      })
      .finally(() => {
        setIsReady(true);
      });
  }, []);

  async function loginUser(payload: LoginPayload) {
    const response = await login(payload);
    persistAuth(response);
    setUser(response.user);
    return response;
  }

  async function registerUser(payload: RegisterPayload) {
    const response = await register(payload);
    persistAuth(response);
    setUser(response.user);
    return response;
  }

  async function googleLoginUser(idToken: string, inviteCode?: string) {
    const response = await loginWithGoogle(idToken, inviteCode);
    persistAuth(response);
    setUser(response.user);
    return response;
  }

  function logout() {
    clearStoredAuth();
    setUser(null);
  }

  async function refreshUser() {
    const resolvedUser = await currentUser();
    setUser(resolvedUser);
    setStoredAuth(getStoredAccessToken() ?? "", localStorage.getItem("gymgenie.refreshToken") ?? "", JSON.stringify(resolvedUser));
  }

  return (
    <AuthContext.Provider value={{ user, isReady, loginUser, registerUser, googleLoginUser, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
}

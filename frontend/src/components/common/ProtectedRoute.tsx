import { Navigate, useLocation } from "react-router-dom";

import { useAuth } from "../../hooks/useAuth";
import type { UserRole } from "../../types/auth";

export function ProtectedRoute({
  children,
  roles,
}: {
  children: React.ReactNode;
  roles?: UserRole[];
}) {
  const { isReady, user } = useAuth();
  const location = useLocation();

  if (!isReady) {
    return <div className="screen-state">Loading your training zone...</div>;
  }

  if (!user) {
    return <Navigate replace state={{ from: location.pathname }} to="/login" />;
  }

  if (roles && !roles.includes(user.role)) {
    return <Navigate replace to="/dashboard" />;
  }

  return <>{children}</>;
}

import { Navigate, Route, Routes } from "react-router-dom";

import { ProtectedRoute } from "./components/common/ProtectedRoute";
import { AppShell } from "./components/common/AppShell";
import { useAuth } from "./hooks/useAuth";
import { LandingPage } from "./pages/LandingPage";
import { LoginPage } from "./pages/LoginPage";
import { MemberDashboardPage } from "./pages/MemberDashboardPage";
import { OnboardingPage } from "./pages/OnboardingPage";
import { OwnerDashboardPage } from "./pages/OwnerDashboardPage";
import { RegisterPage } from "./pages/RegisterPage";
import { TrainerDashboardPage } from "./pages/TrainerDashboardPage";

function DashboardRedirect() {
  const { user } = useAuth();

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (user.role === "member") {
    return <Navigate to="/dashboard/member" replace />;
  }

  if (user.role === "trainer") {
    return <Navigate to="/dashboard/trainer" replace />;
  }

  return <Navigate to="/dashboard/owner" replace />;
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route
        path="/onboarding"
        element={
          <ProtectedRoute roles={["member"]}>
            <OnboardingPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/dashboard/member"
        element={
          <ProtectedRoute roles={["member"]}>
            <AppShell>
              <MemberDashboardPage />
            </AppShell>
          </ProtectedRoute>
        }
      />
      <Route
        path="/dashboard/trainer"
        element={
          <ProtectedRoute roles={["trainer"]}>
            <AppShell>
              <TrainerDashboardPage />
            </AppShell>
          </ProtectedRoute>
        }
      />
      <Route
        path="/dashboard/owner"
        element={
          <ProtectedRoute roles={["owner"]}>
            <AppShell>
              <OwnerDashboardPage />
            </AppShell>
          </ProtectedRoute>
        }
      />
      <Route path="/dashboard" element={<DashboardRedirect />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

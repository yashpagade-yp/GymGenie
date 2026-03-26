import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";

import { ApiError } from "../api/client";
import { AuthCard } from "../components/auth/AuthCard";
import { GoogleAuthButton } from "../components/auth/GoogleAuthButton";
import { useAuth } from "../hooks/useAuth";

export function LoginPage() {
  const { loginUser } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  function navigateByRole(role: "member" | "trainer" | "owner") {
    const target = role === "member" ? "/dashboard/member" : role === "trainer" ? "/dashboard/trainer" : "/dashboard/owner";
    navigate((location.state as { from?: string } | null)?.from ?? target, { replace: true });
  }

  async function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setIsSubmitting(true);
    const formData = new FormData(event.currentTarget);

    try {
      const response = await loginUser({
        email: String(formData.get("email")),
        password: String(formData.get("password")),
      });
      navigateByRole(response.user.role);
    } catch (requestError) {
      setError(requestError instanceof ApiError ? requestError.message : "Unable to login.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="auth-page">
      <AuthCard title="Welcome back" subtitle="Login for member training, trainer CRM, or owner control.">
        <form className="auth-form" onSubmit={onSubmit}>
          <input name="email" placeholder="Email address" required type="email" />
          <input name="password" placeholder="Password" required type="password" />
          <div className="auth-inline-row">
            <span className="muted">Use your assigned account credentials.</span>
            <Link className="inline-link" to="/forgot-password">
              Forgot password?
            </Link>
          </div>
          {error ? <p className="error-text">{error}</p> : null}
          <button className="primary-button" disabled={isSubmitting} type="submit">
            {isSubmitting ? "Signing in..." : "Login"}
          </button>
        </form>
        <div className="auth-divider"><span>or continue with Google</span></div>
        <GoogleAuthButton label="signin" onSuccessNavigate={navigateByRole} />
        <p className="muted">
          Member sign up lives here. Owners and trainers use their existing account. <Link to="/register">Register as member</Link>
        </p>
      </AuthCard>
    </main>
  );
}

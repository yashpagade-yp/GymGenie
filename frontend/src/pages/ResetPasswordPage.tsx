import { useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";

import { resetPassword } from "../api/auth";
import { ApiError } from "../api/client";
import { AuthCard } from "../components/auth/AuthCard";

export function ResetPasswordPage() {
  const [searchParams] = useSearchParams();
  const initialToken = useMemo(() => searchParams.get("token") ?? "", [searchParams]);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setMessage(null);
    setIsSubmitting(true);
    const formData = new FormData(event.currentTarget);
    const password = String(formData.get("password"));
    const confirmPassword = String(formData.get("confirmPassword"));

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      setIsSubmitting(false);
      return;
    }

    try {
      const response = await resetPassword({
        token: String(formData.get("token")),
        password,
      });
      setMessage(response.message);
      event.currentTarget.reset();
    } catch (requestError) {
      setError(requestError instanceof ApiError ? requestError.message : "Unable to reset password.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="auth-page">
      <AuthCard
        title="Choose a new password"
        subtitle="Use the reset link token and set a new password with at least 8 characters."
      >
        <form className="auth-form" onSubmit={onSubmit}>
          <input defaultValue={initialToken} name="token" placeholder="Reset token" required type="text" />
          <input name="password" placeholder="New password" required type="password" />
          <input name="confirmPassword" placeholder="Confirm new password" required type="password" />
          {error ? <p className="error-text">{error}</p> : null}
          {message ? <p className="success-text">{message}</p> : null}
          <button className="primary-button" disabled={isSubmitting} type="submit">
            {isSubmitting ? "Updating..." : "Update password"}
          </button>
        </form>
        <p className="muted">
          Back to sign in. <Link to="/login">Login</Link>
        </p>
      </AuthCard>
    </main>
  );
}

import { useState } from "react";
import { Link } from "react-router-dom";

import { requestPasswordReset } from "../api/auth";
import { ApiError } from "../api/client";
import { AuthCard } from "../components/auth/AuthCard";

export function ForgotPasswordPage() {
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [resetUrl, setResetUrl] = useState<string | null>(null);

  async function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setMessage(null);
    setResetUrl(null);
    setIsSubmitting(true);
    const formData = new FormData(event.currentTarget);

    try {
      const response = await requestPasswordReset({
        email: String(formData.get("email")),
      });
      setMessage(response.message);
      setResetUrl(response.reset_url ?? null);
    } catch (requestError) {
      setError(requestError instanceof ApiError ? requestError.message : "Unable to request password reset.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="auth-page">
      <AuthCard
        title="Reset your password"
        subtitle="Enter the email tied to your GymGenie account. In local development, the reset link will be shown directly here."
      >
        <form className="auth-form" onSubmit={onSubmit}>
          <input name="email" placeholder="Email address" required type="email" />
          {error ? <p className="error-text">{error}</p> : null}
          <button className="primary-button" disabled={isSubmitting} type="submit">
            {isSubmitting ? "Sending..." : "Send reset link"}
          </button>
        </form>
        {message ? (
          <section className="success-card">
            <p className="success-text">{message}</p>
            {resetUrl ? (
              <>
                <a className="ghost-button" href={resetUrl}>
                  Open reset page
                </a>
                <input readOnly type="text" value={resetUrl} />
              </>
            ) : null}
          </section>
        ) : null}
        <p className="muted">
          Back to sign in. <Link to="/login">Login</Link>
        </p>
      </AuthCard>
    </main>
  );
}

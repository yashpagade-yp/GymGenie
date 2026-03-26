import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { ApiError } from "../api/client";
import { AuthCard } from "../components/auth/AuthCard";
import { GoogleAuthButton } from "../components/auth/GoogleAuthButton";
import { PasswordField } from "../components/auth/PasswordField";
import { useAuth } from "../hooks/useAuth";

export function RegisterPage() {
  const { googleLoginUser, registerUser } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const [googleError, setGoogleError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [inviteCode, setInviteCode] = useState("");
  const [googleInviteCode, setGoogleInviteCode] = useState("");
  const [pendingGoogleCredential, setPendingGoogleCredential] = useState<string | null>(null);
  const [isCompletingGoogleSignup, setIsCompletingGoogleSignup] = useState(false);

  function navigateByRole(role: "member" | "trainer" | "owner") {
    const target = role === "member" ? "/dashboard/member" : role === "trainer" ? "/dashboard/trainer" : "/dashboard/owner";
    navigate(target, { replace: true });
  }

  async function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setIsSubmitting(true);
    const formData = new FormData(event.currentTarget);

    try {
      await registerUser({
        email: String(formData.get("email")),
        password: String(formData.get("password")),
        full_name: String(formData.get("full_name")),
        invite_code: String(formData.get("invite_code")).trim().toUpperCase(),
      });
      navigate("/onboarding", { replace: true });
    } catch (requestError) {
      setError(requestError instanceof ApiError ? requestError.message : "Unable to register.");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function onCompleteGoogleSignup(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!pendingGoogleCredential) {
      return;
    }

    setGoogleError(null);
    setIsCompletingGoogleSignup(true);

    try {
      const response = await googleLoginUser(pendingGoogleCredential, googleInviteCode.trim().toUpperCase());
      navigateByRole(response.user.role);
    } catch (requestError) {
      setGoogleError(requestError instanceof ApiError ? requestError.message : "Unable to finish Google sign-up.");
    } finally {
      setIsCompletingGoogleSignup(false);
    }
  }

  return (
    <main className="auth-page">
      <AuthCard title="Create member account" subtitle="Register with email, or use Google and connect your gym in the next step if needed.">
        <form className="auth-form" onSubmit={onSubmit}>
          <input name="full_name" placeholder="Full name" required />
          <input name="email" placeholder="Email address" required type="email" />
          <PasswordField name="password" placeholder="Password" required />
          <input
            name="invite_code"
            onChange={(event) => setInviteCode(event.target.value)}
            placeholder="Gym invite code"
            required
            value={inviteCode}
          />
          {error ? <p className="error-text">{error}</p> : null}
          <button className="primary-button" disabled={isSubmitting} type="submit">
            {isSubmitting ? "Creating account..." : "Register"}
          </button>
        </form>
        <div className="auth-divider"><span>or continue with Google</span></div>
        <div className="google-signup-section">
          <p className="muted">
            Use your Google account first. If this is your first time joining a gym on GymGenie, we will ask for your gym invite code after Google verifies your email.
          </p>
          <GoogleAuthButton
            label="signup"
            onInviteCodeRequired={(credential, message) => {
              setPendingGoogleCredential(credential);
              setGoogleError(message);
            }}
            onSuccessNavigate={navigateByRole}
          />
          {pendingGoogleCredential ? (
            <form className="auth-form google-followup-form" onSubmit={onCompleteGoogleSignup}>
              <div className="google-followup-copy">
                <strong>Finish Google sign-up</strong>
                <p className="muted">Your Google account is verified. Enter your gym invite code to connect this new account to the correct gym.</p>
              </div>
              <input
                name="google_invite_code"
                onChange={(event) => setGoogleInviteCode(event.target.value)}
                placeholder="Gym invite code"
                required
                value={googleInviteCode}
              />
              {googleError ? <p className="error-text">{googleError}</p> : null}
              <button className="primary-button" disabled={isCompletingGoogleSignup} type="submit">
                {isCompletingGoogleSignup ? "Connecting gym..." : "Finish with Google"}
              </button>
            </form>
          ) : null}
        </div>
        <p className="muted">Already have access? <Link to="/login">Login</Link></p>
      </AuthCard>
    </main>
  );
}

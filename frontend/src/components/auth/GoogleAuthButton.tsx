import { useEffect, useId, useState } from "react";

import { getGoogleAuthConfig } from "../../api/auth";
import { ApiError } from "../../api/client";
import { useAuth } from "../../hooks/useAuth";
import { loadGoogleIdentityScript } from "../../utils/google";

export function GoogleAuthButton({
  label,
  onSuccessNavigate,
  inviteCode,
  onInviteCodeRequired,
}: {
  label: "signin" | "signup";
  onSuccessNavigate: (role: "member" | "trainer" | "owner") => void;
  inviteCode?: string;
  onInviteCodeRequired?: (credential: string, message: string) => void;
}) {
  const { googleLoginUser } = useAuth();
  const buttonId = useId();
  const normalizedInviteCode = inviteCode?.trim().toUpperCase();
  const [error, setError] = useState<string | null>(null);
  const [isUnavailable, setIsUnavailable] = useState(false);

  useEffect(() => {
    let isMounted = true;

    async function setupGoogleButton() {
      try {
        const config = await getGoogleAuthConfig();
        if (!config.enabled || !config.client_id) {
          if (isMounted) {
            setIsUnavailable(true);
          }
          return;
        }

        await loadGoogleIdentityScript();
        if (!isMounted || !window.google?.accounts?.id) {
          return;
        }

        const target = document.getElementById(buttonId);
        if (!target) {
          return;
        }

        target.innerHTML = "";
        window.google.accounts.id.initialize({
          client_id: config.client_id,
          callback: async (response) => {
            if (!response.credential) {
              setError("Google did not return a credential.");
              return;
            }

            try {
              const auth = await googleLoginUser(response.credential, normalizedInviteCode);
              onSuccessNavigate(auth.user.role);
            } catch (requestError) {
              if (requestError instanceof ApiError) {
                const needsInviteCode =
                  label === "signup" &&
                  requestError.status === 403 &&
                  requestError.message.toLowerCase().includes("invite code");
                if (needsInviteCode) {
                  setError(null);
                  onInviteCodeRequired?.(response.credential, requestError.message);
                  return;
                }
                setError(requestError.message);
                return;
              }
              setError("Google sign-in failed.");
            }
          },
        });
        window.google.accounts.id.renderButton(target, {
          theme: "outline",
          size: "large",
          shape: "pill",
          text: label === "signup" ? "signup_with" : "signin_with",
          width: 320,
        });
      } catch (requestError) {
        if (isMounted) {
          setError(requestError instanceof Error ? requestError.message : "Unable to initialize Google sign-in.");
        }
      }
    }

    void setupGoogleButton();

    return () => {
      isMounted = false;
    };
  }, [buttonId, googleLoginUser, label, normalizedInviteCode, onInviteCodeRequired, onSuccessNavigate]);

  if (isUnavailable) {
    return null;
  }

  return (
    <div className="google-auth-block">
      <div id={buttonId} />
      {error ? <p className="error-text">{error}</p> : null}
    </div>
  );
}

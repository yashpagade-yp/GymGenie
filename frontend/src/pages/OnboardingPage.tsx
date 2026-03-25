import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { ApiError } from "../api/client";
import { createOnboarding } from "../api/members";

export function OnboardingPage() {
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setIsSubmitting(true);
    const formData = new FormData(event.currentTarget);

    try {
      await createOnboarding({
        height_cm: Number(formData.get("height_cm")),
        weight_kg: Number(formData.get("weight_kg")),
        goal: String(formData.get("goal")) as "lose" | "gain" | "maintain",
        diet_preference: String(formData.get("diet_preference")) as "vegetarian" | "non_vegetarian",
        date_of_birth: String(formData.get("date_of_birth")) || null,
        sex: (String(formData.get("sex")) || null) as "male" | "female" | null,
      });
      navigate("/dashboard/member", { replace: true });
    } catch (requestError) {
      setError(requestError instanceof ApiError ? requestError.message : "Unable to save onboarding.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-card wide">
        <p className="eyebrow">Member Onboarding</p>
        <h1>Build your baseline</h1>
        <p className="muted">We use this to shape your daily workout and diet plan.</p>
        <form className="auth-form two-column" onSubmit={onSubmit}>
          <input min="100" name="height_cm" placeholder="Height (cm)" required type="number" />
          <input min="30" name="weight_kg" placeholder="Weight (kg)" required type="number" />
          <select defaultValue="gain" name="goal">
            <option value="lose">Lose weight</option>
            <option value="gain">Gain weight</option>
            <option value="maintain">Maintain weight</option>
          </select>
          <select defaultValue="non_vegetarian" name="diet_preference">
            <option value="vegetarian">Vegetarian</option>
            <option value="non_vegetarian">Non-vegetarian</option>
          </select>
          <input name="date_of_birth" type="date" />
          <select defaultValue="male" name="sex">
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
          {error ? <p className="error-text span-full">{error}</p> : null}
          <button className="primary-button span-full" disabled={isSubmitting} type="submit">
            {isSubmitting ? "Saving..." : "Finish onboarding"}
          </button>
        </form>
      </section>
    </main>
  );
}

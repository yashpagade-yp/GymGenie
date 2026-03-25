import { useEffect, useState } from "react";

import { ApiError } from "../api/client";
import {
  getMemberProducts,
  getMemberProfile,
  getTodayDiet,
  getTodayWorkout,
  getWorkoutHistory,
  logWorkout,
  saveMemberProfile,
} from "../api/members";
import { DietPanel } from "../components/member/DietPanel";
import { ProductPanel } from "../components/member/ProductPanel";
import { WorkoutPanel } from "../components/member/WorkoutPanel";
import { useAuth } from "../hooks/useAuth";
import type { MemberProfile, TodayDietResponse, TodayWorkoutResponse, WorkoutLog } from "../types/member";
import type { Product } from "../types/product";

export function MemberDashboardPage() {
  const { user } = useAuth();
  const [profile, setProfile] = useState<MemberProfile | null>(null);
  const [workout, setWorkout] = useState<TodayWorkoutResponse | null>(null);
  const [diet, setDiet] = useState<TodayDietResponse | null>(null);
  const [history, setHistory] = useState<WorkoutLog[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function refreshDashboard() {
    setError(null);
    setIsLoading(true);
    try {
      const [nextProfile, nextWorkout, nextDiet, nextHistory, nextProducts] = await Promise.all([
        getMemberProfile(),
        getTodayWorkout(),
        getTodayDiet(),
        getWorkoutHistory(),
        getMemberProducts(),
      ]);
      setProfile(nextProfile);
      setWorkout(nextWorkout);
      setDiet(nextDiet);
      setHistory(nextHistory);
      setProducts(nextProducts);
    } catch (requestError) {
      setError(requestError instanceof ApiError ? requestError.message : "Unable to load your member dashboard.");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    void refreshDashboard();
  }, []);

  async function onLogWorkout(workoutId: string) {
    await logWorkout({ workout_id: workoutId, sets: 3, reps: 10, weight_used: 20, is_completed: true });
    const nextHistory = await getWorkoutHistory();
    setHistory(nextHistory);
  }

  async function onSaveProfile(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    try {
      const nextProfile = await saveMemberProfile({
        height_cm: Number(formData.get("height_cm")),
        weight_kg: Number(formData.get("weight_kg")),
        goal: String(formData.get("goal")) as "lose" | "gain" | "maintain",
        diet_preference: String(formData.get("diet_preference")) as "vegetarian" | "non_vegetarian",
        date_of_birth: String(formData.get("date_of_birth")) || null,
        sex: (String(formData.get("sex")) || null) as "male" | "female" | null,
      });
      setProfile(nextProfile);
    } catch (requestError) {
      setError(requestError instanceof ApiError ? requestError.message : "Unable to update profile.");
    }
  }

  if (isLoading) {
    return <div className="screen-state">Loading member dashboard...</div>;
  }

  return (
    <div className="dashboard-grid member-dashboard">
      <section className="panel-card hero-dashboard member-hero">
        <p className="eyebrow">Member Mode</p>
        <h1>{user?.full_name}</h1>
        <p className="muted">
          Goal: {profile?.goal ?? "Not set"} | Diet: {profile?.diet_preference ?? "Not set"} | Logged workouts: {history.length}
        </p>
        {error ? <p className="error-text">{error}</p> : null}
        <div className="member-overview-strip">
          <div className="member-overview-card">
            <span>Goal</span>
            <strong>{profile?.goal ?? "Pending"}</strong>
          </div>
          <div className="member-overview-card">
            <span>Diet</span>
            <strong>{profile?.diet_preference ?? "Pending"}</strong>
          </div>
          <div className="member-overview-card">
            <span>Height / Weight</span>
            <strong>{profile ? `${profile.height_cm} cm / ${profile.weight_kg} kg` : "Pending"}</strong>
          </div>
          <div className="member-overview-card">
            <span>Sessions</span>
            <strong>{history.length}</strong>
          </div>
        </div>
      </section>

      <div className="member-main-column">
        <WorkoutPanel onLog={onLogWorkout} workout={workout} />
        <DietPanel diet={diet} />
      </div>

      <div className="member-side-column">
        <section className="panel-card member-profile-panel">
          <p className="eyebrow">Profile Settings</p>
          <h2>Update your baseline</h2>
          <p className="muted">Keep your metrics current so your plans stay relevant.</p>
          <form className="auth-form two-column" onSubmit={onSaveProfile}>
            <input defaultValue={profile?.height_cm ?? ""} min="100" name="height_cm" placeholder="Height (cm)" required type="number" />
            <input defaultValue={profile?.weight_kg ?? ""} min="30" name="weight_kg" placeholder="Weight (kg)" required type="number" />
            <select defaultValue={profile?.goal ?? "gain"} name="goal">
              <option value="lose">Lose weight</option>
              <option value="gain">Gain weight</option>
              <option value="maintain">Maintain weight</option>
            </select>
            <select defaultValue={profile?.diet_preference ?? "non_vegetarian"} name="diet_preference">
              <option value="vegetarian">Vegetarian</option>
              <option value="non_vegetarian">Non-vegetarian</option>
            </select>
            <input defaultValue={profile?.date_of_birth ?? ""} name="date_of_birth" type="date" />
            <select defaultValue={profile?.sex ?? "male"} name="sex">
              <option value="male">Male</option>
              <option value="female">Female</option>
            </select>
            <button className="primary-button span-full" type="submit">
              Save profile
            </button>
          </form>
        </section>

        <section className="panel-card member-history-panel">
          <p className="eyebrow">Recent Sessions</p>
          <h2>Workout history</h2>
          <div className="stack compact">
            {history.slice(0, 8).map((log) => (
              <div className="timeline-item" key={log.id}>
                <strong>{new Date(log.logged_at).toLocaleDateString()}</strong>
                <span>
                  {log.sets} x {log.reps} reps {log.weight_used ? `at ${log.weight_used} kg` : ""}
                </span>
              </div>
            ))}
          </div>
        </section>
      </div>

      <section className="member-products-row">
        <ProductPanel products={products} />
      </section>
    </div>
  );
}

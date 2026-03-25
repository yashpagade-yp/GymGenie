import { useEffect, useState } from "react";

import { ApiError } from "../api/client";
import {
  assignTrainer,
  createProduct,
  createTrainer,
  getActivityAnalytics,
  getGoalDistribution,
  getGymSettings,
  getOwnerAlerts,
  getOwnerMemberDetail,
  getOwnerMembers,
  getOwnerProducts,
  getOwnerTrainers,
  getRetentionAnalytics,
  updateGymSettings,
} from "../api/owners";
import { OwnerBoard } from "../components/owner/OwnerBoard";
import type { UserSummary } from "../types/auth";
import type { ActivityTrendPoint, GoalDistributionItem, GymSettings, OwnerMemberDetail, RetentionAnalytics } from "../types/owner";
import type { Product } from "../types/product";
import type { ActivityAlert } from "../types/trainer";

export function OwnerDashboardPage() {
  const [members, setMembers] = useState<UserSummary[]>([]);
  const [trainers, setTrainers] = useState<UserSummary[]>([]);
  const [selectedMember, setSelectedMember] = useState<OwnerMemberDetail | null>(null);
  const [products, setProducts] = useState<Product[]>([]);
  const [gym, setGym] = useState<GymSettings | null>(null);
  const [alerts, setAlerts] = useState<ActivityAlert[]>([]);
  const [retention, setRetention] = useState<RetentionAnalytics | null>(null);
  const [goals, setGoals] = useState<GoalDistributionItem[]>([]);
  const [activity, setActivity] = useState<ActivityTrendPoint[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function refreshBoard() {
    setError(null);
    setIsLoading(true);
    try {
      const [nextMembers, nextTrainers, nextProducts, nextGym, nextAlerts, nextRetention, nextGoals, nextActivity] =
        await Promise.all([
          getOwnerMembers(),
          getOwnerTrainers(),
          getOwnerProducts(),
          getGymSettings(),
          getOwnerAlerts(),
          getRetentionAnalytics(),
          getGoalDistribution(),
          getActivityAnalytics(),
        ]);

      setMembers(nextMembers);
      setTrainers(nextTrainers);
      setProducts(nextProducts);
      setGym(nextGym);
      setAlerts(nextAlerts);
      setRetention(nextRetention);
      setGoals(nextGoals);
      setActivity(nextActivity);
    } catch (requestError) {
      setError(requestError instanceof ApiError ? requestError.message : "Unable to load owner control center.");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    void refreshBoard();
  }, []);

  async function onSelectMember(memberId: string) {
    const detail = await getOwnerMemberDetail(memberId);
    setSelectedMember(detail);
  }

  async function onCreateTrainer(payload: { email: string; full_name: string; password: string }) {
    await createTrainer(payload);
    await refreshBoard();
  }

  async function onAssignTrainer(payload: { trainer_id: string; member_id: string }) {
    await assignTrainer(payload);
    await refreshBoard();
    await onSelectMember(payload.member_id);
  }

  async function onCreateProduct(payload: { name: string; description: string; price: number }) {
    await createProduct(payload);
    await refreshBoard();
  }

  async function onUpdateGym(payload: { name?: string; address?: string; logo_url?: string | null }) {
    await updateGymSettings(payload);
    await refreshBoard();
  }

  if (isLoading) {
    return <div className="screen-state">Loading owner control center...</div>;
  }

  return (
    <>
      {error ? <div className="panel-card"><p className="error-text">{error}</p></div> : null}
      <OwnerBoard
        activity={activity}
        alerts={alerts}
        goals={goals}
        gym={gym}
        members={members}
        onAssignTrainer={onAssignTrainer}
        onCreateProduct={onCreateProduct}
        onCreateTrainer={onCreateTrainer}
        onSelectMember={onSelectMember}
        onUpdateGym={onUpdateGym}
        products={products}
        retention={retention}
        selectedMember={selectedMember}
        trainers={trainers}
      />
    </>
  );
}

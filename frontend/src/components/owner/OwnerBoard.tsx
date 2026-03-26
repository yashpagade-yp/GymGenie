import type { UserSummary } from "../../types/auth";
import { PasswordField } from "../auth/PasswordField";
import type { ActivityTrendPoint, GoalDistributionItem, GymSettings, OwnerMemberDetail, RetentionAnalytics } from "../../types/owner";
import type { Product } from "../../types/product";
import type { ActivityAlert } from "../../types/trainer";
import { formatCurrency, titleCase } from "../../utils/formatters";

export function OwnerBoard({
  members,
  trainers,
  selectedMember,
  products,
  gym,
  alerts,
  retention,
  goals,
  activity,
  onSelectMember,
  onCreateTrainer,
  onAssignTrainer,
  onCreateProduct,
  onUpdateGym,
}: {
  members: UserSummary[];
  trainers: UserSummary[];
  selectedMember: OwnerMemberDetail | null;
  products: Product[];
  gym: GymSettings | null;
  alerts: ActivityAlert[];
  retention: RetentionAnalytics | null;
  goals: GoalDistributionItem[];
  activity: ActivityTrendPoint[];
  onSelectMember: (memberId: string) => Promise<void>;
  onCreateTrainer: (payload: { email: string; full_name: string; password: string }) => Promise<void>;
  onAssignTrainer: (payload: { trainer_id: string; member_id: string }) => Promise<void>;
  onCreateProduct: (payload: { name: string; description: string; price: number }) => Promise<void>;
  onUpdateGym: (payload: { name?: string; address?: string; logo_url?: string | null }) => Promise<void>;
}) {
  const maxGoalCount = Math.max(...goals.map((goal) => goal.count), 1);
  const maxActivityCount = Math.max(...activity.map((point) => point.workout_count), 1);
  const selectedProfile = selectedMember?.profile;

  return (
    <div className="dashboard-grid owner-layout">
      <section className="panel-card span-2 owner-command-card">
        <div className="owner-command-copy">
          <p className="eyebrow">Owner Command Center</p>
          <h2>{gym?.name ?? "Your gym"}</h2>
          <p className="muted">
            Manage members, trainers, products, retention risk, and gym settings from one structured workspace.
          </p>
        </div>
        <div className="owner-overview-strip">
          <div className="owner-overview-card">
            <span>Total members</span>
            <strong>{members.length}</strong>
          </div>
          <div className="owner-overview-card">
            <span>Total trainers</span>
            <strong>{trainers.length}</strong>
          </div>
          <div className="owner-overview-card">
            <span>Active members</span>
            <strong>{retention?.active_members ?? 0}</strong>
          </div>
          <div className="owner-overview-card">
            <span>At risk</span>
            <strong>{retention?.at_risk_members ?? 0}</strong>
          </div>
        </div>
      </section>

      <section className="panel-card owner-members-panel">
        <div className="panel-header">
          <div>
            <p className="eyebrow">Member CRM</p>
            <h3>Members</h3>
          </div>
          <span className="muted">{members.length} total</span>
        </div>
        <div className="stack compact">
          {members.length > 0 ? (
            members.map((member) => (
              <button className="member-row" key={member.id} onClick={() => void onSelectMember(member.id)} type="button">
                <div className="owner-member-row-copy">
                  <strong>{member.full_name}</strong>
                  <p>{member.email}</p>
                </div>
                <span className="status-pill active">View</span>
              </button>
            ))
          ) : (
            <p className="muted">No members have joined this gym yet.</p>
          )}
        </div>
      </section>

      <section className="panel-card owner-member-detail-panel">
        <p className="eyebrow">Selected Member Detail</p>
        {selectedMember ? (
          <div className="owner-member-detail">
            <div className="owner-member-header">
              <div>
                <h2>{selectedMember.member.full_name}</h2>
                <p className="muted">{selectedMember.member.email}</p>
              </div>
              <span className="status-pill active">{selectedMember.assigned_trainer_ids.length} trainers assigned</span>
            </div>

            <div className="owner-member-stats">
              <div className="owner-member-stat">
                <span>Goal</span>
                <strong>{selectedProfile ? titleCase(selectedProfile.goal) : "Not set"}</strong>
              </div>
              <div className="owner-member-stat">
                <span>Diet</span>
                <strong>{selectedProfile ? titleCase(selectedProfile.diet_preference.replace("_", " ")) : "Not set"}</strong>
              </div>
              <div className="owner-member-stat">
                <span>Weight</span>
                <strong>{selectedProfile ? `${selectedProfile.weight_kg} kg` : "Not set"}</strong>
              </div>
              <div className="owner-member-stat">
                <span>Height</span>
                <strong>{selectedProfile ? `${selectedProfile.height_cm} cm` : "Not set"}</strong>
              </div>
            </div>

            <div className="panel-header">
              <div>
                <h3>Recent workout activity</h3>
                <p className="muted">Latest workout logs for this member.</p>
              </div>
            </div>
            <div className="stack compact">
              {selectedMember.recent_workouts.length > 0 ? (
                selectedMember.recent_workouts.map((log) => (
                  <div className="timeline-item" key={log.id}>
                    <strong>{log.sets} x {log.reps}</strong>
                    <span>{new Date(log.logged_at).toLocaleDateString()}</span>
                  </div>
                ))
              ) : (
                <p className="muted">No workout history logged yet.</p>
              )}
            </div>
            <div className="owner-assign-card">
              <div>
                <h3>Trainer assignment</h3>
                <p className="muted">Assign a trainer to keep this member engaged and monitored.</p>
              </div>
              {trainers.length > 0 ? (
                <button
                  className="primary-button"
                  onClick={() => void onAssignTrainer({ trainer_id: trainers[0].id, member_id: selectedMember.member.id })}
                  type="button"
                >
                  Assign first available trainer
                </button>
              ) : (
                <p className="muted">Create a trainer first before assigning one.</p>
              )}
            </div>
          </div>
        ) : (
          <div className="owner-empty-state">
            <h3>Select a member</h3>
            <p className="muted">Choose a member from the left column to inspect profile details, activity, and assignment status.</p>
          </div>
        )}
      </section>

      <section className="panel-card owner-trainer-panel">
        <div className="panel-header">
          <div>
            <p className="eyebrow">Trainer Management</p>
            <h3>Team roster</h3>
          </div>
          <span className="muted">{trainers.length} trainers</span>
        </div>
        <div className="owner-roster-list">
          {trainers.length > 0 ? (
            trainers.map((trainer) => (
              <div className="timeline-item" key={trainer.id}>
                <strong>{trainer.full_name}</strong>
                <span>{trainer.email}</span>
              </div>
            ))
          ) : (
            <p className="muted">No trainers created yet.</p>
          )}
        </div>
        <form
          className="stack compact"
          onSubmit={(event) => {
            event.preventDefault();
            const formData = new FormData(event.currentTarget);
            void onCreateTrainer({
              email: String(formData.get("email")),
              full_name: String(formData.get("full_name")),
              password: String(formData.get("password")),
            });
            event.currentTarget.reset();
          }}
        >
          <input name="full_name" placeholder="Trainer name" required />
          <input name="email" placeholder="Trainer email" required type="email" />
          <PasswordField name="password" placeholder="Temporary password" required />
          <button className="primary-button" type="submit">Create trainer</button>
        </form>
      </section>

      <section className="panel-card owner-analytics-panel">
        <div className="panel-header">
          <div>
            <p className="eyebrow">Retention Analytics</p>
            <h3>Member trends</h3>
          </div>
        </div>
        <div className="owner-analytics-grid">
          <div className="owner-analytics-block">
            <h4>Goal distribution</h4>
            <div className="stack compact">
              {goals.length > 0 ? (
                goals.map((goal) => (
                  <div className="chart-row" key={goal.goal}>
                    <div className="chart-label">
                      <strong>{titleCase(goal.goal)}</strong>
                      <span>{goal.count} members</span>
                    </div>
                    <div className="chart-bar">
                      <span style={{ width: `${(goal.count / maxGoalCount) * 100}%` }} />
                    </div>
                  </div>
                ))
              ) : (
                <p className="muted">No goal data available yet.</p>
              )}
            </div>
          </div>
          <div className="owner-analytics-block">
            <h4>Workout activity</h4>
            <div className="stack compact">
              {activity.length > 0 ? (
                activity.map((point) => (
                  <div className="chart-row" key={point.label}>
                    <div className="chart-label">
                      <strong>{point.label}</strong>
                      <span>{point.workout_count} workouts</span>
                    </div>
                    <div className="chart-bar warm">
                      <span style={{ width: `${(point.workout_count / maxActivityCount) * 100}%` }} />
                    </div>
                  </div>
                ))
              ) : (
                <p className="muted">No workout activity captured yet.</p>
              )}
            </div>
          </div>
        </div>
      </section>

      <section className="panel-card owner-products-panel">
        <div className="panel-header">
          <div>
            <p className="eyebrow">Product Catalog</p>
            <h3>Inventory and sales items</h3>
          </div>
          <span className="muted">{products.length} items</span>
        </div>
        <div className="owner-roster-list">
          {products.length > 0 ? (
            products.map((product) => (
              <div className="timeline-item" key={product.id}>
                <strong>{product.name}</strong>
                <span>{formatCurrency(product.price)}</span>
              </div>
            ))
          ) : (
            <p className="muted">No products added yet.</p>
          )}
        </div>
        <form
          className="stack compact"
          onSubmit={(event) => {
            event.preventDefault();
            const formData = new FormData(event.currentTarget);
            void onCreateProduct({
              name: String(formData.get("name")),
              description: String(formData.get("description")),
              price: Number(formData.get("price")),
            });
            event.currentTarget.reset();
          }}
        >
          <input name="name" placeholder="Product name" required />
          <textarea name="description" placeholder="Description" required rows={3} />
          <input min="1" name="price" placeholder="Price" required step="0.01" type="number" />
          <button className="primary-button" type="submit">Add product</button>
        </form>
      </section>

      <section className="panel-card owner-settings-panel">
        <div className="panel-header">
          <div>
            <p className="eyebrow">Gym Settings</p>
            <h3>Business profile</h3>
          </div>
        </div>
        <div className="owner-settings-meta">
          <div className="owner-member-stat">
            <span>Invite code</span>
            <strong>{gym?.invite_code ?? "Not available"}</strong>
          </div>
        </div>
        <form
          className="stack compact"
          onSubmit={(event) => {
            event.preventDefault();
            const formData = new FormData(event.currentTarget);
            void onUpdateGym({
              name: String(formData.get("name")),
              address: String(formData.get("address")),
              logo_url: String(formData.get("logo_url")) || null,
            });
          }}
        >
          <input defaultValue={gym?.name ?? ""} name="name" placeholder="Gym name" />
          <textarea defaultValue={gym?.address ?? ""} name="address" placeholder="Gym address" rows={3} />
          <input defaultValue={gym?.logo_url ?? ""} name="logo_url" placeholder="Logo URL" />
          <button className="primary-button" type="submit">Save settings</button>
        </form>
      </section>

      <section className="panel-card span-2 owner-alerts-panel">
        <div className="panel-header">
          <div>
            <p className="eyebrow">Owner Alerts</p>
            <h3>Issues requiring follow-up</h3>
          </div>
        </div>
        <div className="stack compact">
          {alerts.length > 0 ? (
            alerts.map((alert) => (
              <div className="timeline-item" key={alert.id}>
                <strong>{titleCase(alert.alert_type)}</strong>
                <span>{alert.message}</span>
              </div>
            ))
          ) : (
            <p className="muted">No gym alerts at the moment.</p>
          )}
        </div>
      </section>
    </div>
  );
}

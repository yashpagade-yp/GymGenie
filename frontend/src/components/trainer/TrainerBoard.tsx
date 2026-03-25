import type { ActivityAlert, TrainerAssignedMember, TrainerMemberDetail, TrainerNote } from "../../types/trainer";
import { formatDate, titleCase } from "../../utils/formatters";

export function TrainerBoard({
  members,
  selectedMember,
  notes,
  alerts,
  onSelectMember,
  onCreateNote,
}: {
  members: TrainerAssignedMember[];
  selectedMember: TrainerMemberDetail | null;
  notes: TrainerNote[];
  alerts: ActivityAlert[];
  onSelectMember: (memberId: string) => Promise<void>;
  onCreateNote: (note: string) => Promise<void>;
}) {
  const activeMembers = members.filter((member) => !member.is_at_risk).length;
  const atRiskMembers = members.filter((member) => member.is_at_risk).length;
  const selectedProfile = selectedMember?.profile;

  return (
    <div className="dashboard-grid trainer-layout">
      <section className="panel-card span-2 trainer-command-card">
        <div className="trainer-command-copy">
          <p className="eyebrow">Trainer CRM</p>
          <h2>Assigned member command view</h2>
          <p className="muted">Track adherence, review workouts, capture coaching notes, and act on retention risks from one structured workspace.</p>
        </div>
        <div className="trainer-overview-strip">
          <div className="trainer-overview-card">
            <span>Assigned members</span>
            <strong>{members.length}</strong>
          </div>
          <div className="trainer-overview-card">
            <span>Active members</span>
            <strong>{activeMembers}</strong>
          </div>
          <div className="trainer-overview-card">
            <span>At risk</span>
            <strong>{atRiskMembers}</strong>
          </div>
          <div className="trainer-overview-card">
            <span>Open alerts</span>
            <strong>{alerts.length}</strong>
          </div>
        </div>
      </section>

      <section className="panel-card trainer-members-panel">
        <div className="panel-header">
          <div>
            <p className="eyebrow">Assigned Members</p>
            <h3>Coaching roster</h3>
          </div>
          <span className="muted">{members.length} total</span>
        </div>
        <div className="stack compact">
          {members.length > 0 ? (
            members.map((member) => (
              <button className="member-row" key={member.user_id} onClick={() => void onSelectMember(member.user_id)} type="button">
                <div className="owner-member-row-copy">
                  <strong>{member.full_name}</strong>
                  <p>{member.email}</p>
                </div>
                <span className={member.is_at_risk ? "status-pill risk" : "status-pill active"}>
                  {member.is_at_risk ? "At Risk" : "Active"}
                </span>
              </button>
            ))
          ) : (
            <p className="muted">No assigned members yet.</p>
          )}
        </div>
      </section>

      <section className="panel-card trainer-member-detail-panel">
        <p className="eyebrow">Selected Member</p>
        {selectedMember ? (
          <div className="trainer-member-detail">
            <div className="trainer-member-header">
              <div>
                <h2>{selectedMember.member.full_name}</h2>
                <p className="muted">{selectedMember.member.email}</p>
              </div>
              <span className={selectedMember.member.is_at_risk ? "status-pill risk" : "status-pill active"}>
                {selectedMember.member.is_at_risk ? "At Risk" : "Active"}
              </span>
            </div>

            <div className="trainer-member-stats">
              <div className="owner-member-stat">
                <span>Goal</span>
                <strong>{selectedMember.member.goal ? titleCase(selectedMember.member.goal) : "Not set"}</strong>
              </div>
              <div className="owner-member-stat">
                <span>Diet</span>
                <strong>
                  {selectedMember.member.diet_preference
                    ? titleCase(selectedMember.member.diet_preference.replace("_", " "))
                    : "Not set"}
                </strong>
              </div>
              <div className="owner-member-stat">
                <span>Workouts completed</span>
                <strong>{selectedMember.member.workouts_completed}</strong>
              </div>
              <div className="owner-member-stat">
                <span>Last workout</span>
                <strong>{selectedMember.member.last_workout_at ? formatDate(selectedMember.member.last_workout_at) : "No logs"}</strong>
              </div>
            </div>

            <div className="trainer-member-bio">
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
                <h3>Recent workouts</h3>
                <p className="muted">Use this to spot drop-off and follow up before the member disengages.</p>
              </div>
            </div>
            <div className="stack compact">
              {selectedMember.recent_workouts.length > 0 ? (
                selectedMember.recent_workouts.map((workout) => (
                  <div className="timeline-item" key={workout.id}>
                    <strong>{formatDate(workout.logged_at)}</strong>
                    <span>
                      {workout.sets} x {workout.reps} reps
                    </span>
                  </div>
                ))
              ) : (
                <p className="muted">No recent workouts logged yet.</p>
              )}
            </div>

            <div className="panel-header">
              <div>
                <h3>Private coaching notes</h3>
                <p className="muted">Store internal follow-up notes, upsell opportunities, and adherence observations.</p>
              </div>
            </div>
            <form
              className="note-form"
              onSubmit={(event) => {
                event.preventDefault();
                const formData = new FormData(event.currentTarget);
                const note = String(formData.get("note") ?? "").trim();
                if (!note) {
                  return;
                }
                void onCreateNote(note);
                event.currentTarget.reset();
              }}
            >
              <textarea name="note" placeholder="Add a private coaching note" rows={4} />
              <button className="primary-button" type="submit">
                Save note
              </button>
            </form>
            <div className="stack compact">
              {notes.length > 0 ? (
                notes.map((note) => (
                  <div className="timeline-item" key={note.id}>
                    <strong>{formatDate(note.created_at)}</strong>
                    <span>{note.note}</span>
                  </div>
                ))
              ) : (
                <p className="muted">No private notes saved for this member yet.</p>
              )}
            </div>
          </div>
        ) : (
          <div className="owner-empty-state">
            <h3>Select a member</h3>
            <p className="muted">Choose a member from the roster to review profile data, workouts, and coaching notes.</p>
          </div>
        )}
      </section>

      <section className="panel-card span-2 trainer-alerts-panel">
        <div className="panel-header">
          <div>
            <p className="eyebrow">Retention Watch</p>
            <h3>Alerts requiring action</h3>
          </div>
          <span className="muted">{alerts.length} alerts</span>
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
            <p className="muted">No inactivity or retention alerts right now.</p>
          )}
        </div>
      </section>
    </div>
  );
}

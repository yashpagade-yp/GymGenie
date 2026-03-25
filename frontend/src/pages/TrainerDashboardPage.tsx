import { useEffect, useState } from "react";

import { ApiError } from "../api/client";
import { createTrainerNote, getAssignedMembers, getTrainerAlerts, getTrainerMemberDetail, getTrainerNotes } from "../api/trainers";
import { TrainerBoard } from "../components/trainer/TrainerBoard";
import type { ActivityAlert, TrainerAssignedMember, TrainerMemberDetail, TrainerNote } from "../types/trainer";

export function TrainerDashboardPage() {
  const [members, setMembers] = useState<TrainerAssignedMember[]>([]);
  const [selectedMember, setSelectedMember] = useState<TrainerMemberDetail | null>(null);
  const [notes, setNotes] = useState<TrainerNote[]>([]);
  const [alerts, setAlerts] = useState<ActivityAlert[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function refreshBoard() {
    setError(null);
    setIsLoading(true);
    try {
      const [nextMembers, nextAlerts] = await Promise.all([getAssignedMembers(), getTrainerAlerts()]);
      setMembers(nextMembers);
      setAlerts(nextAlerts);
    } catch (requestError) {
      setError(requestError instanceof ApiError ? requestError.message : "Unable to load trainer CRM.");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    void refreshBoard();
  }, []);

  async function onSelectMember(memberId: string) {
    const [detail, nextNotes] = await Promise.all([getTrainerMemberDetail(memberId), getTrainerNotes(memberId)]);
    setSelectedMember(detail);
    setNotes(nextNotes);
  }

  async function onCreateNote(note: string) {
    if (!selectedMember) {
      return;
    }

    await createTrainerNote(selectedMember.member.user_id, note);
    const nextNotes = await getTrainerNotes(selectedMember.member.user_id);
    setNotes(nextNotes);
  }

  if (isLoading) {
    return <div className="screen-state">Loading trainer CRM...</div>;
  }

  return (
    <>
      {error ? <div className="panel-card"><p className="error-text">{error}</p></div> : null}
      <TrainerBoard
        alerts={alerts}
        members={members}
        notes={notes}
        onCreateNote={onCreateNote}
        onSelectMember={onSelectMember}
        selectedMember={selectedMember}
      />
    </>
  );
}

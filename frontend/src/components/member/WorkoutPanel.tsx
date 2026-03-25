import type { TodayWorkoutResponse } from "../../types/member";

export function WorkoutPanel({
  workout,
  onLog,
}: {
  workout: TodayWorkoutResponse | null;
  onLog: (workoutId: string) => Promise<void>;
}) {
  if (!workout) {
    return <div className="panel-card">No workout plan yet.</div>;
  }

  return (
    <section className="panel-card member-workout-panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Today&apos;s Training</p>
          <h2>Today&apos;s plan</h2>
          <p className="muted">For {workout.plan_date}</p>
        </div>
      </div>
      <div className="stack">
        {workout.exercises.map((exercise) => (
          <article className="workout-card" key={exercise.workout_id}>
            <div>
              <h3>{exercise.title}</h3>
              <p>{exercise.description}</p>
              <small>
                {exercise.muscle_group} | {exercise.prescribed_sets} sets x {exercise.prescribed_reps} reps
              </small>
            </div>
            <div className="workout-actions">
              {exercise.video_url ? (
                <a className="ghost-button" href={exercise.video_url} rel="noreferrer" target="_blank">
                  Watch
                </a>
              ) : null}
              <button className="primary-button" onClick={() => void onLog(exercise.workout_id)} type="button">
                Log set
              </button>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

import type { TodayDietResponse } from "../../types/member";

export function DietPanel({ diet }: { diet: TodayDietResponse | null }) {
  if (!diet) {
    return <div className="panel-card">No diet plan yet.</div>;
  }

  return (
    <section className="panel-card member-diet-panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Fuel Plan</p>
          <h2>{diet.total_calories} kcal</h2>
          <p className="muted">Your macro split for the day</p>
        </div>
        <div className="macro-strip">
          <span>{diet.total_protein_g}P</span>
          <span>{diet.total_carbs_g}C</span>
          <span>{diet.total_fats_g}F</span>
        </div>
      </div>
      <div className="meal-grid member-meal-grid">
        {diet.meals.map((meal) => (
          <article className="meal-card" key={meal.meal_type}>
            <p className="eyebrow">{meal.meal_type}</p>
            <h3>{meal.meal_name}</h3>
            <p>
              {meal.calories} kcal | {meal.protein_g}P / {meal.carbs_g}C / {meal.fats_g}F
            </p>
          </article>
        ))}
      </div>
    </section>
  );
}

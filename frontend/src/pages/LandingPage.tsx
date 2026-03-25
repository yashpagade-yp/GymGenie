import { Link } from "react-router-dom";

export function LandingPage() {
  return (
    <main className="landing-page">
      <section className="landing-stack">
        <section className="hero-panel landing-hero">
          <div className="hero-copy">
            <p className="eyebrow">GymGenie</p>
            <h1>Train hard. Eat smart. Keep members coming back.</h1>
            <p className="lead">
              GymGenie turns your gym into a digital coaching system with daily workouts, macro-based meal plans,
              trainer CRM follow-up, and owner-level retention visibility.
            </p>
            <div className="hero-actions horizontal">
              <Link className="primary-button" to="/register">
                Start member journey
              </Link>
              <Link className="ghost-button" to="/login">
                Open dashboard
              </Link>
            </div>
            <div className="hero-tag-row">
              <span>Workout plans</span>
              <span>Diet plans</span>
              <span>Trainer CRM</span>
              <span>Owner analytics</span>
            </div>
          </div>
          <div className="hero-visual">
            <div className="hero-stat-tower">
              <div className="metric-card accent">
                <span>Daily momentum</span>
                <strong>Slow is smooth</strong>
                <p>Build discipline with repeatable plans and consistent tracking.</p>
              </div>
              <div className="metric-card">
                <span>Gym retention</span>
                <strong>7-day inactivity alerts</strong>
                <p>Catch member drop-off before it becomes churn.</p>
              </div>
            </div>
            <div className="hero-silhouette">
              <div className="silhouette-ring" />
              <div className="silhouette-card">
                <p className="eyebrow">Today&apos;s Push</p>
                <h3>Strength + discipline + recovery</h3>
                <p>Members get guided action. Trainers get context. Owners get control.</p>
              </div>
            </div>
          </div>
        </section>

        <section className="landing-band">
          <div className="band-item">
            <span className="band-number">01</span>
            <div>
              <strong>Members</strong>
              <p>Daily workouts with video links, macro-aware diets, and progress accountability.</p>
            </div>
          </div>
          <div className="band-item">
            <span className="band-number">02</span>
            <div>
              <strong>Trainers</strong>
              <p>Assigned member CRM, private notes, and early alerts for people going inactive.</p>
            </div>
          </div>
          <div className="band-item">
            <span className="band-number">03</span>
            <div>
              <strong>Owners</strong>
              <p>Trainer management, product control, retention analytics, and goal-distribution insight.</p>
            </div>
          </div>
        </section>

        <section className="landing-grid">
          <article className="panel-card landing-feature">
            <p className="eyebrow">Member Experience</p>
            <h2>Your digital personal trainer inside the gym</h2>
            <ul className="landing-list">
              <li>Goal-based workout plans for lose, gain, or maintain</li>
              <li>Daily meal structure with calorie and macro breakdown</li>
              <li>Workout logging that turns effort into visible consistency</li>
            </ul>
          </article>

          <article className="panel-card landing-feature">
            <p className="eyebrow">Trainer CRM</p>
            <h2>Coaching clarity without chasing scattered spreadsheets</h2>
            <ul className="landing-list">
              <li>Assigned member roster with activity status</li>
              <li>Private notes for coaching, follow-up, and upsell context</li>
              <li>At-risk alerts when members stop logging workouts</li>
            </ul>
          </article>

          <article className="panel-card landing-feature">
            <p className="eyebrow">Owner Control</p>
            <h2>Know what is happening inside your gym every day</h2>
            <ul className="landing-list">
              <li>Trainer and member management inside one tenant-safe system</li>
              <li>Retention, activity, and goal distribution visibility</li>
              <li>Product catalog management for supplements and gym counter sales</li>
            </ul>
          </article>
        </section>

        <section className="landing-quote panel-card">
          <p className="eyebrow">GymGenie Philosophy</p>
          <blockquote>"Slow is smooth, smooth is fast."</blockquote>
          <p className="muted">
            Real transformation is not built on hype. It is built on repeatable habits, smart coaching,
            and a system that makes consistency easier every day.
          </p>
        </section>

        <section className="landing-cta panel-card">
          <div>
            <p className="eyebrow">Ready To Launch</p>
            <h2>Bring structure, motivation, and retention to your gym.</h2>
          </div>
          <div className="hero-actions horizontal">
            <Link className="primary-button" to="/register">
              Join as member
            </Link>
            <Link className="ghost-button" to="/login">
              Login to GymGenie
            </Link>
          </div>
        </section>
      </section>
    </main>
  );
}

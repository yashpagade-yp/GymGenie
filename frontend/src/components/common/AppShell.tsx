import { Link, useLocation } from "react-router-dom";

import { useAuth } from "../../hooks/useAuth";

const navigation = {
  member: [
    { label: "Training", href: "/dashboard/member" },
    { label: "Onboarding", href: "/onboarding" },
  ],
  trainer: [{ label: "CRM", href: "/dashboard/trainer" }],
  owner: [{ label: "Control", href: "/dashboard/owner" }],
} as const;

export function AppShell({ children }: { children: React.ReactNode }) {
  const { logout, user } = useAuth();
  const location = useLocation();

  if (!user) {
    return <>{children}</>;
  }

  return (
    <div className="app-shell">
      <aside className="shell-sidebar">
        <div>
          <div className="brand-mark">GG</div>
          <p className="eyebrow">GymGenie</p>
          <h1>Slow is smooth, smooth is fast.</h1>
        </div>
        <nav className="shell-nav">
          {navigation[user.role].map((item) => (
            <Link
              key={item.href}
              className={location.pathname === item.href ? "nav-link active" : "nav-link"}
              to={item.href}
            >
              {item.label}
            </Link>
          ))}
        </nav>
        <button className="ghost-button" onClick={logout} type="button">
          Logout
        </button>
      </aside>
      <main className="shell-content">{children}</main>
    </div>
  );
}

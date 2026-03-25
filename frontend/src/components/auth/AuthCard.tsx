export function AuthCard({
  title,
  subtitle,
  children,
}: {
  title: string;
  subtitle: string;
  children: React.ReactNode;
}) {
  return (
    <section className="auth-card">
      <p className="eyebrow">GymGenie Access</p>
      <h1>{title}</h1>
      <p className="muted">{subtitle}</p>
      {children}
    </section>
  );
}

import { portfolio } from "../../config/portfolio";

export function MetricsBar() {
  return (
    <div className="hero-stats metrics-bar">
      {portfolio.metrics.map((m) => (
        <div key={m.label} className="stat-pill">
          <span className="stat-value">{m.value}</span>
          <span className="stat-label">{m.label}</span>
        </div>
      ))}
    </div>
  );
}

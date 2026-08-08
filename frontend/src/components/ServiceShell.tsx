import { useEffect, useState, type ReactNode } from "react";
import { Link } from "react-router-dom";
import { checkHealth } from "../api/http";
import type { ServiceMeta } from "../config/services";

type Props = {
  service: ServiceMeta;
  children: ReactNode;
};

export function ServiceShell({ service, children }: Props) {
  const [online, setOnline] = useState<boolean | null>(null);

  useEffect(() => {
    let active = true;
    const ping = async () => {
      const ok = await checkHealth(service.baseUrl);
      if (active) setOnline(ok);
    };
    void ping();
    const id = window.setInterval(ping, 8000);
    return () => {
      active = false;
      window.clearInterval(id);
    };
  }, [service.baseUrl]);

  return (
    <div className={`app-shell realm-stage ${service.theme}`} data-game={service.game}>
      <header className="glass-card shell-header-card">
        <div className="shell-header">
          <div>
            <Link className="back-link" to="/">
              ← Exit realm
            </Link>
            <div className="realm-chip">{service.realm}</div>
            <h1>
              {service.index}. {service.name}
            </h1>
            <p>{service.tagline}</p>
            <p className="muted">{service.blurb}</p>
            <p className="muted">
              Uplink: <code>{service.baseUrl}</code>
            </p>
          </div>
          <div className={`badge ${online ? "online" : online === false ? "offline" : ""}`}>
            <span className="badge-dot" />
            {online === null ? "SCANNING…" : online ? "SIGNAL LOCKED" : "SIGNAL LOST"}
          </div>
        </div>
      </header>
      {children}
    </div>
  );
}

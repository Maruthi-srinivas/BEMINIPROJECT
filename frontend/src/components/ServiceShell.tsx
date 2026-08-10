import { useEffect, useState, type ReactNode } from "react";
import { checkHealth } from "../api/http";
import { getHighlightForService } from "../config/portfolio";
import type { ServiceMeta } from "../config/services";

type Props = {
  service: ServiceMeta;
  children: ReactNode;
};

export function ServiceShell({ service, children }: Props) {
  const [online, setOnline] = useState<boolean | null>(null);
  const highlight = getHighlightForService(service.slug);

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
            <div className="realm-breadcrumb">
              <span className="realm-chip">{service.realm}</span>
              <span className="realm-breadcrumb-sep">/</span>
              <span className="realm-game-chip">{service.game}</span>
            </div>
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
        {highlight && (
          <aside className="resume-callout">
            <div className="resume-callout-label">Resume highlight</div>
            <strong>{highlight.title}</strong>
            <p>{highlight.talkingPoint ?? highlight.body}</p>
          </aside>
        )}
      </header>
      {children}
    </div>
  );
}

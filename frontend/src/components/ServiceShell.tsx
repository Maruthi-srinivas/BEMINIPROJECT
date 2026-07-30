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
    <div className="app-shell">
      <div className="shell-header">
        <div>
          <Link className="back-link" to="/">
            ← All services
          </Link>
          <h1>
            {service.index}. {service.name}
          </h1>
          <p>{service.blurb}</p>
          <p className="muted">
            Base URL: <code>{service.baseUrl}</code>
          </p>
        </div>
        <div className={`badge ${online ? "online" : online === false ? "offline" : ""}`}>
          {online === null ? "Checking…" : online ? "Online" : "Offline — start the service"}
        </div>
      </div>
      {children}
    </div>
  );
}

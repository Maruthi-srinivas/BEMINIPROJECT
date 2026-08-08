import { Link } from "react-router-dom";
import { services } from "../config/services";

export function HomePage() {
  return (
    <div className="app-shell">
      <section className="hero">
        <div className="glass-card hero-card">
          <div className="brand brand-mark">BE Mini Lab // Neon Realms</div>
          <h1>
            Jack into <span className="gradient-text">ten</span> backend worlds
          </h1>
          <p>
            A cyberpunk ops deck where every microservice is a playable open-world
            RPG realm — neon corridors, vault terminals, and mass relays waiting
            for your next command.
          </p>
          <div className="hero-stats">
            <div className="stat-pill">
              <span className="stat-value">{services.length}</span>
              <span className="stat-label">Realms</span>
            </div>
            <div className="stat-pill">
              <span className="stat-value">FastAPI</span>
              <span className="stat-label">Stack</span>
            </div>
            <div className="stat-pill">
              <span className="stat-value">Live</span>
              <span className="stat-label">Uplink</span>
            </div>
          </div>
          <a className="cta" href="#services">
            <span className="cta-glow" />
            Enter the grid →
          </a>
        </div>
      </section>

      <section id="services" className="glass-section">
        <div className="section-header">
          <h2 className="section-title">Realm Directory</h2>
          <p className="section-sub">
            Each console channels a legendary open-world RPG vibe while talking to
            the live FastAPI service on its port.
          </p>
        </div>
        <div className="service-list">
          {services.map((service) => (
            <Link
              key={service.slug}
              className={`service-link ${service.theme}`}
              to={`/services/${service.slug}`}
            >
              <span className="service-index">{service.index}</span>
              <div>
                <h3>{service.name}</h3>
                <p className="realm">
                  {service.realm} · {service.game}
                </p>
                <p>{service.tagline}</p>
              </div>
              <span className="service-port">:{service.port}</span>
              <span className="service-shimmer" />
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}

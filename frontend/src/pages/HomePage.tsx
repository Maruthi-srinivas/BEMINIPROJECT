import { Link } from "react-router-dom";
import { services } from "../config/services";

export function HomePage() {
  return (
    <div className="app-shell">
      <section className="hero">
        <div className="brand brand-mark">BE Mini Lab // Neon Realms</div>
        <h1>
          Jack into <span>ten</span> backend worlds
        </h1>
        <p>
          A cyberpunk ops deck where every microservice is a playable open-world
          RPG realm — neon corridors, vault terminals, and mass relays waiting
          for your next command.
        </p>
        <a className="cta" href="#services">
          Enter the grid →
        </a>
      </section>

      <section id="services">
        <h2 className="section-title">Realm Directory</h2>
        <p className="section-sub">
          Each console channels a legendary open-world RPG vibe while talking to
          the live FastAPI service on its port.
        </p>
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
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}

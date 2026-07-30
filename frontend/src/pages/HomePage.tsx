import { Link } from "react-router-dom";
import { services } from "../config/services";

export function HomePage() {
  return (
    <div className="app-shell">
      <section className="hero">
        <div className="brand brand-mark">BE Mini Lab</div>
        <h1>Ten backend services. One console.</h1>
        <p>
          Explore production-inspired mini services — from URL shortening to
          feature flags — through focused interactive consoles.
        </p>
        <a className="cta" href="#services">
          Browse services →
        </a>
      </section>

      <section id="services">
        <h2 className="section-title">Services</h2>
        <div className="service-list">
          {services.map((service) => (
            <Link
              key={service.slug}
              className="service-link"
              to={`/services/${service.slug}`}
            >
              <span className="service-index">{service.index}</span>
              <div>
                <h3>{service.name}</h3>
                <p>{service.blurb}</p>
              </div>
              <span className="service-port">:{service.port}</span>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}

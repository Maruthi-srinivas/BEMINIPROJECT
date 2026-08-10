import { useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { ArchitectureMap } from "../components/portfolio/ArchitectureMap";
import { HighlightCards } from "../components/portfolio/HighlightCards";
import { MetricsBar } from "../components/portfolio/MetricsBar";
import { NarrativeSection } from "../components/portfolio/NarrativeSection";
import { SectionHeader } from "../components/portfolio/SectionHeader";
import { SkillsGrid } from "../components/portfolio/SkillsGrid";
import { portfolio } from "../config/portfolio";
import { services } from "../config/services";

export function HomePage() {
  const location = useLocation();

  useEffect(() => {
    if (!location.hash) return;
    const id = location.hash.slice(1);
    const el = document.getElementById(id);
    if (el) {
      requestAnimationFrame(() => {
        el.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    }
  }, [location.hash]);

  return (
    <div className="app-shell portfolio-shell">
      <section id="hero" className="hero">
        <div className="glass-card hero-card hud-frame">
          <div className="brand brand-mark">
            {portfolio.brand} // Neon Realms
          </div>
          <h1>
            Ten backend systems.{" "}
            <span className="gradient-text">One neon</span> command deck.
          </h1>
          <p>{portfolio.heroSub}</p>
          <p className="hero-oneliner muted">{portfolio.oneLiner}</p>
          <MetricsBar />
          <div className="hero-ctas">
            <a className="cta" href="#architecture">
              <span className="cta-glow" />
              Explore architecture →
            </a>
            <a className="cta cta-secondary" href="#services">
              <span className="cta-glow" />
              Launch demos →
            </a>
          </div>
        </div>
      </section>

      <NarrativeSection />
      <ArchitectureMap />
      <SkillsGrid />
      <HighlightCards />

      <section id="services" className="portfolio-section glass-section">
        <SectionHeader
          index="05 // Demos"
          title="Realm Directory"
          subtitle="Each console channels a live FastAPI service — jack in and exercise the API."
        />
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

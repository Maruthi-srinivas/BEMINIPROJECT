import { Link } from "react-router-dom";
import { portfolio } from "../../config/portfolio";
import { services } from "../../config/services";
import { ScrollReveal } from "./ScrollReveal";
import { SectionHeader } from "./SectionHeader";

export function ArchitectureMap() {
  return (
    <section id="architecture" className="portfolio-section">
      <SectionHeader
        index="02 // Architecture"
        title="Systems map"
        subtitle="Independent deployable services — each owns config, store, and deploy. Not a shared mesh."
      />
      <ScrollReveal>
        <div className="arch-map glass-section hud-frame">
          <div className="arch-hub">
            <span className="arch-hub-label">{portfolio.architectureHub.label}</span>
            <p className="muted">{portfolio.architectureHub.blurb}</p>
          </div>

          <div className="arch-services">
            {services.map((service) => (
              <Link
                key={service.slug}
                to={`/services/${service.slug}`}
                className={`arch-node arch-node--service ${service.theme}`}
                title={service.blurb}
              >
                <span className="arch-node-index">{service.index}</span>
                <span className="arch-node-name">{service.name}</span>
                <span className="arch-node-tip">{service.blurb}</span>
              </Link>
            ))}
          </div>

          <div className="arch-infra-label">Shared infra patterns</div>
          <div className="arch-infra">
            {portfolio.architectureInfra.map((node) => (
              <div key={node.id} className="arch-node arch-node--infra" title={node.blurb}>
                <span className="arch-node-name">{node.label}</span>
                <span className="arch-node-tip">{node.blurb}</span>
              </div>
            ))}
          </div>
        </div>
      </ScrollReveal>
    </section>
  );
}

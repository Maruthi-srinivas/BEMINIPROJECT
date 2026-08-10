import { portfolio } from "../../config/portfolio";
import { ScrollReveal } from "./ScrollReveal";
import { SectionHeader } from "./SectionHeader";

export function SkillsGrid() {
  return (
    <section id="skills" className="portfolio-section">
      <SectionHeader
        index="03 // Skills"
        title="Stack matrix"
        subtitle="Scannable keywords aligned with the resume skills line."
      />
      <div className="skills-grid">
        {portfolio.skills.map((group, i) => (
          <ScrollReveal key={group.category} delayMs={i * 70}>
            <div className="glass-card skills-card">
              <h3 className="skills-category">{group.category}</h3>
              <div className="skills-chips">
                {group.items.map((item) => (
                  <span key={item} className="skill-chip">
                    {item}
                  </span>
                ))}
              </div>
            </div>
          </ScrollReveal>
        ))}
      </div>
    </section>
  );
}

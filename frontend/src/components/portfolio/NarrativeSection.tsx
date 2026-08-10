import { portfolio } from "../../config/portfolio";
import { ScrollReveal } from "./ScrollReveal";
import { SectionHeader } from "./SectionHeader";

export function NarrativeSection() {
  return (
    <section id="story" className="portfolio-section">
      <SectionHeader
        index="01 // Story"
        title="Project narrative"
        subtitle="STAR framing for interview walkthroughs — why this lab exists and what it proves."
      />
      <div className="narrative-grid">
        {portfolio.starNarrative.map((block, i) => (
          <ScrollReveal key={block.label} delayMs={i * 90}>
            <article className="glass-card narrative-card">
              <div className="narrative-label">{block.label}</div>
              <h3>{block.title}</h3>
              <p>{block.body}</p>
            </article>
          </ScrollReveal>
        ))}
      </div>
    </section>
  );
}

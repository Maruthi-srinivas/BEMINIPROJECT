import { useState } from "react";
import { portfolio } from "../../config/portfolio";
import { ScrollReveal } from "./ScrollReveal";
import { SectionHeader } from "./SectionHeader";

export function HighlightCards() {
  const [openId, setOpenId] = useState<string | null>(null);

  return (
    <section id="highlights" className="portfolio-section">
      <SectionHeader
        index="04 // Highlights"
        title="Engineering highlights"
        subtitle="Resume bullets with expandable interview talking points."
      />
      <div className="highlights-grid">
        {portfolio.highlights.map((item, i) => {
          const isOpen = openId === item.id;
          return (
            <ScrollReveal key={item.id} delayMs={i * 60}>
              <button
                type="button"
                className={`glass-card highlight-card ${isOpen ? "is-open" : ""}`}
                aria-expanded={isOpen}
                onClick={() => setOpenId(isOpen ? null : item.id)}
              >
                <div className="highlight-card-top">
                  <h3>{item.title}</h3>
                  <span className="highlight-chevron" aria-hidden="true">
                    {isOpen ? "−" : "+"}
                  </span>
                </div>
                <p>{item.body}</p>
                <div className="highlight-tags">
                  {item.tags.map((tag) => (
                    <span key={tag} className="skill-chip skill-chip--sm">
                      {tag}
                    </span>
                  ))}
                </div>
                {item.talkingPoint && (
                  <div className={`highlight-talk ${isOpen ? "is-open" : ""}`}>
                    <div className="highlight-talk-label">Interview angle</div>
                    <p>{item.talkingPoint}</p>
                  </div>
                )}
              </button>
            </ScrollReveal>
          );
        })}
      </div>
    </section>
  );
}

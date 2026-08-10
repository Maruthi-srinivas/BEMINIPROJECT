import { portfolio } from "../../config/portfolio";

export function SiteFooter() {
  return (
    <footer className="site-footer">
      <div className="site-footer-inner">
        <div>
          <div className="site-footer-brand">{portfolio.brand}</div>
          <p className="site-footer-title">{portfolio.projectTitle}</p>
          <p className="muted">{portfolio.footerNote}</p>
        </div>
        <div className="site-footer-badges" aria-label="Tech stack">
          {portfolio.footerStack.map((item) => (
            <span key={item} className="footer-badge">
              {item}
            </span>
          ))}
        </div>
      </div>
    </footer>
  );
}

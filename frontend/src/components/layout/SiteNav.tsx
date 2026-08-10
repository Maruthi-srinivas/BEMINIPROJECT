import { useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { navAnchors, portfolio } from "../../config/portfolio";

export function SiteNav() {
  const location = useLocation();
  const isHome = location.pathname === "/";
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState<string>("hero");
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    setOpen(false);
  }, [location.pathname, location.hash]);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    if (!isHome) return;

    const ids = ["hero", ...navAnchors.map((a) => a.id)];
    const elements = ids
      .map((id) => document.getElementById(id))
      .filter((el): el is HTMLElement => Boolean(el));

    if (elements.length === 0) return;

    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((e) => e.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio);
        if (visible[0]?.target.id) {
          setActive(visible[0].target.id);
        }
      },
      { rootMargin: "-20% 0px -55% 0px", threshold: [0.1, 0.35, 0.6] },
    );

    elements.forEach((el) => observer.observe(el));
    return () => observer.disconnect();
  }, [isHome]);

  const linkTo = (id: string) => (isHome ? `#${id}` : `/#${id}`);

  return (
    <header className={`site-nav ${scrolled ? "site-nav--scrolled" : ""}`}>
      <div className="site-nav-inner">
        <Link className="site-nav-brand" to="/" onClick={() => setOpen(false)}>
          <span className="site-nav-brand-mark" />
          {portfolio.brand}
        </Link>

        {isHome ? (
          <>
            <nav className="site-nav-links" aria-label="Portfolio sections">
              {navAnchors.map((anchor) => (
                <a
                  key={anchor.id}
                  href={`#${anchor.id}`}
                  className={`site-nav-link ${active === anchor.id ? "is-active" : ""}`}
                >
                  {anchor.label}
                </a>
              ))}
            </nav>
            <button
              type="button"
              className={`site-nav-toggle ${open ? "is-open" : ""}`}
              aria-expanded={open}
              aria-controls="site-nav-mobile"
              aria-label={open ? "Close menu" : "Open menu"}
              onClick={() => setOpen((v) => !v)}
            >
              <span />
              <span />
              <span />
            </button>
          </>
        ) : (
          <Link className="site-nav-back" to="/">
            ← Portfolio
          </Link>
        )}
      </div>

      {isHome && (
        <div
          id="site-nav-mobile"
          className={`site-nav-mobile ${open ? "is-open" : ""}`}
          hidden={!open}
        >
          {navAnchors.map((anchor) => (
            <a
              key={anchor.id}
              href={linkTo(anchor.id)}
              className={`site-nav-link ${active === anchor.id ? "is-active" : ""}`}
              onClick={() => setOpen(false)}
            >
              {anchor.label}
            </a>
          ))}
        </div>
      )}
    </header>
  );
}

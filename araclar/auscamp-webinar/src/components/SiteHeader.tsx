import { useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { webinars, communityUrl } from "../config/webinars";
import { dateBadge } from "../lib/dates";
import { trackAndRedirect } from "../lib/tracking";

/**
 * Sticky site header with a left hamburger that opens a slide-in drawer.
 * The drawer is the primary way to jump to each webinar's own page from
 * anywhere on the site (home + detail pages).
 */
export default function SiteHeader() {
  const [open, setOpen] = useState(false);
  const location = useLocation();

  // Close the drawer whenever the route changes.
  useEffect(() => setOpen(false), [location.pathname]);

  // Lock body scroll while the drawer is open.
  useEffect(() => {
    document.body.style.overflow = open ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [open]);

  // Close on Escape.
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && setOpen(false);
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open]);

  return (
    <>
      <header className="absolute inset-x-0 top-0 z-40">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-4 sm:px-6">
          <button
            type="button"
            onClick={() => setOpen(true)}
            aria-label="Menüyü aç"
            aria-expanded={open}
            className="inline-flex h-11 w-11 items-center justify-center rounded-xl border border-white/15 bg-white/10 text-white backdrop-blur-md transition hover:bg-white/20 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
          >
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden>
              <path d="M3 6h18M3 12h18M3 18h18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
            </svg>
          </button>

          <Link to="/" aria-label="AUSCAMP ana sayfa" className="rounded-xl bg-white px-4 py-2 shadow-card">
            <img src="/auscamp-logo.png" alt="AUSCAMP" className="h-7 w-auto sm:h-8" />
          </Link>

          <button
            type="button"
            onClick={() => trackAndRedirect("header-cta", communityUrl)}
            className="hidden rounded-full bg-brand-yellow px-5 py-2.5 text-sm font-bold text-brand-green-dark shadow-card transition hover:brightness-105 sm:inline-flex"
          >
            Topluluğa Katıl
          </button>
          {/* On mobile the right slot stays balanced with an invisible spacer */}
          <span aria-hidden className="h-11 w-11 sm:hidden" />
        </div>
      </header>

      {/* Drawer + scrim */}
      <div
        className={`fixed inset-0 z-50 transition ${open ? "visible" : "invisible"}`}
        aria-hidden={!open}
      >
        <div
          onClick={() => setOpen(false)}
          className={`absolute inset-0 bg-brand-green-dark/70 backdrop-blur-sm transition-opacity duration-300 ${
            open ? "opacity-100" : "opacity-0"
          }`}
        />
        <nav
          className={`absolute left-0 top-0 flex h-full w-[86%] max-w-sm flex-col bg-brand-green-dark shadow-2xl transition-transform duration-300 ${
            open ? "translate-x-0" : "-translate-x-full"
          }`}
          aria-label="Ana menü"
        >
          <div className="flex items-center justify-between border-b border-white/10 px-6 py-5">
            <img src="/auscamp-logo.png" alt="AUSCAMP" className="h-8 w-auto rounded-lg bg-white p-1.5" />
            <button
              type="button"
              onClick={() => setOpen(false)}
              aria-label="Menüyü kapat"
              className="inline-flex h-10 w-10 items-center justify-center rounded-lg text-brand-cream/80 transition hover:bg-white/10 hover:text-white"
            >
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden>
                <path d="M6 6l12 12M18 6L6 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
              </svg>
            </button>
          </div>

          <div className="flex-1 overflow-y-auto px-6 py-6">
            <Link
              to="/"
              className="block rounded-xl px-3 py-3 text-lg font-bold text-white transition hover:bg-white/10"
            >
              Ana Sayfa
            </Link>

            <p className="mt-6 px-3 text-xs font-bold uppercase tracking-[0.2em] text-brand-yellow">
              Ekim Webinarları
            </p>
            <ul className="mt-2 space-y-1">
              {webinars.map((w) => {
                const b = dateBadge(w);
                // Danışanlara özel oturumlar reklamdan gelen ziyaretçiye kapalı:
                // detay sayfasına link verilmez, satır tıklanabilir değildir.
                const rowInner = (
                  <>
                    <span className="flex h-11 w-11 shrink-0 flex-col items-center justify-center rounded-lg bg-brand-yellow/15 leading-none text-brand-yellow">
                      <span className="text-base font-extrabold">{b.day}</span>
                      <span className="text-[9px] font-bold uppercase">{b.month}</span>
                    </span>
                    <span className="min-w-0">
                      <span className="block text-sm font-semibold leading-snug text-white">
                        {w.title}
                      </span>
                      <span className="block truncate text-xs text-brand-cream/60">
                        {w.speaker}
                        {!w.openToAll && " · Danışanlara özel"}
                      </span>
                    </span>
                  </>
                );
                return (
                  <li key={w.slug}>
                    {w.openToAll ? (
                      <Link
                        to={`/webinar/${w.slug}`}
                        className="flex items-center gap-3 rounded-xl px-3 py-3 transition hover:bg-white/10"
                      >
                        {rowInner}
                      </Link>
                    ) : (
                      <div className="flex items-center gap-3 rounded-xl px-3 py-3">
                        {rowInner}
                      </div>
                    )}
                  </li>
                );
              })}
            </ul>

            <div className="mt-6 space-y-1 border-t border-white/10 pt-4">
              <a href="/#kadro" className="block rounded-xl px-3 py-2.5 font-semibold text-brand-cream/90 transition hover:bg-white/10 hover:text-white">
                Uzman Kadro
              </a>
              <a href="/#nasil" className="block rounded-xl px-3 py-2.5 font-semibold text-brand-cream/90 transition hover:bg-white/10 hover:text-white">
                Webinara Nasıl Katılırım?
              </a>
              <a href="/#sss" className="block rounded-xl px-3 py-2.5 font-semibold text-brand-cream/90 transition hover:bg-white/10 hover:text-white">
                Sık Sorulanlar
              </a>
              <a href="/#bilgi" className="block rounded-xl px-3 py-2.5 font-semibold text-brand-yellow transition hover:bg-white/10">
                Bilgi Al / Ön Değerlendirme
              </a>
            </div>
          </div>

          <div className="border-t border-white/10 p-6">
            <button
              type="button"
              onClick={() => trackAndRedirect("drawer-cta", communityUrl)}
              className="btn-primary w-full"
            >
              Duyuru Topluluğuna Katıl
              <span aria-hidden>→</span>
            </button>
          </div>
        </nav>
      </div>
    </>
  );
}

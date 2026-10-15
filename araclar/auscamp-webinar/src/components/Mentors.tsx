import { useEffect, useState } from "react";
import { createPortal } from "react-dom";
import { mentors, type Mentor } from "../config/mentors";

const TITLES = new Set(["dr", "doç", "doc", "uzm", "dt", "prof", "op"]);

function initials(name: string): string {
  const words = name
    .split(/\s+/)
    .map((w) => w.replace(/\./g, ""))
    .filter((w) => w && !TITLES.has(w.toLowerCase()));
  return words.slice(0, 2).map((w) => w[0]?.toUpperCase() ?? "").join("");
}

function Avatar({ m, size }: { m: Mentor; size: "md" | "lg" }) {
  const dim = size === "lg" ? "h-28 w-28" : "h-24 w-24 sm:h-28 sm:w-28";
  return (
    <div className={`relative ${dim} shrink-0 rounded-full p-[3px] ring-2 ring-brand-yellow`}>
      {m.photo ? (
        <img
          src={m.photo}
          alt={m.name}
          className="h-full w-full rounded-full object-cover"
          style={{ objectPosition: m.objectPosition ?? "50% 30%" }}
          loading="lazy"
        />
      ) : (
        <div className="flex h-full w-full items-center justify-center rounded-full bg-gradient-to-br from-brand-green to-brand-green-deep text-xl font-extrabold text-white">
          {initials(m.name)}
        </div>
      )}
    </div>
  );
}

export default function Mentors() {
  const [active, setActive] = useState<Mentor | null>(null);

  useEffect(() => {
    document.body.style.overflow = active ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [active]);

  useEffect(() => {
    if (!active) return;
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && setActive(null);
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [active]);

  return (
    <section id="kadro" className="bg-brand-cream px-5 py-16 text-brand-green-dark sm:py-20">
      <div className="mx-auto max-w-5xl">
        <div className="flex flex-col items-center text-center">
          <p className="section-eyebrow text-brand-green">Uzman Kadro & Mentorlar</p>
          <h2 className="section-heading text-brand-green-dark">
            Süreci yaşamış hekimlerden rehberlik
          </h2>
          <span className="section-rule" />
          <p className="mt-5 max-w-2xl text-sm leading-relaxed text-brand-green-dark/70 sm:text-base">
            Webinarları veren ekip, Avustralya&apos;da aktif çalışan ya da denklik
            sürecini birebir yaşamış hekimlerden oluşur. 8 yıllık USCAMP deneyiminin
            üzerine kurulan kadromuzla her adımda yanınızdayız.
          </p>
        </div>

        <div className="mt-12 grid grid-cols-2 gap-x-6 gap-y-10 sm:grid-cols-3 md:grid-cols-4">
          {mentors.map((m) => (
            <button
              key={m.name}
              type="button"
              onClick={() => setActive(m)}
              className="group flex flex-col items-center text-center focus:outline-none"
            >
              <div className="transition-transform duration-200 group-hover:-translate-y-1">
                <Avatar m={m} size="md" />
              </div>
              <p className="mt-4 text-sm font-bold leading-snug text-brand-green-dark group-hover:text-brand-green">
                {m.name}
              </p>
              <p className="mt-1 text-xs font-medium text-brand-green-dark/55">{m.role}</p>
              {m.bio && (
                <span className="mt-2 text-xs font-semibold text-brand-green opacity-0 transition-opacity group-hover:opacity-100">
                  Özgeçmişi gör →
                </span>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Bio modal — portaled to <body> so `position: fixed` escapes the
          transformed/will-change ancestor (Reveal) and centers on the viewport. */}
      {active &&
        createPortal(
        <div
          className="fixed inset-0 z-50 flex items-end justify-center p-0 sm:items-center sm:p-6"
          role="dialog"
          aria-modal="true"
          aria-label={`${active.name} özgeçmiş`}
        >
          <div
            className="absolute inset-0 bg-brand-green-dark/70 backdrop-blur-sm"
            onClick={() => setActive(null)}
          />
          <div className="relative w-full max-w-lg overflow-hidden rounded-t-3xl bg-white shadow-2xl sm:rounded-3xl">
            <button
              type="button"
              onClick={() => setActive(null)}
              aria-label="Kapat"
              className="absolute right-4 top-4 inline-flex h-9 w-9 items-center justify-center rounded-full bg-brand-green-dark/5 text-brand-green-dark/60 transition hover:bg-brand-green-dark/10 hover:text-brand-green-dark"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden>
                <path d="M6 6l12 12M18 6L6 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
              </svg>
            </button>
            <div className="max-h-[85vh] overflow-y-auto p-7 sm:p-8">
              <div className="flex flex-col items-center text-center">
                <Avatar m={active} size="lg" />
                <h3 className="mt-4 text-lg font-extrabold text-brand-green-dark">{active.name}</h3>
                <p className="mt-1 text-sm font-semibold text-brand-green">{active.role}</p>
                <span className="mt-4 h-px w-12 bg-brand-yellow" />
              </div>
              <p className="mt-5 text-sm leading-relaxed text-brand-green-dark/80">{active.bio}</p>
            </div>
          </div>
        </div>,
          document.body
        )}
    </section>
  );
}

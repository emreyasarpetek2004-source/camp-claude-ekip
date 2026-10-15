import { useEffect, useRef, useState, type ReactNode } from "react";

/**
 * Fades + rises its children into view when scrolled into the viewport.
 *
 * FAILSAFE by design: this wraps conversion-critical content, so it must never
 * leave content permanently hidden. If IntersectionObserver is unavailable, or
 * hasn't fired within a short grace period, the content is revealed anyway.
 * prefers-reduced-motion users skip the transform entirely (handled in CSS).
 */
export default function Reveal({
  children,
  className = "",
  delayMs = 0,
}: {
  children: ReactNode;
  className?: string;
  delayMs?: number;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el || typeof IntersectionObserver === "undefined") {
      setVisible(true);
      return;
    }

    const obs = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          if (e.isIntersecting) {
            setVisible(true);
            obs.disconnect();
          }
        }
      },
      { threshold: 0.1, rootMargin: "0px 0px 200px 0px" }
    );
    obs.observe(el);

    // Safety net: never let content stay hidden if the observer misbehaves
    // (odd scroll containers, restored scroll position, etc.).
    const fallback = window.setTimeout(() => setVisible(true), 1600);

    return () => {
      obs.disconnect();
      window.clearTimeout(fallback);
    };
  }, []);

  return (
    <div
      ref={ref}
      className={`reveal ${visible ? "is-visible" : ""} ${className}`}
      style={delayMs ? { transitionDelay: `${delayMs}ms` } : undefined}
    >
      {children}
    </div>
  );
}

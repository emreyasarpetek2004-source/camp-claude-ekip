import { useMemo } from "react";
import { webinars } from "../config/webinars";
import { webinarInstant, isPast, formatWebinarDate } from "../lib/dates";
import CountdownTimer from "./CountdownTimer";

export default function Countdown() {
  // The next upcoming webinar, chosen at runtime from the config.
  const next = useMemo(() => {
    const upcoming = webinars
      .filter((w) => !isPast(w))
      .sort((a, b) => webinarInstant(a).getTime() - webinarInstant(b).getTime());
    return upcoming[0] ?? null;
  }, []);

  if (!next) return null;

  return (
    <section className="px-5 py-10" aria-label="Bir sonraki webinara kalan süre">
      <div className="glass mx-auto max-w-2xl p-7 text-center shadow-lift sm:p-9">
        <CountdownTimer
          target={webinarInstant(next).getTime()}
          label="Bir sonraki webinara kalan süre"
        />
        <div className="mx-auto mt-6 h-px w-16 bg-brand-yellow/40" />
        <p className="mt-5 text-sm text-brand-cream/90">
          <span className="font-semibold text-white">{next.title}</span>
          <br />
          <span className="text-brand-cream/70">{formatWebinarDate(next)}</span>
        </p>
      </div>
    </section>
  );
}

import { useMemo } from "react";
import { webinars } from "../config/webinars";
import { webinarInstant } from "../lib/dates";
import WebinarCard from "./WebinarCard";

export default function WebinarList() {
  // Sort chronologically so past ones drop to the bottom naturally.
  const ordered = useMemo(
    () => [...webinars].sort((a, b) => webinarInstant(a).getTime() - webinarInstant(b).getTime()),
    []
  );

  return (
    <section id="webinarlar" className="px-5 py-10 sm:py-14">
      <div className="mx-auto max-w-2xl">
        <div className="flex flex-col items-center text-center">
          <p className="section-eyebrow">Ekim 2026 · 4 canlı oturum</p>
          <h2 className="section-heading text-white">Yaklaşan webinarlar</h2>
          <span className="section-rule" />
          <p className="mx-auto mt-5 max-w-md text-sm text-brand-cream/80">
            Her webinar Türkiye saatiyle 13.00'te canlı. Gruba katıl, katılım linki
            webinar günü grupta paylaşılsın.
          </p>
        </div>

        <div className="mt-7 flex flex-col gap-4 sm:gap-5">
          {ordered.map((w) => (
            <WebinarCard key={w.slug} webinar={w} />
          ))}
        </div>
      </div>
    </section>
  );
}

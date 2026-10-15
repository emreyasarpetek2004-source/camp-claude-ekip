import { useCountdown } from "../hooks/useCountdown";

function pad(n: number): string {
  return String(n).padStart(2, "0");
}

interface Props {
  target: number;
  label?: string;
}

export default function CountdownTimer({ target, label }: Props) {
  const t = useCountdown(target);
  if (!t) return null;

  if (t.done) {
    return (
      <p className="rounded-2xl bg-brand-yellow/15 px-4 py-3 text-center text-sm font-semibold text-brand-yellow">
        Webinar başladı. Katılım linki için WhatsApp grubuna göz at.
      </p>
    );
  }

  const units = [
    { label: "Gün", value: t.days },
    { label: "Saat", value: t.hours },
    { label: "Dakika", value: t.minutes },
    { label: "Saniye", value: t.seconds },
  ];

  return (
    <div>
      {label && (
        <p className="mb-4 text-center text-sm font-semibold uppercase tracking-widest text-brand-yellow">
          {label}
        </p>
      )}
      <div className="flex justify-center gap-2 sm:gap-4">
        {units.map((u) => (
          <div
            key={u.label}
            className="flex min-w-[68px] flex-col items-center rounded-2xl bg-brand-green-dark/70 px-2 py-3 sm:min-w-[84px] sm:py-4"
          >
            <span className="font-mono text-3xl font-extrabold tabular-nums text-white sm:text-4xl">
              {pad(u.value)}
            </span>
            <span className="mt-1 text-[11px] font-medium uppercase tracking-wide text-brand-cream/70 sm:text-xs">
              {u.label}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

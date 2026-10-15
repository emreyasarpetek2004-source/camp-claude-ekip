import type { Webinar } from "../types";

const TR_MONTHS = [
  "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
  "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık",
];

// Turkey time is UTC+3 year-round (no DST since 2016). Building the instant
// with a fixed +03:00 offset makes "13.00 TSİ" correct in every viewer's
// timezone without needing Intl timezone math.
export function webinarInstant(w: Pick<Webinar, "date" | "time">): Date {
  const [h, m] = w.time.split(".");
  const hh = (h ?? "13").padStart(2, "0");
  const mm = (m ?? "00").padStart(2, "0");
  return new Date(`${w.date}T${hh}:${mm}:00+03:00`);
}

export function isPast(w: Pick<Webinar, "date" | "time">, now: number = Date.now()): boolean {
  return webinarInstant(w).getTime() < now;
}

// "12 Temmuz 2026, 13.00 TSİ"
export function formatWebinarDate(w: Pick<Webinar, "date" | "time">): string {
  const [y, mo, d] = w.date.split("-").map(Number);
  const day = d;
  const month = TR_MONTHS[(mo ?? 1) - 1];
  return `${day} ${month} ${y}, ${w.time} TSİ`;
}

// Short date badge: { day: "12", month: "Temmuz" }
export function dateBadge(w: Pick<Webinar, "date">): { day: string; month: string } {
  const [, mo, d] = w.date.split("-").map(Number);
  return { day: String(d), month: TR_MONTHS[(mo ?? 1) - 1] ?? "" };
}

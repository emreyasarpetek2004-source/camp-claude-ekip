import { Link } from "react-router-dom";
import type { Webinar } from "../types";
import { dateBadge, formatWebinarDate, isPast } from "../lib/dates";
import { webinarSpeakers } from "../config/speakers";
import { trackAndRedirect } from "../lib/tracking";
import SpeakerAvatar from "./SpeakerAvatar";
import { WhatsAppIcon } from "./icons";

export default function WebinarCard({ webinar }: { webinar: Webinar }) {
  const past = isPast(webinar);
  const badge = dateBadge(webinar);

  return (
    <article
      className={`group relative flex flex-col gap-4 rounded-3xl border border-transparent bg-white p-5 text-brand-green-dark shadow-card transition-all duration-200 hover:-translate-y-0.5 hover:border-brand-yellow/60 hover:shadow-lift sm:flex-row sm:items-center sm:gap-5 sm:p-6 ${
        past ? "opacity-70" : ""
      }`}
    >
      {/* Date badge — compact grouped row on mobile, vertical column on desktop */}
      <div
        className={`flex shrink-0 items-baseline gap-2 sm:w-[92px] sm:flex-col sm:items-center sm:gap-0 ${
          past ? "text-brand-green-dark/50" : "text-brand-green"
        }`}
      >
        <span className="text-4xl font-extrabold leading-none sm:text-5xl">{badge.day}</span>
        <span className="text-sm font-bold uppercase tracking-wide sm:mt-1">{badge.month}</span>
        <span className="text-xs font-semibold text-brand-green-dark/55 sm:mt-1">
          {webinar.time} TSİ
        </span>
      </div>

      <div aria-hidden className="mt-1 h-px w-full bg-brand-green/10 sm:mt-0 sm:h-auto sm:w-px sm:self-stretch sm:bg-brand-green/15" />

      {/* Speaker + content */}
      <div className="flex flex-1 items-start gap-4">
        <div className="flex shrink-0 flex-col gap-4">
          {(webinarSpeakers[webinar.slug] ?? [{ name: webinar.speaker }]).map((s, i) => (
            <SpeakerAvatar
              key={i}
              speaker={s.name}
              photo={s.photo}
              objectPosition={s.objectPosition}
              grayed={past}
            />
          ))}
        </div>
        <div className="min-w-0 flex-1">
          <div className="mb-2 flex flex-wrap items-center gap-2">
            <span className="rounded-full bg-brand-green/10 px-2.5 py-1 text-xs font-bold text-brand-green">
              {webinar.audience}
            </span>
            {past ? (
              <span className="rounded-full bg-brand-green-dark/10 px-2.5 py-1 text-xs font-bold text-brand-green-dark/60">
                Tamamlandı
              </span>
            ) : webinar.openToAll ? (
              <span className="rounded-full bg-brand-yellow px-2.5 py-1 text-xs font-extrabold text-brand-green-dark">
                HERKESE AÇIK, ÜCRETSİZ!
              </span>
            ) : null}
          </div>

          <h3 className="text-base font-extrabold leading-snug text-brand-green-dark sm:text-lg">
            {webinar.openToAll ? (
              <Link to={`/webinar/${webinar.slug}`} className="hover:underline">
                {webinar.title}
              </Link>
            ) : (
              webinar.title
            )}
          </h3>
          <p className="mt-1 text-sm font-medium text-brand-green-dark/70">{webinar.speaker}</p>
          <p className="mt-0.5 hidden text-xs text-brand-green-dark/55 sm:block">{formatWebinarDate(webinar)}</p>

          {!past && webinar.openToAll && (
            <div className="mt-4 flex flex-col gap-2 sm:flex-row sm:items-center">
              <button
                type="button"
                onClick={() => trackAndRedirect(webinar.slug, webinar.whatsappUrl)}
                className="btn-whatsapp sm:w-auto sm:px-6"
              >
                <WhatsAppIcon size={18} />
                WhatsApp Grubuna Katıl
              </button>
              <Link
                to={`/webinar/${webinar.slug}`}
                className="inline-flex items-center justify-center gap-1 rounded-xl px-4 py-3 text-sm font-bold text-brand-green transition-colors hover:bg-brand-green/5 sm:py-3"
              >
                Detayları Gör <span aria-hidden>→</span>
              </Link>
            </div>
          )}

          {!past && !webinar.openToAll && (
            <p className="mt-3 text-xs font-semibold text-brand-green-dark/55">
              Bu oturum yalnızca AUSCAMP danışanlarına açıktır.
            </p>
          )}
        </div>
      </div>
    </article>
  );
}

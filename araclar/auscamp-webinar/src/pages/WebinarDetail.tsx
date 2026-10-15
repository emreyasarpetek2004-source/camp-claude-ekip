import { useEffect } from "react";
import { Link, Navigate, useParams } from "react-router-dom";
import { webinars } from "../config/webinars";
import { webinarSpeakers } from "../config/speakers";
import { webinarHighlights } from "../config/webinarDetails";
import { formatWebinarDate, isPast, webinarInstant } from "../lib/dates";
import { trackAndRedirect } from "../lib/tracking";
import { useDocumentMeta } from "../lib/seo";
import BackgroundVideo from "../components/BackgroundVideo";
import CountdownTimer from "../components/CountdownTimer";
import HowItWorks from "../components/HowItWorks";
import Footer from "../components/Footer";
import InfoForm from "../components/InfoForm";
import SiteHeader from "../components/SiteHeader";
import SpeakerAvatar from "../components/SpeakerAvatar";
import Reveal from "../components/Reveal";
import { CalendarIcon, CheckIcon, WhatsAppIcon } from "../components/icons";

export default function WebinarDetail() {
  const { slug } = useParams<{ slug: string }>();
  const webinar = webinars.find((w) => w.slug === slug);

  // Fire a per-webinar ViewContent so ad interest is measurable per page.
  useEffect(() => {
    if (webinar && typeof window.fbq === "function") {
      window.fbq("track", "ViewContent", { content_name: webinar.slug });
    }
  }, [webinar]);

  useDocumentMeta(
    webinar
      ? `${webinar.title} | AUSCAMP Webinar`
      : "Webinar | AUSCAMP",
    webinar
      ? `${formatWebinarDate(webinar)} — ${webinar.audience}.${webinar.openToAll ? " Ücretsiz." : ""} WhatsApp grubuna katıl, katılım linki grupta paylaşılsın.`
      : undefined
  );

  if (!webinar) return <Navigate to="/" replace />;

  const past = isPast(webinar);
  const speakers = webinarSpeakers[webinar.slug] ?? [
    { name: webinar.speaker },
  ];
  const highlights = webinarHighlights[webinar.slug] ?? [];

  const join = () => trackAndRedirect(webinar.slug, webinar.whatsappUrl);

  return (
    <div className="flex min-h-screen w-full flex-col">
      <SiteHeader />
      <main className="flex-1">
        {/* HERO */}
        <header className="relative isolate overflow-hidden px-5 pb-12 pt-28 sm:pt-32">
          <BackgroundVideo />

          <div className="relative mx-auto max-w-2xl">
            <Link
              to="/"
              className="inline-flex items-center gap-1 text-sm font-semibold text-brand-cream/80 transition hover:text-white"
            >
              <span aria-hidden>←</span> Tüm webinarlar
            </Link>

            <div className="mt-6 flex flex-wrap items-center gap-2">
              <span className="rounded-full bg-white/10 px-3 py-1 text-xs font-bold text-brand-cream">
                {webinar.audience}
              </span>
              {past ? (
                <span className="rounded-full bg-white/10 px-3 py-1 text-xs font-bold text-brand-cream/70">
                  Tamamlandı
                </span>
              ) : webinar.openToAll ? (
                <span className="rounded-full bg-brand-yellow px-3 py-1 text-xs font-extrabold text-brand-green-dark">
                  HERKESE AÇIK, ÜCRETSİZ!
                </span>
              ) : null}
            </div>

            <h1 className="mt-4 text-2xl font-extrabold leading-tight tracking-tight text-white sm:text-4xl">
              {webinar.title}
            </h1>

            <p className="mt-3 flex items-center gap-2 text-base font-medium text-brand-cream/90">
              <CalendarIcon className="text-brand-yellow" size={18} />
              {formatWebinarDate(webinar)}
            </p>

            <div className="mt-8 rounded-3xl border border-white/10 bg-white/5 p-6 backdrop-blur-sm">
              {past ? (
                <p className="text-center text-sm font-semibold text-brand-cream/85">
                  Bu webinar tamamlandı. Gelecek webinarlar için topluluğa katıl.
                </p>
              ) : (
                <CountdownTimer
                  target={webinarInstant(webinar).getTime()}
                  label="Webinara kalan süre"
                />
              )}

              {!past && webinar.openToAll && (
                <button
                  type="button"
                  onClick={join}
                  className="btn-whatsapp cta-pulse mt-6 py-4 text-base"
                >
                  <WhatsAppIcon />
                  WhatsApp Grubuna Katıl
                </button>
              )}
              <p className="mt-3 text-center text-xs text-brand-cream/70">
                {past
                  ? "Gelecek webinarlar için ana sayfadaki topluluğa katıl."
                  : webinar.openToAll
                    ? "Katılım linki webinar günü grupta paylaşılır. Kayıt formu yok."
                    : "Bu oturum yalnızca AUSCAMP danışanlarına açıktır. Katılım bilgisi danışan kanallarından paylaşılır."}
              </p>
            </div>
          </div>
        </header>

        {/* SPEAKERS */}
        <Reveal className="px-5 py-8 sm:py-10">
          <div className="mx-auto max-w-2xl">
            <h2 className="section-title text-center">
              {speakers.length > 1 ? "Konuşmacılar" : "Konuşmacı"}
            </h2>
            <div className="mt-7 flex flex-col gap-4">
              {speakers.map((s) => (
                <div
                  key={s.name}
                  className="flex flex-col items-center gap-4 rounded-3xl bg-white p-6 text-center text-brand-green-dark shadow-card sm:flex-row sm:items-start sm:text-left"
                >
                  <SpeakerAvatar
                    speaker={s.name}
                    photo={s.photo}
                    objectPosition={s.objectPosition}
                    size="xl"
                  />
                  <div className="min-w-0 flex-1">
                    <h3 className="text-lg font-extrabold text-brand-green-dark">{s.name}</h3>
                    {s.title && (
                      <p className="mt-0.5 text-sm font-semibold text-brand-green">{s.title}</p>
                    )}
                    {s.bio && (
                      <p className="mt-3 text-sm leading-relaxed text-brand-green-dark/75">
                        {s.bio}
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </Reveal>

        {/* HIGHLIGHTS */}
        {highlights.length > 0 && (
          <Reveal className="px-5 py-8 sm:py-10">
            <div className="mx-auto max-w-2xl">
              <h2 className="section-title text-center">Neler Konuşulacak?</h2>
              <ul className="mx-auto mt-7 flex max-w-xl flex-col gap-3">
                {highlights.map((h) => (
                  <li
                    key={h}
                    className="flex items-start gap-3 rounded-2xl border border-white/10 bg-white/5 p-4"
                  >
                    <span className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-brand-yellow text-brand-green-dark">
                      <CheckIcon size={14} />
                    </span>
                    <span className="text-sm leading-relaxed text-brand-cream/90">{h}</span>
                  </li>
                ))}
              </ul>
            </div>
          </Reveal>
        )}

        <HowItWorks />

        {/* FINAL CTA — yalnız herkese açık oturumlarda */}
        {!past && webinar.openToAll && (
          <Reveal className="px-5 py-8 sm:py-10">
            <div className="mx-auto max-w-2xl rounded-3xl bg-brand-yellow p-7 text-center text-brand-green-dark sm:p-9">
              <h2 className="text-2xl font-extrabold tracking-tight sm:text-3xl">
                Yerini ayırt, ücretsiz.
              </h2>
              <p className="mx-auto mt-2 max-w-md text-sm font-medium text-brand-green-dark/80">
                WhatsApp grubuna katıl; hatırlatmalar ve canlı yayın linki seninle
                doğrudan paylaşılsın.
              </p>
              <button
                type="button"
                onClick={join}
                className="btn-whatsapp mx-auto mt-6 max-w-sm py-4 text-base"
              >
                <WhatsAppIcon />
                WhatsApp Grubuna Katıl
              </button>
            </div>
          </Reveal>
        )}

        <Reveal>
          <InfoForm
            groupUrl={webinar.openToAll ? webinar.whatsappUrl : undefined}
            groupContentName={webinar.slug}
          />
        </Reveal>
      </main>
      <Footer />
    </div>
  );
}

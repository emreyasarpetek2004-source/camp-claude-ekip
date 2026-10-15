import { communityUrl } from "../config/webinars";
import { trackAndRedirect } from "../lib/tracking";
import BackgroundVideo from "./BackgroundVideo";
import { CalendarIcon, ClockIcon, GlobeIcon } from "./icons";

export default function Hero() {
  return (
    <header className="relative isolate flex min-h-[92vh] flex-col justify-center overflow-hidden px-5 pb-16 pt-28 sm:pt-32">
      <BackgroundVideo />

      <div className="relative mx-auto flex max-w-2xl flex-col items-center text-center">
        <p className="eyebrow animate-fade-up">
          Ücretsiz webinar serisi
        </p>

        <h1 className="mt-5 font-extrabold leading-[1.08] tracking-tight text-white">
          <span className="block text-[2.5rem] sm:text-5xl md:text-[3.4rem]">
            Avustralya&apos;da Doktorluk
          </span>
          <span className="mt-3 block">
            <span className="highlight-bar text-4xl leading-relaxed sm:text-5xl">
              Webinar Takvimi
            </span>
          </span>
        </h1>

        <p className="mt-7 max-w-xl text-base leading-relaxed text-brand-cream sm:text-lg">
          CV ve iş başvurularından{" "}
          <strong className="font-semibold text-white">uzmanlık denkliğine</strong>{" "}
          kadar; alanında uzman hekimlerle canlı oturumlar.
        </p>

        {/* Info chips — clean, informative (DEUCAMP-style), not decorative glass */}
        <div className="mt-7 flex flex-wrap items-center justify-center gap-2.5">
          <span className="info-chip">
            <CalendarIcon size={16} />
            4–25 Ekim 2026
          </span>
          <span className="info-chip">
            <ClockIcon size={16} />
            13.00 TSİ
          </span>
          <span className="info-chip">
            <GlobeIcon size={16} />
            Online · Ücretsiz
          </span>
        </div>

        <button
          type="button"
          onClick={() => trackAndRedirect("duyuru-toplulugu", communityUrl)}
          className="btn-primary cta-pulse mt-9"
        >
          Duyuru Topluluğuna Katıl
          <span aria-hidden>→</span>
        </button>

        <p className="mt-4 text-sm text-brand-cream/75">
          Tüm webinar duyuruları ve katılım linkleri toplulukta paylaşılır.
        </p>
      </div>

      <div className="relative mx-auto mt-14 flex justify-center">
        <a href="#webinarlar" className="text-xs font-semibold tracking-widest text-brand-cream/60 transition hover:text-brand-cream">
          EKİM TAKVİMİ ↓
        </a>
      </div>
    </header>
  );
}

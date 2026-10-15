import { communityUrl } from "../config/webinars";
import { trackAndRedirect } from "../lib/tracking";
import LogoCard from "./LogoCard";

const WHATSAPP_TEL = "+90 552 253 03 37";
const WHATSAPP_HREF = "https://wa.me/905522530337";
const INSTAGRAM_HREF = "https://instagram.com/auscamp";
const SITE_HREF = "https://auscamp.com.tr";

export default function Footer() {
  return (
    <footer className="mt-6 border-t border-white/10 px-5 py-10">
      <div className="mx-auto flex max-w-2xl flex-col items-center gap-6 text-center">
        <LogoCard />

        <p className="max-w-md text-sm leading-relaxed text-brand-cream/80">
          AUSCAMP, Avustralya'da tıp kariyeri kurmak isteyen Türk hekimlere uçtan
          uca danışmanlık sunar.
        </p>

        <button
          type="button"
          onClick={() => trackAndRedirect("duyuru-toplulugu-footer", communityUrl)}
          className="btn-primary"
        >
          Duyuru Topluluğuna Katıl
          <span aria-hidden>→</span>
        </button>

        <div className="flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-sm">
          <a
            href={SITE_HREF}
            target="_blank"
            rel="noopener noreferrer"
            className="font-semibold text-brand-yellow hover:underline"
          >
            auscamp.com.tr
          </a>
          <a
            href={WHATSAPP_HREF}
            target="_blank"
            rel="noopener noreferrer"
            className="text-brand-cream/85 hover:text-white"
          >
            WhatsApp {WHATSAPP_TEL}
          </a>
          <a
            href={INSTAGRAM_HREF}
            target="_blank"
            rel="noopener noreferrer"
            className="text-brand-cream/85 hover:text-white"
          >
            @auscamp
          </a>
        </div>

        <p className="text-xs text-brand-cream/50">
          © {new Date().getFullYear()} AUSCAMP. Tüm hakları saklıdır.
        </p>
      </div>
    </footer>
  );
}

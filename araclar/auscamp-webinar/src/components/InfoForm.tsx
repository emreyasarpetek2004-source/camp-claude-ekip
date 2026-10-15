import { useEffect, useState } from "react";
import { trackAndRedirect } from "../lib/tracking";
import { WhatsAppIcon } from "./icons";

/**
 * "Bilgi Al" — a native, branded form that submits directly to the AUSCAMP
 * Google Form's formResponse endpoint (responses still land in the same Google
 * Sheet). Native instead of an <iframe> embed because Google Forms embeds render
 * blank when browsers block third-party storage. No iframe → always works.
 */
const FORM_ACTION =
  "https://docs.google.com/forms/d/e/<FORM_ID>/formResponse";

const CHOICES = [
  {
    key: "entry.531207248",
    label: "Mevcut mesleki durumunuz nedir?",
    options: [
      "Uzman Hekim", "Pratisyen Hekim", "Asistan Hekim", "Tıp Öğrencisi",
      "Uzman Diş Hekimi", "Pratisyen Diş Hekimi", "Asistan Diş Hekimi", "Diş Hekimliği Öğrencisi",
    ],
  },
  {
    key: "entry.1998664040",
    label: "Hangi alan sizi daha çok ilgilendiriyor?",
    options: ["Avustralya'da Doktorluk", "Avustralya'da Diş Hekimliği (ADC süreci)", "Yeni Zelanda'da Doktorluk"],
  },
  {
    key: "entry.1065477664",
    label: "Avustralya'da kariyer hedefleriniz hakkında mevcut bilgi durumunuz nedir?",
    options: ["Ciddi şekilde ilgileniyorum, yol haritası arıyorum.", "Sadece merak ediyorum, genel bilgi istiyorum."],
  },
  {
    key: "entry.1481470500",
    label: "İngilizce seviyeniz?",
    options: ["Başlangıç (A1-A2)", "Orta (B1-B2)", "İleri (C1-C2)"],
  },
];
const TEXT_FIELDS = [
  { key: "entry.223450296", label: "Ad Soyad", type: "text", placeholder: "Adınız Soyadınız", autoComplete: "name" },
  { key: "entry.6148850", label: "Telefon Numarası", type: "tel", placeholder: "05xx xxx xx xx", autoComplete: "tel" },
  { key: "entry.1997639038", label: "E-posta", type: "email", placeholder: "ornek@eposta.com", autoComplete: "email" },
];

interface InfoFormProps {
  /** "Webinar grubuna katıl" butonunun WhatsApp linki; verilmezse buton gösterilmez. */
  groupUrl?: string;
  /** Lead olayındaki content_name (webinar slug'ı ya da topluluk CTA'sı). */
  groupContentName?: string;
}

export default function InfoForm({ groupUrl, groupContentName = "bilgi-kutusu" }: InfoFormProps) {
  const [open, setOpen] = useState(false);
  const [values, setValues] = useState<Record<string, string>>({});
  const [error, setError] = useState("");
  const [sent, setSent] = useState(false);
  const [sending, setSending] = useState(false);

  // Menüdeki "/#bilgi" linki paneli açık getirsin.
  useEffect(() => {
    const sync = () => {
      if (window.location.hash === "#bilgi") setOpen(true);
    };
    sync();
    window.addEventListener("hashchange", sync);
    return () => window.removeEventListener("hashchange", sync);
  }, []);

  const set = (k: string, v: string) => setValues((s) => ({ ...s, [k]: v }));

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const required = [...CHOICES.map((c) => c.key), ...TEXT_FIELDS.map((t) => t.key)];
    const missing = required.some((k) => !values[k]?.trim());
    if (missing) {
      setError("Lütfen tüm alanları doldurun.");
      return;
    }
    setError("");
    setSending(true);
    const body = new URLSearchParams();
    Object.entries(values).forEach(([k, v]) => body.append(k, v));
    try {
      await fetch(FORM_ACTION, {
        method: "POST",
        mode: "no-cors",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: body.toString(),
      });
    } catch {
      // no-cors resolves opaque; a throw means network error, but the POST
      // usually still reaches Google — treat as sent to avoid double entries.
    }
    if (typeof window.fbq === "function") window.fbq("track", "Lead", { content_name: "bilgi-formu" });
    setSending(false);
    setSent(true);
  };

  return (
    <section id="bilgi" className="bg-brand-cream px-5 py-12 text-brand-green-dark sm:py-16">
      <div className="mx-auto max-w-3xl">
        <div className="rounded-3xl bg-white p-4 shadow-lift sm:p-5">
          <div className="flex flex-col gap-3 md:flex-row md:items-center md:gap-5">
            <button
              type="button"
              onClick={() => setOpen((o) => !o)}
              aria-expanded={open}
              aria-controls="bilgi-panel"
              className="flex flex-1 items-center justify-between gap-4 rounded-2xl border border-brand-green-dark/15 px-4 py-3.5 text-left transition hover:border-brand-green/50"
            >
              <span>
                <span className="block text-base font-bold text-brand-green-dark">Süreç hakkında bilgi al</span>
                <span className="mt-1 block text-sm text-brand-green-dark/65">
                  Avustralya'da doktorluk için yol haritanı birlikte netleştirelim.
                </span>
              </span>
              <svg
                width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden
                className={`shrink-0 text-brand-green-dark/70 transition-transform duration-200 ${open ? "rotate-180" : ""}`}
              >
                <path d="m6 9 6 6 6-6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </button>
            {groupUrl && (
              <button
                type="button"
                onClick={() => trackAndRedirect(groupContentName, groupUrl)}
                className="btn-whatsapp shrink-0 md:w-auto md:px-7"
              >
                <WhatsAppIcon size={18} />
                Webinar grubuna katıl
              </button>
            )}
          </div>

          {open && (
            <div id="bilgi-panel" className="mt-5">
        {sent ? (
          <div className="rounded-3xl bg-brand-cream/40 p-10 text-center shadow-lift">
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-brand-green text-white">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" aria-hidden>
                <path d="M20 6 9 17l-5-5" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </div>
            <h3 className="mt-5 text-xl font-extrabold text-brand-green-dark">Teşekkürler! Başvurunuz alındı.</h3>
            <p className="mt-2 text-sm text-brand-green-dark/70">
              Ekibimiz en kısa sürede sizinle iletişime geçecek. Bu arada duyuru topluluğumuza da katılabilirsiniz.
            </p>
          </div>
        ) : (
          <form onSubmit={onSubmit} className="space-y-7 px-1 pb-2 sm:px-3">
            {CHOICES.map((q) => (
              <fieldset key={q.key}>
                <legend className="mb-3 text-sm font-bold text-brand-green-dark">
                  {q.label} <span className="text-brand-yellow-deep">*</span>
                </legend>
                <div className="flex flex-wrap gap-2">
                  {q.options.map((opt) => {
                    const active = values[q.key] === opt;
                    return (
                      <button
                        type="button"
                        key={opt}
                        onClick={() => set(q.key, opt)}
                        className={`rounded-full border px-4 py-2 text-sm font-medium transition ${
                          active
                            ? "border-brand-green bg-brand-green text-white"
                            : "border-brand-green-dark/15 bg-white text-brand-green-dark/80 hover:border-brand-green/50"
                        }`}
                      >
                        {opt}
                      </button>
                    );
                  })}
                </div>
              </fieldset>
            ))}

            <div className="grid gap-5 sm:grid-cols-2">
              {TEXT_FIELDS.map((f) => (
                <div key={f.key} className={f.type === "text" ? "sm:col-span-2" : ""}>
                  <label className="mb-1.5 block text-sm font-bold text-brand-green-dark">
                    {f.label} <span className="text-brand-yellow-deep">*</span>
                  </label>
                  <input
                    type={f.type}
                    value={values[f.key] ?? ""}
                    onChange={(e) => set(f.key, e.target.value)}
                    placeholder={f.placeholder}
                    autoComplete={f.autoComplete}
                    className="w-full rounded-xl border border-brand-green-dark/15 bg-brand-cream/40 px-4 py-3 text-brand-green-dark outline-none transition placeholder:text-brand-green-dark/40 focus:border-brand-green focus:bg-white focus:ring-2 focus:ring-brand-green/20"
                  />
                </div>
              ))}
            </div>

            {error && <p className="text-sm font-semibold text-red-600">{error}</p>}

            <button type="submit" disabled={sending} className="btn-primary w-full disabled:opacity-60">
              {sending ? "Gönderiliyor…" : "Bilgi Al"}
              {!sending && <span aria-hidden>→</span>}
            </button>
            <p className="text-center text-xs text-brand-green-dark/55">
              Bilgileriniz yalnızca sizinle iletişim için kullanılır.
            </p>
          </form>
        )}
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

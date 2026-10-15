const FAQS = [
  {
    q: "Webinarlar ücretsiz mi?",
    a: "\"Herkese açık, ücretsiz\" etiketli webinarlar için evet: ödeme ya da üyelik gerekmez, WhatsApp grubuna katılman yeterli. Takvimdeki bazı oturumlar ise yalnızca AUSCAMP danışanlarına özeldir; onların katılım bilgisi danışan kanallarından paylaşılır.",
  },
  {
    q: "Kayıt olmam gerekiyor mu?",
    a: "Ayrı bir kayıt formu doldurmana gerek yok. İlgilendiğin webinarın WhatsApp grubuna katılman yeterli; tüm bilgilendirme grup üzerinden yapılır.",
  },
  {
    q: "Katılım linkine nasıl ulaşırım?",
    a: "Webinar günü canlı yayın (Zoom/online) katılım linki, ilgili WhatsApp grubunda seninle paylaşılır. Bu yüzden gruba katılmak yeterlidir.",
  },
  {
    q: "Canlı katılamazsam kaydı olur mu?",
    a: "Mümkün olduğunda webinar kaydı ilgili grupta paylaşılır. Canlı katılamasan da grupta kalarak kayda ve materyallere erişebilirsin.",
  },
  {
    q: "Kimler katılabilir?",
    a: "Her kartta hedef kitle yazılıdır. \"Tüm Hekimlere Açık\" oturumlara herkes katılabilir. \"AUSCAMP Danışanlarına Özel\" oturumlar ise yalnızca danışanlarımıza yöneliktir; bu oturumlarda katılım butonu bulunmaz.",
  },
];

export default function FAQ() {
  return (
    <section id="sss" className="px-5 py-12 sm:py-16">
      <div className="mx-auto max-w-2xl">
        <div className="flex flex-col items-center text-center">
          <p className="section-eyebrow">Sık Sorulanlar</p>
          <h2 className="section-heading text-white">Merak edilenler</h2>
          <span className="section-rule" />
        </div>
        <div className="mt-10 flex flex-col gap-3">
          {FAQS.map((item, i) => (
            <details
              key={i}
              className="group rounded-2xl border border-white/10 bg-white/5 p-1 [&_summary::-webkit-details-marker]:hidden"
            >
              <summary className="flex cursor-pointer list-none items-center justify-between gap-4 p-4 font-semibold text-white">
                <span>{item.q}</span>
                <span
                  aria-hidden
                  className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-brand-yellow text-brand-green-dark transition-transform duration-200 group-open:rotate-45"
                >
                  +
                </span>
              </summary>
              <p className="px-4 pb-4 text-sm leading-relaxed text-brand-cream/85">
                {item.a}
              </p>
            </details>
          ))}
        </div>
      </div>
    </section>
  );
}

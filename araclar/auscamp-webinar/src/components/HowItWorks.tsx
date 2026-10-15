const STEPS = [
  {
    n: "1",
    title: "WhatsApp grubuna katıl",
    desc: "İlgilendiğin webinarın grubuna tek dokunuşla katıl. Kayıt formu yok.",
  },
  {
    n: "2",
    title: "Hatırlatma mesajlarını al",
    desc: "Webinar öncesi hatırlatmalar ve içerik grubuna düşer, kaçırmazsın.",
  },
  {
    n: "3",
    title: "Katılım linki grupta paylaşılır",
    desc: "Webinar günü canlı yayın linki doğrudan grupta seninle paylaşılır.",
  },
];

export default function HowItWorks() {
  return (
    <section id="nasil" className="px-5 py-12 sm:py-16">
      <div className="mx-auto max-w-2xl">
        <div className="flex flex-col items-center text-center">
          <p className="section-eyebrow">Webinara Nasıl Katılırım?</p>
          <h2 className="section-heading text-white">Üç adımda katıl</h2>
          <span className="section-rule" />
        </div>
        <div className="mt-10 grid gap-4 sm:grid-cols-3">
          {STEPS.map((s) => (
            <div
              key={s.n}
              className="rounded-2xl border border-white/10 bg-white/5 p-5 text-center"
            >
              <span className="mx-auto flex h-11 w-11 items-center justify-center rounded-full bg-brand-yellow text-lg font-extrabold text-brand-green-dark">
                {s.n}
              </span>
              <h3 className="mt-3 font-bold text-white">{s.title}</h3>
              <p className="mt-1.5 text-sm leading-relaxed text-brand-cream/80">
                {s.desc}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

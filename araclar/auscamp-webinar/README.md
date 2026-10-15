# AUSCAMP Webinar Landing Page

Türkçe, mobil öncelikli webinar açılış sayfası. Instagram/Facebook reklamlarından
gelen hekimleri AUSCAMP'in Temmuz 2026 webinar takvimine ve WhatsApp topluluklarına
yönlendirir. Tüm CTA'lar Meta Pixel'e `Lead` olayı düşürür.

- **Stack:** Vite + React + TypeScript + Tailwind CSS + React Router
- **Yayın:** Vercel → `webinar.auscamp.com.tr`
- **Analitik:** yalnızca Meta Pixel (`1489409728980211`)

### Sayfalar (her reklam kendi sayfasına)

| Sayfa | URL | Açıklama |
|-------|-----|----------|
| Ana sayfa | `/` | Hero + geri sayım + tüm webinar kartları + SSS |
| Webinar detay | `/webinar/<slug>` | O webinara özel: detay, hoca bilgisi, geri sayım, WhatsApp CTA |

Her webinarın reklamını kendi detay sayfasına yönlendir. Slug'lar
`src/config/webinars.ts` içindedir, örn:
`https://webinar.auscamp.com.tr/webinar/genel-cerrahi-12-tem`

Pixel: her sayfa yüklemesinde/geçişinde **PageView**, detay sayfası açılışında
ayrıca **ViewContent** (`content_name = slug`) → hangi webinarın ilgi çektiğini
Meta'da webinar bazında ölçebilirsin.

---

## 1. Yerelde çalıştırma

Bu makinede `bun` kurulu (Node yerine de kullanılabilir). İkisi de çalışır:

```bash
# bun ile (bu makinede kurulu)
bun install
bun run dev        # http://localhost:5173

# veya npm ile (Node 18+ gerekir)
npm install
npm run dev
```

Derleme (tip kontrolü + prod build):

```bash
bun run build      # veya: npm run build
bun run preview    # derlenmiş çıktıyı önizle
```

Çıktı `dist/` klasörüne üretilir.

---

## 2. Vercel'e yayınlama

Sayfa Vercel tarafından otomatik algılanır (`vercel.json` mevcut).

**İlk kurulum:**

1. Bu klasörü bir Git deposu yapıp GitHub'a push'la.
2. Vercel'de **New Project → Import** ile depoyu seç.
3. Framework otomatik "Vite" gelir. Build ayarı: `npm run build`, çıktı: `dist`.
4. Deploy'a bas.

**Özel alan adı (`webinar.auscamp.com.tr`):**

1. Vercel projesinde **Settings → Domains → Add** ile `webinar.auscamp.com.tr` ekle.
2. Alan adı sağlayıcında Vercel'in verdiği `CNAME` kaydını gir.
3. SSL otomatik gelir.

**CLI ile (alternatif):**

```bash
npm i -g vercel
vercel        # önizleme
vercel --prod # canlı
```

---

## 3. Webinar listesini düzenleme

Tüm webinar verisi tek dosyada: **`src/config/webinars.ts`**.

Her webinar bir nesne:

```ts
{
  slug: "genel-cerrahi-12-tem",          // benzersiz kimlik (pixel content_name)
  date: "2026-07-12",                     // YYYY-MM-DD
  time: "13.00",                          // TSİ (Türkiye saati, UTC+3)
  title: "Genel Cerrahlara Özel: ...",
  audience: "Genel Cerrahlara Özel",      // karttaki rozet
  speaker: "Doç. Dr. İbrahim Ethem Cakcak",
  whatsappUrl: "https://chat.whatsapp.com/..."   // gruba katıl linki
}
```

- **Webinar eklemek:** listeye yeni bir nesne ekle. Sıralama ve geri sayım otomatik.
- **Webinar çıkarmak:** ilgili nesneyi sil.
- **Geçmiş webinar:** tarihi bugünden eskiyse kart otomatik gri "Tamamlandı" olur,
  CTA gizlenir. Elle bir şey yapmana gerek yok.
- **Topluluk linki:** üstteki `communityUrl` (hero + footer ana CTA).

### Konuşmacı bilgisi + fotoğrafı

`webinars.ts` sade kalsın diye konuşmacı profilleri ayrı dosyada:
**`src/config/speakers.ts`** (slug → konuşmacı listesi). Her profilde ad, unvan,
foto ve kısa bio var:

```ts
"genel-cerrahi-12-tem": [
  {
    name: "Doç. Dr. İbrahim Ethem Cakcak",
    title: "Genel Cerrahi Uzmanı",
    photo: "/speakers/ethem.jpg",   // public/speakers/ altına koy
    objectPosition: "50% 15%",       // boy fotoğrafı için kırpma ayarı
    bio: "…",
  },
],
```

Foto yoksa kart/detay otomatik baş harf gösterir. Bir webinarda iki konuşmacı
olabilir (dizi). Bio'ları gerçek özgeçmiş bilgileriyle zenginleştirebilirsin.

### Webinar detay içeriği (ajanda)

Detay sayfasındaki "Neler Konuşulacak?" maddeleri **`src/config/webinarDetails.ts`**
içinde, slug → madde listesi olarak durur. Serbestçe düzenle.

### Arka plan videosu (Sydney)

Hero'larda arka planda **Sydney Opera Binası videosu** oynar (Pexels, ticari
kullanıma uygun, atıf gerekmez). Aktif dosya:

```
public/videos/sydney.mp4                 # aktif (Opera + Harbour Bridge, ~7.3 MB)
public/videos/sydney-alt-cinematic.mp4   # alternatif (daha hafif ~2.9 MB, sinematik)
```

Alternatife geçmek için: `sydney.mp4`'i sil, `sydney-alt-cinematic.mp4`'i
`sydney.mp4` olarak yeniden adlandır. Kendi videonu koymak istersen aynı isimle
(`public/videos/sydney.mp4`) değiştir. Video yoksa hero yine şık görünür
(marka-yeşili degrade fallback). Üstteki koyu yeşil overlay markayı ve metin
okunabilirliğini korur.

---

## 4. Meta Pixel'i doğrulama

Pixel ID `1489409728980211`, `index.html` içine gömülüdür ve sayfa açılışında
`PageView` gönderir. CTA'lar `src/lib/tracking.ts` üzerinden `Lead` gönderir
(`content_name` + `utm_source` / `utm_campaign` / `utm_content`).

**Meta Events Manager → Test Events ile test:**

1. [Events Manager](https://business.facebook.com/events_manager2) → ilgili pixel → **Test Events**.
2. "Website URL" alanına canlı adresi (veya yerelde `http://localhost:5173`) gir.
3. Sayfa açılınca **PageView** olayı düşmeli.
4. Bir CTA'ya (ör. "WhatsApp Grubuna Katıl") tıkla → **Lead** olayı, `content_name`
   ve UTM parametreleriyle görünmeli.
5. UTM'leri test etmek için adrese `?utm_source=test&utm_campaign=deneme&utm_content=v1`
   ekleyip CTA'ya bas; parametreler olay detayında görünür.

> İpucu: Reklam engelleyiciler pixel'i durdurabilir. Test için engelleyiciyi kapat.
> Kod, pixel yüklenmese bile kullanıcıyı yine de hedefe yönlendirir (asla takılmaz).

---

## Proje yapısı

```
index.html              # Meta Pixel + Türkçe meta/OG etiketleri
src/
  App.tsx               # router: / (Home) ve /webinar/:slug (WebinarDetail)
  pages/Home.tsx
  pages/WebinarDetail.tsx
  config/webinars.ts    # TEK veri kaynağı (webinarlar + topluluk linki)
  config/speakers.ts    # konuşmacı profilleri (foto + unvan + bio)
  config/webinarDetails.ts  # detay sayfası ajandası
  lib/tracking.ts       # trackAndRedirect (Lead + yönlendirme)
  lib/dates.ts          # TSİ tarih/format yardımcıları
  lib/seo.ts            # sayfa başına title/description
  hooks/useCountdown.ts # geri sayım (flash yok)
  components/           # Hero, Countdown(Timer), WebinarCard, BackgroundVideo,
                        # Reveal, PixelTracker, HowItWorks, FAQ, Footer, icons
public/
  auscamp-logo.png
  speakers/             # ethem.jpg, fidan.jpg, tugba.jpg
  videos/               # sydney.mp4 (opsiyonel, sen eklersin)
  og.jpg                # sosyal paylaşım görseli
references/             # tasarım referansları (deploy'a dahil değil)
```

# CAMP GROUP: Claude Code Sistemleri ve Otomasyonlar

Hazırlayan: Emre Yaşar Petek (AUSCAMP Marketing Koordinatörü)
Tarih: 10 Ekim 2026

Bu belge, Claude Code üzerinde kurulu olan tüm proje, ajan (agent), skill ve otomasyonları tek yerde toplar. Amaç: ekipte kimin neyi isteyebileceğini, hangi işin otomatik yürüdüğünü ve hangi kuralla çalıştığını görmesi.

> Not: Şifre, token ve API anahtarları bu repoda yer almaz; Marketing Koordinatöründen (Emre) ayrıca alınır.

> **Ekip sürümü.** Bu repo CAMP GROUP ekibi için hazırlanmış paylaşılabilir sürümdür. Kişisel bilgiler çıkarıldı: ajan ve kurallarda onay/karar artık skill'i çalıştıran **kullanıcıya** aittir. Kişisel veri, reklam hesabı verisi ve lisanslı ders içeriği taşıyan araçlar (auscamp-memnuniyet, camp-wa-core, camp-lead-crm, meta-ads-rapor, campverse-slides, ukcamp-rehber) ile Meta reklam otomasyon klasörleri bu sürümde yer almaz; aşağıda yalnızca tanım olarak geçerler. Telefon numaraları ve Asana/Meta kimlikleri `<...>` yer tutucularıyla değiştirildi.

**Kendi bilgisayarınıza kurmak için: [KURULUM.md](KURULUM.md)**

### Repo yapısı

| Klasör | İçerik |
|---|---|
| `claude/agents/` | 37 ajan (3 marka içerik ekibi, video, reels, slayt, denetçiler) |
| `claude/skills/` | Kendi skill'lerimiz |
| `CLAUDE.md` | Ortak çalışma kuralları (Claude her oturumda okur) |
| `bilgi-bankasi/` | AUSCAMP / UKCAMP / DENTCAMP bilgi bankaları + Instagram ve Meta reklam otomasyon scriptleri |
| `araclar/` | Araçların kaynak kodu (camp-reels, camp-video, camp-caption, katalog, webinar sitesi) |
| `kur.sh` | Hepsini doğru yerlere kopyalayan kurulum scripti |

---

## 1. Genel Bakış

| Alan | Ne yapar | Durum |
|---|---|---|
| Sosyal medya içerik sistemi (3 marka) | Fikir → brief → Asana task → caption → Instagram yayını | Aktif (AUSCAMP, UKCAMP, DENTCAMP) |
| Instagram yayın otomasyonu | Make üzerinden tek görsel / carousel / reels yayını | Aktif, 3 marka |
| CAMP REELS | Webinar kaydından premium reels üretimi | Aktif |
| CAMPVERSE video hattı | Loom ders kayıtlarını kurgulama | Aktif |
| CAMPVERSE ders slaytları + kitap | AMC MCQ ders desteleri ve kitap bölümleri | Aktif |
| Webinar landing page'leri | AUSCAMP ve UKCAMP webinar kayıt siteleri | Canlı |
| Meta Ads | Reklam yapıları + aylık rapor motoru | Aktif |
| CAMP LEAD → CRM | Webinar anket oylarını CRM'e lead olarak aktarır | Aktif |
| Danışan memnuniyet takibi | WhatsApp hal hatır mesajları → e-tablo | Aktif |
| Danışan rehberi | Tüm danışanların tek Excel rehberi | Aktif |
| Kataloglar ve sunumlar | Ülke katalogları, webinar sunumları, PDF'ler | Talep üzerine |
| Web sitesi içerik aktarımı | auscamp.com.tr yenileme (staging) | Devam ediyor |

---

## 2. Sosyal Medya İçerik Sistemi (AUSCAMP, UKCAMP, DENTCAMP)

Her marka için aynı mimaride 8 kişilik bir "ajan ekibi" kuruldu. Her markanın kendi bilgi bankası, marka sesi ve Asana projesi var.

### Akış

```
İçerik araştırması → Haftalık plan → Brief → (kullanıcı onayı) → Asana task
→ Tasarım → Caption (5 varyant) → (kullanıcı seçer) → Instagram yayını
```

### Ajanlar (her markada)

| Ajan | Görevi |
|---|---|
| `*-orkestra-sefi` | Çok adımlı işi baştan sona planlar, diğer ajanları sırayla çalıştırır |
| `*-icerik-arastirmaci` | Bir konu için 3-5 uyarlanabilir içerik fikri bulur |
| `*-haftalik-planlayici` | Haftalık Instagram takvimini kurar (gün, konu, şablon) |
| `*-brief-uretici` | Fikri sayfa sayfa tasarım brief'ine çevirir (T1-T10 şablonları) |
| `*-asana-task` | Onaylanan brief'i Asana'ya task olarak girer |
| `*-takvim-denetci` | Asana takviminde çakışma ve konu tekrarı arar |
| `*-caption-uretici` | Yayına hazır caption + CTA + hashtag (5 varyant) |
| `*-yayinci` | Onaylı postu yayına zamanlar |

DENTCAMP'e özel ek ajanlar: `dentcamp-reklam-denetci` (Meta reklam QA), `dentcamp-katalog-denetci`, `dentcamp-tasarim-denetci`.
AUSCAMP'e özel ek ajan: `auscamp-rehber-denetci` (danışan rehberi Excel QA).

### Sabit kurallar (3 marka)

- **Onaysız hiçbir şey yayınlanmaz.** Her post kullanıcının onayından geçer.
- Hoca/mentör tanıtımı, webinar, kampanya, lansman ve başarı postları **yalnızca kullanıcı istediğinde** üretilir.
- Asana task girişi sade: ad + brief + section + Priority. Atama ve teslim tarihi girilmez.
- Yayın otomasyonu Asana'ya hiçbir şey yazmaz (Asana yalnız okunur).
- Brief'ler kısa ve net: sayfa başına 3 madde. Tasarım metninde "-iyor" ve "meslektaş" kullanılmaz; uzun tire (—) kullanılmaz.
- Marka adları her yerde büyük harf: CAMP GROUP, AUSCAMP, UKCAMP, DENTCAMP.
- Caption'da 🔹 madde işareti, tek satır 📞 CTA, küçük harf hashtag.

### Marka özetleri

| Marka | Hesap | Kimlik | CTA iletişim |
|---|---|---|---|
| AUSCAMP | AUSCAMP IG | Avustralya'da doktorluk (Uzman / Pratisyen / YZ / Yaşam) | +90 552 253 03 37 |
| UKCAMP | @camp2uk | İngiltere / NHS, PLAB, GMC; Union Jack renkleri | ukcamp.com.tr, +90 552 253 0 337, info@ukcamp.com.tr |
| DENTCAMP | @dentcamptr | Yurt dışında diş hekimliği (Almanya, Avustralya, ABD, İngiltere, Danimarka); petrol yeşili/turkuaz | dentcamp.com.tr, +90 552 000 78 38 |

---

## 3. Instagram Yayın Otomasyonu

- **Birincil yol: Make (webhook yayıncı).** Fotoğraf, carousel ve reels rotaları var; 3 marka da aktif.
- **Yedek yol: Buffer** (script hazır ve test edildi). Make çalışmazsa buraya dönülür.
- Metricool API denendi; Advanced plan gerektiriyor.
- "Paylaş" akışı: Asana'dan postu çek → 5 caption üret → kullanıcı seçince yayınla.
- Sıralı çok görselli setler varsayılan olarak kaydırmalı carousel yayınlanır.
- Reels kapağını kullanıcı ekler; otomasyon kapak seçmez.
- Hazır görselde yazım hatası görülürse yayından önce bildirilir; küçük düzeltmeler görsel üzerinde doğrudan yapılır.

---

## 4. Video Sistemleri

### 4.1 CAMP REELS (webinar → reels)
Klasör: `~/camp-reels` · Skill: `camp-reels`

Zoom webinar kaydından premium Instagram reels üretir:
1. Transkript (kelime zamanlı)
2. `camp-reels-anlar`: en güçlü 4-6 anı seçer
3. `camp-reels-yonetmen`: her reels için sahne planı (soru kartı, vurgu kelimeleri, hareketli grafikler, zoom, ses efekti)
4. `camp-reels-gorsel`: açık kaynak / AI görselleri bulur ve gözle doğrular
5. Remotion ile render (kelime vurgulu altyazı, grafik, SFX)
6. `camp-reels-denetci`: her videoyu ölçüm + gözle denetler

Kurallar: hocanın konuşma videosu dış AI servislerine gönderilmez (yalnız yerel iyileştirme); otomatik yayın yok.

### 4.2 CAMPVERSE ders video kurgusu
Klasör: `~/camp-video` · Skill: `camp-video`

Loom ders kayıtlarını kurgular:
- `camp-video-hazirlik`: WhatsApp grubundan Loom linki + kesim talimatı çeker, indirir, sessizlik haritası ve transkript çıkarır
- `camp-video-kurgucu`: bozuk çekim, yeniden başlama, ölü zaman için kesim listesi üretir
- Render + opener ekleme
- `camp-video-denetci`: süre, çözünürlük, ses seviyesi, her kesim noktası denetimi

Odak kurgudur; hocanın tıbbi içeriği denetlenmez. 72 ders işlendi.

### 4.3 Diğer video araçları
- `video-use` skill'i: sohbetle video düzenleme (kesme, renk, altyazı, overlay)
- `manim-video` skill'i: teknik/animasyonlu anlatım videoları
- Emergency Focus video indirme otomasyonu (AMC MCQ, 135 video, kaldığı yerden devam eder)
- AUSCAMP tanıtım videosu senaryoları (`~/auscamp-tanitim-video`)

---

## 5. CAMPVERSE Eğitim İçeriği

| Proje | Klasör | Açıklama |
|---|---|---|
| Ders slaytları | `~/campverse-slides` | AMC MCQ chapter desteleri; AUSCAMP markalı PPTX motoru, EKG/figür gömülü |
| Kitap yeni bölümler | `~/campverse-slides/bookgen` | First Step AMC kitabına birebir dizgiyle yeni bölümler (Proxima Nova, A4) |
| Kitap şekilleri | skill `campverse-kitap-sekil` | Kitap diline uygun vektör şekil üretimi |
| AMC kitap denetimi | `~/amc-book-audit` | 5 cilt tam denetim, 1.104 satırlık bulgu kaydı |
| AMC radyoloji sunumu | `~/amc-radyoloji-sunum` | Radyoloji ders destesi |
| Müfredat sheet | Google Sheets | 5 marka video müfredatı (AMC MCQ 164 bölüm) |

Kurallar: açık kaynak görsel gözle açılmadan desteye konmaz (künyesi CREDITS.json'a yazılır); aynı bilgi en fazla 2 slaytta; kitaptaki hata slayta yazılmaz, ayrı dosyada tutulur.
Denetçiler: `campverse-slayt-denetci`, `campverse-gorsel-secici`.

---

## 6. Web Siteleri

| Site | Teknoloji | Not |
|---|---|---|
| AUSCAMP webinar sayfası | Vite + React, Vercel, Meta Pixel | auscamp-webinar.vercel.app; her ay o ayın takvimiyle güncellenir |
| UKCAMP webinar sayfası | Lovable | Güncelleme Lovable üzerinden yapılır |
| auscamp.com.tr yenileme | WordPress (staging) | Yalnız wp-admin içerik doldurma; kod işleri yazılımcıda. Blog + SSS yayında, sırada yasal sayfalar |
| DENTCAMP Danimarka içeriği | Lovable | Süreç sayfası, mentör, blog içerikleri hazır (Discovery kapsamında) |

---

## 7. Reklam ve Raporlama

- **Meta Ads yapıları:** AUSCAMP (webinar leadgen), UKCAMP (leadgen + webinar trafik), DENTCAMP (bilinirlik + leadgen + conversion). Kampanya ve görsel yükleme notları kayıtlı.
- **Aylık Meta Ads rapor motoru** (`~/meta-ads-rapor`): 3 marka, 16 sayfalık PDF, reklam görselleri gömülü.
- **DENTCAMP Instagram istatistik raporu** (`~/dentcamp-istatistik`): ilk 25 gün IG performansı.
- **Sosyal medya dışı reklam** (AUSCAMP): yeni alan, ayrı klasörde yürüyor.

---

## 8. Lead, CRM ve Danışan Sistemleri

| Sistem | Klasör | Ne yapar |
|---|---|---|
| CAMP LEAD → CRM | `~/camp-lead-crm` · skill `webinar-lead` | Webinar sonrası WhatsApp anket oylarını Quickesta CRM'e yeni lead olarak girer. Tek komut: `bin/lead webinar`. AUSCAMP leadleri iki satış temsilcisi arasında yarı yarıya atanır |
| AUSCAMP memnuniyet takibi | `~/auscamp-memnuniyet` | Ayda bir danışan WhatsApp gruplarına hal hatır mesajı; dönüşler e-tabloya özetlenir |
| AUSCAMP danışan rehberi | `~/auscamp-memnuniyet` | Ad / paket / telefon / e-posta / mentör tek Excel'de; portal (Moodle) eşleştirmesi |
| UKCAMP rehber | `~/ukcamp-rehber` | UKCAMP danışan rehberi |
| WhatsApp çekirdeği | `~/camp-wa-core` | Tüm WhatsApp otomasyonlarının ortak paketi (grup okuma, anket oyu, toplu grup ekleme) |

Not: WhatsApp toplu işlemler hesabı korumak için 3'erli partiler ve 2-3 dk arayla yapılır.

---

## 9. Kataloglar, Sunumlar ve Belgeler

| İş | Klasör |
|---|---|
| DENTCAMP ülke katalogları (4+1 ülke) | `~/dentcamp-katalog` |
| DENTCAMP vaka çalışması (işe alım PDF'i) | `~/dentcamp-vaka` |
| DENTCAMP webinar sunumları (Almanya, Amerika, Avustralya, İngiltere) | `~/dentcamp-webinar-*` (koyu sahne tasarım dili, düzenlenebilir PPTX) |
| DENTCAMP şemalar / mentör ödeme tablosu | `~/dentcamp-semalar`, `~/dentcamp-mentor-odeme` |
| AUSCAMP Specialist Pathway kataloğu | `~/auscamp-specialist-katalog` |
| İrem Çelik iş birliği reels rehberi | `~/camp-irem-isbirligi` |
| CloudPDF → aranabilir PDF dönüştürücü | `~/site-pdf` |

Hoca sunumu kuralı: içeriğe dokunulmaz, hocanın görselleri korunur, çıktı düzenlenebilir PPTX olur.

---

## 10. Skill'ler (tam liste)

### 10.1 Kendi yazdığımız skill'ler (bu repoda, `claude/skills/`)

| Skill | Ne zaman |
|---|---|
| `camp-humanize` | CAMP metni "yapay zeka gibi" duruyorsa doğallaştırır (3 marka) |
| `dentcamp-marka-sesi` | DENTCAMP'e giden her Türkçe metin |
| `camp-reels` | Webinardan reels üretimi |
| `camp-video` | CAMPVERSE ders videosu kurgusu |
| `campverse-kitap-sekil` | Kitap bölümü şekli |
| `webinar-lead` | Webinar anket leadlerini CRM'e aktarma (araç private repoda) |
| `auscamp-memnuniyet-takibi` | Çeyreklik memnuniyet kampanyası + tabloya not işleme (claude.ai'de organizasyon skill'i olarak paylaşılır) |

`kur.sh` bunları `~/.claude/skills/` altına kopyalar.

### 10.2 Üçüncü taraf skill'ler (kur.sh kurar)

| Paket | Kaynak | İçerik |
|---|---|---|
| **Superpowers** | `superpowers@claude-plugins-official` | brainstorming, systematic-debugging, writing-plans, TDD, code review, paralel ajan |
| **UI/UX Pro Max** | `nextlevelbuilder/ui-ux-pro-max-skill` | arayüz, banner, logo, sosyal medya görseli, tasarım sistemi, slayt |
| **planning-with-files** | `OthmanAdi/planning-with-files` | uzun işleri dosya tabanlı planla takip (`/plan`) |
| **gstack** | `garrytan/gstack` | `/browse`, `/qa`, `/review`, `/ship`, `/design-review`, `/make-pdf`, `/cso` ve ~35 skill daha |
| **video-use** + `manim-video` | `browser-use/video-use` | konuşarak video kurgu; matematik/teknik animasyon (camp-video ve camp-reels buna dayanır) |

### 10.3 Hesapla gelen skill'ler (kurulum gerekmez)

CAMP GROUP claude.ai hesabıyla giriş yapınca otomatik gelir: `pdf`, `docx`, `xlsx`, `pptx`, `docs`, `google-workspace`, `skill-creator`, `copywriting`, `import-memory`, `morning`.

## 11. Eklentiler

Eklentiler 10.2'deki tabloda. Elle kurmak isterseniz komutlar `KURULUM.md` 3. adımda.

## 12. Bağlı Servisler (MCP)

Asana, Make, Google Drive / Takvim, Notion, Higgsfield (AI görsel/video), Meta Ads, Canva, Figma, Lovable, Vercel, WordPress, Metricool, Quickesta CRM, Zoom, tl;dv, Slack, Gmail.

---

## 13. Ekip İçin: Nasıl İş İstenir?

Claude Code'a düz Türkçe yazmanız yeterli. Örnekler:

- "AUSCAMP için bu haftanın içerik takvimini kur"
- "Şu fikrin DENTCAMP brief'ini yaz"
- "Bu postu paylaş" (caption varyantları gelir, seçilen yayınlanır)
- "Cumartesi webinarından reels çıkar"
- "Bu webinarın leadlerini CRM'e gir"
- "Ekim Meta Ads raporunu çıkar"
- "Bu ders videosunu talimata göre kurgula"

Hatırlatma: hiçbir içerik kullanıcı onaylamadan yayınlanmaz veya Asana'ya girilmez.

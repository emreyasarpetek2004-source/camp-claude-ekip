# Make senaryosu — "IG Yayıncı" (Şekil A)

Bu senaryo **karar vermez, yayınlar.** Takvimi taramaz, caption üretmez. `make_publish.py`
tetiklediğinde (kullanıcı caption'ı seçtikten sonra) devreye girer.

**Neden takvim taramalı otomatik senaryo değil:** Asana task'ında caption YOK
(`feedback-ukcamp-task-assign`: "brief, caption koyma") ve akış gereği caption'ı kullanıcı
5 varyant arasından seçiyor (`feedback-auscamp-paylas-akisi`). Kendi kendine çalışan bir
senaryo caption'ı uydurmak zorunda kalırdı — kural ihlali.

**Make'in Buffer'a göre iki avantajı:**
1. **Süreli URL sorunu yok** → Asana'nın taze `download_url`'i yayın anında Instagram'a
   verilir. Görseli Vercel'e koy/deploy et/sil adımı **tamamen gereksiz**.
2. **Bulutta çalışır** → bilgisayarın açık olması gerekmez.

---

## ÖN KOŞUL — bunu doğrulamadan kurmaya başlama

Make'te yeni senaryo → "Instagram for Business" modülü ekle → **Create a connection**:

- **"Sign in with Facebook" diyorsa** → Make'in kendi Meta app'i. Kısıtlı developer
  hesabın devre dışı, **yolumuz açık**, kuruluma devam.
- **App ID / App Secret istiyorsa** → sen app açamıyorsun, **Make bu iş için kullanılamaz**.
  `buffer_publish.py` yedeğine dön.

Instagram hesabı **Business** olmalı ve yönettiğin bir Facebook Sayfası'na bağlı olmalı.
Kısıtlama yalnız geliştirici yüzeyinde; Business Suite/Instagram normal çalışıyor
(`reference-auscamp-ig-publish`), dolayısıyla bu bağlantı kurulabilir olmalı.

---

## Modüller

### 1. Webhooks → Custom webhook
Adı: `AUSCAMP IG Yayin`. Oluştur, **Copy address to clipboard** ile adresi al.
Adresi `.env` içine `MAKE_WEBHOOK_URL=` olarak yaz.

> Webhook adresi bir **sırdır** — bilen herkes yayın tetikleyebilir. Repoya girmez.

Beklenen gövde (`make_publish.py` bunu gönderiyor):

```json
{
  "brand": "auscamp",
  "ig_type": "carousel",
  "caption": "...",
  "media": ["https://...", "https://..."]
}
```

Webhook'u ilk kurarken `make_publish.py --live --yes` ile bir kez tetikle (medya
gerçek olsun ama senaryoda IG modülü henüz **bağlı değilken**) — Make gövde yapısını
böyle öğrenir (Determine data structure).

### 2. Router — `ig_type`'a göre 3 yol
| Yol | Filtre | Modül |
|---|---|---|
| Carousel | `ig_type` = `carousel` | Instagram → **Create a carousel post** |
| Tek görsel | `ig_type` = `photo` | Instagram → **Create a photo post** |
| Reel | `ig_type` = `reel` | Instagram → **Create a reel post** |

### 3. Instagram for Business modülü
- **Connection:** `brand` alanına göre doğru marka bağlantısı (@camp2aus / @camp2uk / @dentcamptr).
  Tek senaryoda 3 markayı yönetmek için `brand`'e göre ikinci bir router katmanı ekle,
  ya da her marka için senaryoyu kopyala (daha basit, önerilen).
- **Caption:** `{{1.caption}}`
- **Media (carousel):** `media` bir dizi olarak geliyor. Modülün medya alanındaki
  **Map** anahtarını aç ve `{{1.media}}` bağla. Map açılmazsa Make tek tek alan ister ve
  dizi bağlanamaz — bu en sık takılınan yer.
- **Media (photo/reel):** `{{1.media[1]}}` (Make dizileri **1'den** başlar, 0'dan değil).

### 4. Asana → **yazma YOK** (31 Ağu 2026'da kaldırıldı)
Yayın otomasyonu Asana'ya **hiçbir şey yazmaz** — ne başarı yorumu, ne hata yorumu,
ne başlık ön-eki. Kullanıcının kalıcı kararı; senaryoya `asana:CreateStory` modülü geri
eklenmez. Ayrıntı ve geri alma tarifi: `ASANA_YORUM_KAPATILDI.md`.

> Asana yalnızca **okunur**: görsel ekleri `download_url` ile çekilir. Yazma yönü kapalı.

### 5. Webhooks → Webhook response
- **Status:** 200
- **Body:** `{"post_id": "<IG modülünün Post ID alanı>"}`

`make_publish.py` `post_id`'yi de `permalink`'i de okuyor; hangisi gelirse onu basar.

### 6. Hata yolu (IG modülüne sağ tık → Add error handler)
- **Webhook response:** `{"error": "<error.message>"}` (status 200 kalsın; script
  `error` alanını görüp hata olarak bildiriyor)

Hata handler'ı olmadan başarısız yayın sessizce kaybolur — Buffer'da yaşadığımız
"sessiz düşme" sorununun Make'teki karşılığı budur.

---

## Bilinen kısıtlar

| Kısıt | Not |
|---|---|
| **JPEG zorunlu** | Instagram API'si PNG kabul etmez. Asana ekleri PNG ise ya tasarımcıdan JPEG export istenir (bedava, önerilen) ya da senaryoya Cloudinary gibi bir dönüştürme adımı girer. `make_publish.py --media` preflight'ı PNG'yi yakalar. |
| Carousel 2–10 görsel | Native uygulama 20'ye izin verir, API 10. |
| Görsel ≤ 8 MB | 4:5 – 1.91:1 en-boy. |
| Caption ≤ 2.200 karakter | 30 hashtag dahil. Script kontrol ediyor. |
| Operasyon maliyeti | Yayın başına ~4-6 operasyon. Aylık kotada ihmal edilebilir. |
| Yayın **anında** canlı olur | Zamanlama yok (Şekil A). İleri tarih isteniyorsa Şekil B'ye geçilir. |

---

## Test sırası (canlı posta çıkmadan)

1. `make_publish.py ... ` (dry-run) → payload'ı ve preflight'ı doğrula
2. Make'te senaryoyu **IG modülü devre dışı** kurup `--live --yes` ile tetikle →
   webhook'un gövdeyi doğru aldığını History'den gör
3. IG modülünü bağla, **kendi test hesabında** ya da kullanıcı onaylı gerçek bir postta çalıştır
4. Dönen `post_id`'nin geldiğini doğrula (Asana'ya hiçbir şey yazılmaz)

Gerçek yayın yalnız kullanıcı onayıyla (`feedback-auscamp-onaysiz-planlama-yok`).

---

## Şekil B'ye geçiş (sonra)

Bu senaryo çalıştıktan sonra "hafta başı planla, gün gün atsın" için eklenecekler:
onaylı caption + yayın saatinin saklandığı bir katman (Asana custom field ya da Make
Data Store) + zamanlı trigger. Onay atlanmaz, öne alınır. Şekil A kanıtlanmadan
başlanmaz.

## Reels rotası ve KAPAK (14 Ağu 2026)

Router'ın 3. rotası: filtre `ig_type = reel` → modül **`instagram-business:CreateAReelPost`**
("Create a reel post"). Alan eşlemeleri:

| Alan | Değer |
|---|---|
| `accountId` | DENTCAMP `<ID>` (@dentcamptr) |
| `video_url` | `{{2.media[1]}}` |
| `caption` | `{{2.caption}}` |
| `thumb_offset` | `{{2.thumb_offset}}` — **kapak karesi, milisaniye** |
| `share_to_feed` | `true` (hem Reels sekmesi hem ana akış) |

Hata kolu diğer rotalarla aynı: yalnız `WebhookRespond` (`{"error": "..."}`).

### Kapak kuralı — sonradan düzeltilemez
Instagram **yayınlanmış** bir reels'in kapağını değiştirmiyor; kapak yalnız paylaşım anında
`thumb_offset` ile belirleniyor. Yanlış kare seçildiyse tek çare gönderiyi silip yeniden atmak.
Dışarıdan kapak görseli yükleme yolu bu modülde yok — kapak videonun içinden bir kare olmak zorunda.

Bu yüzden akış **her zaman** şöyle:

```bash
# 1) Kapağı seç ve GÖZ İLE DOĞRULA (dry-run, hiçbir şey yayınlanmaz)
python3 make_publish.py --brand dentcamp --ig-type reel \
    --caption cap.txt --media "<public video url>" \
    --cover-ms 2500 --cover-preview ~/Downloads/video.mov
#    -> ~/Downloads/video.kapak-2500ms.jpg dosyasını aç ve bak

# 2) Kapak doğruysa yayınla
python3 make_publish.py --brand dentcamp --ig-type reel \
    --caption cap.txt --media "<public video url>" --cover-ms 2500 --live --yes
```

Konuşan kafa videolarında başlık/soru yazıları genelde 1–2,5 sn arasında ekrana giriyor;
`--cover-ms 0` (ilk kare) çoğu zaman **yazısız, kapaksız görünen** bir gönderi demek.

## DENTCAMP güncel durum (18 Ağustos 2026 — hat KURULU ve AKTİF)

| Nesne | Değer |
|---|---|
| Senaryo | `9655812` — "DENTCAMP IG Yayın" |
| Webhook (hook) | `4314220` — adres `.env` içindeki `MAKE_WEBHOOK_URL` (**SIRDIR**) |
| IG hesabı (`accountId`) | `<ID>` — **Dentcamp (@dentcamptr)** |
| IG bağlantısı | `__IMTCONN__ 14510204` (the user's Facebook connection) |
| Asana bağlantısı | `__IMTCONN__ 14511837` (yalnız hata kolunda kullanılıyor) |
| Rotalar | carousel · photo · **reel** (üçü de AUSCAMP ile birebir) |
| Durum | `isActive = true` — webhook 7/24 açık, Run once'a basmak gerekmiyor |

18.08.2026'da tamamlanan eksikler: iki rotadaki boş `accountId` dolduruldu, AUSCAMP'in reels
rotası klonlandı, senaryo aktive edildi. `accountId` **@dentcamptr**'nin IG Business ID'si;
Make'in `instagram-business` → `Pages` RPC'siyle tespit edildi (tahmin edilmedi).

### Yayın komutu (dry-run varsayılan)
```bash
cd "~/Documents/DENTCAMP Claude/DENTCAMP Marketing/Instagram Paylasim Otomasyonu"
export $(grep -v '^#' .env | xargs)
python3 make_publish.py --brand dentcamp --ig-type carousel \
    --task <ASANA_GID> --caption cap.txt --media "<url1>" "<url2>" ...
# yukarıdaki çıktı doğruysa sonuna --live --yes ekle
```
Medya kaynağı: Asana ekinin **taze** `download_url`'i (imzalı link süreli — çekip bekletme,
çek ve hemen tetikle). Vercel'e yükleme adımı Make yolunda gereksiz.

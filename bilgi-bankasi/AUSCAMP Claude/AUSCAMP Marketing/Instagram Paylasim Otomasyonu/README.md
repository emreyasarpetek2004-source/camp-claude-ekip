# AUSCAMP — Instagram Organik Paylaşım Otomasyonu

@camp2aus hesabına Graph API (Instagram Content Publishing) ile **organik** gönderi
yayınlar: tek görsel · carousel · reels. **Reklam değil** — normal feed paylaşımı.
(Reklamlar ayrı: `../Sosyal Medya Disi Reklamlar/Meta Reklam Otomasyonu/`.)

## 2 önemli gerçek (kısıt)
1. **Görsel/video PUBLIC bir https URL'den çekilir.** Yerel dosya yüklenemez.
   Kaynak seçenekleri: bir hosting/bucket, ya da **Asana attachment `download_url`**
   (public + süreli; hemen yayınlarken işe yarar).
2. **API'de ileri tarih ZAMANLAMA yok** — `media_publish` **anında** yayınlar.
   Belirli saatte istiyorsan bir **cron** hedef saatte bu script'i tetikler.
   (Planlı yayın için alternatif: Meta Business Suite — yayinci agent.)

## Kurulum
```bash
pip install requests
cp .env.example .env    # token'ı koy (reklam otomasyonundaki token'ın aynısı olabilir)
export $(grep -v '^#' .env | xargs)
```
Token izinleri: `instagram_content_publish`, `instagram_basic`, `pages_show_list`,
`pages_read_engagement`. Kısa ömürlüyse Access Token Debugger'da **Extend**.

## Kullanım
```bash
# DRY-RUN (varsayılan — yayınlamaz, planı yazar)
python publish_instagram.py --type carousel --images https://.../1.jpg https://.../2.jpg --caption-file cap.txt

# tek görsel
python publish_instagram.py --type single --image https://.../kapak.jpg --caption-file cap.txt

# reels
python publish_instagram.py --type reels --video https://.../reel.mp4 --caption-file cap.txt

# GERÇEK yayın (ANINDA canlı) — çift onay
python publish_instagram.py --type carousel --images ... --caption-file cap.txt --live --yes
```

## Akış (Content Publishing API)
- Tek görsel: `POST /{ig}/media` (image_url, caption) → **status FINISHED bekle** → `POST /{ig}/media_publish`
- Carousel: her görsel için child container (is_carousel_item) → **her child'ı FINISHED bekle** → `CAROUSEL` container (children) → **FINISHED bekle** → publish
- Reels: `REELS` container (video_url) → işlenene kadar bekle (status FINISHED) → publish

## ⚠️ 3 Ağustos 2026 düzeltmesi (Platform Terms 7.e.i.2 nedeniyle)
Meta developer hesabı **askıya alındı** ("negatively impacting platform"). Kök neden bu script'teki
iki kusurdu; ikisi de giderildi:

1. **Status beklenmiyordu.** Fotoğraf/carousel'de container oluşturulup HEMEN `media_publish`
   çağrılıyordu → `code=9007 sub=2207027 Media ID is not available` → tekrar denemeler → anormal
   başarısız çağrı yığını. Artık `wait_ready()` **fotoğraf ve carousel için de** çağrılıyor
   (üstel backoff, tavan 30sn, sert deneme sınırı).
2. **Hatalı URL'ler API'ye gidiyordu.** Yeni `preflight()`, her medya URL'sini **Graph'a hiç çağrı
   yapmadan** yerelde doğruluyor: HTTP durumu (200/206), `Content-Type` (image/* veya video/*),
   boyut (görsel ≤ 8 MB). Geçersizse `--live` yayını **başlamadan** iptal eder; dry-run'da uyarı basar.
   Bu, geçici dosya host'larının (tmpfiles vb.) HTML sayfasına yönlendirmesinden doğan
   `2207083 image format not supported` hatalarını da tamamen engelliyor.

Aynı düzeltme UKCAMP kopyasına da uygulandı. İtiraz dosyası:
`../Sosyal Medya Disi Reklamlar/Meta Reklam Otomasyonu/APPEAL-2026-08-03.md`

**Kural:** Geçici üçüncü taraf dosya host'u kullanmayın — medyayı kendi kontrolümüzdeki bir
alan adından (ya da taze Asana `download_url`) servis edin.

## Guardrail
- Varsayılan **dry-run**; `--live` için `--yes` şart.
- Yayınlanan gönderi **anında canlıdır** (silinebilir ama yayınlanmış olur) → `--live` yalnız onayla.
- Görseller https olmalı; caption dosyadan (`--caption-file`) okunabilir.
- Instagram: 24 saatte ~50 API gönderimi limiti.

## AUSCAMP akışına bağlanışı
- **caption:** `auscamp-caption-uretici` üretir → `cap.txt`'e koy.
- **görsel:** Asana task ekinden `download_url` (public) ya da bir bucket.
- **planlama:** anlık yayın = bu script; ileri tarih = cron ya da Business Suite (yayinci).

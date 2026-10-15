# UKCAMP Otomasyon — Kurulum Notu & Kalan Credential'lar

> UKCAMP içerik/carousel otomasyonu AUSCAMP sisteminden klonlandı (20.07.2026).
> Bu dosya, sistemin çalışması için **kullanıcının sağlaması gereken** credential'ları ve açık kalemleri listeler. Token'lar güvenlik gereği kopyalanmadı — sıfırdan girilecek.

## Hazır olanlar ✅
- Bilgi bankası: `01`–`07` dokümanları (UKCAMP'e özel, veri analizine dayalı).
- 8 agent: `~/.claude/agents/ukcamp-*.md` (orkestra-sefi, icerik-arastirmaci, haftalik-planlayici, brief-uretici, caption-uretici, asana-task, yayinci, takvim-denetci).
- Asana bağlantısı: UKCAMP projesi `<ID>`, Post section `<ID>`, Priority `<ID>`.
- IG publish script: `UKCAMP Marketing/Instagram Paylasim Otomasyonu/publish_instagram.py` (dry-run guardrail'li).
- Post verisi: `veri_arsivi/ukcamp_posts.json` (495 @camp2uk postu).

## Kullanıcının sağlaması gerekenler ⏳
1. **`~/Documents/UKCAMP Claude/.asana_token`** — UKCAMP Asana Personal Access Token
   (attachment upload + REST için). AUSCAMP'inkiyle AYNI olabilir (aynı workspace) —
   ama ayrı dosyaya konmalı. Asana → Settings → Apps → Personal Access Token.
2. **`UKCAMP Marketing/Instagram Paylasim Otomasyonu/.env`** — `.env.example`'dan kopyala:
   - `META_ACCESS_TOKEN` = UKCAMP'in @camp2uk'a erişimi olan Meta token'ı.
   - `META_IG_USER_ID` = @camp2uk Instagram Business hesabının ID'si.
3. **IG publish için public görsel host'u** — AUSCAMP `auscamp-webinar.vercel.app` kullanıyor.
   UKCAMP için karşılık: ayrı Vercel projesi / mevcut UKCAMP sayfası / geçici bucket.
   (Analiz + brief + caption üretimi bundan bağımsız çalışır; yalnız API ile organik yayın için gerekli.)

## Teyit edilecek 📌
- **Sabit haftalık ritim:** AUSCAMP'te Çarşamba=webinar, Pazar=story. UKCAMP'in sabit günleri var mı? (planlayici agent şu an esnek.)
- **@camp2uk IG_USER_ID** tespit edilince `.env` + gerekiyorsa reference memory güncellenir.

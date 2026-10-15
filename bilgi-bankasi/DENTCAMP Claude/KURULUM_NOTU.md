# DENTCAMP Otomasyon — Kurulum Notu & Kalan Kalemler

> DENTCAMP içerik/carousel otomasyonu UKCAMP sisteminden klonlandı (10.08.2026).
> UKCAMP de AUSCAMP'in klonuydu (20.07.2026) — kalıp üçüncü kez uygulanıyor.
> Bu dosya sistemin tam çalışması için **kullanıcının sağlaması gereken** kalemleri ve açık soruları listeler.

## Hazır olanlar ✅
- **Bilgi bankası:** `01`–`07` dokümanları + bu not.
  - `01_Caption_ve_Dil_Rehberi.md` · `02_Gorsel_Tasarim_Sistemi.md` · `03_Asana_Yapisi_ve_Otomasyon_Tasarimi.md` · `04_CAMP_Group_Marka_Manzarasi.md` · `05_DENTCAMP_Lansman_Icerik_Stratejisi.md` · `06_DENTCAMP_Dili_Master.md` · `07_Dis_Hekimligi_Konu_Listesi_ReShare.md`
- **8 agent:** `~/.claude/agents/dentcamp-*.md` (orkestra-sefi, icerik-arastirmaci, haftalik-planlayici, brief-uretici, caption-uretici, asana-task, yayinci, takvim-denetci)
- **Asana:** DENTCAMP projesi `<ID>` (MediaCamp takımı), 5 section açıldı.
- **`.asana_token`:** AUSCAMP'in PAT'inden kopyalandı (aynı workspace, aynı kullanıcı). Attachment upload için hazır.
- **IG publish script:** `DENTCAMP Marketing/Instagram Paylasim Otomasyonu/publish_instagram.py` (dry-run guardrail'li, preflight + wait_ready düzeltmeleri dâhil).

## Kullanıcının sağlaması gerekenler ⏳

1. **`@dentcamptr` Instagram Business hesabının `META_IG_USER_ID`'si**
   `.env` dosyasına yazılacak. Meta erişimi düzelince `check_token.sh` ile tespit edilebilir.

2. **`Instagram Paylasim Otomasyonu/.env`** — `.env.example`'dan kopyalanacak:
   - `META_ACCESS_TOKEN` = @dentcamptr'e erişimi olan Meta token'ı
   - `META_IG_USER_ID` = yukarıdaki ID

3. **IG publish için public görsel host'u**
   AUSCAMP `auscamp-webinar.vercel.app` kullanıyor. DENTCAMP karşılığı: `dentcamp.com.tr` üzerinde bir dizin, ayrı bir Vercel projesi, veya yayın anında çekilen taze Asana `download_url`.
   ⚠️ **Üçüncü parti geçici host (tmpfiles/catbox) KULLANILMAZ** — Meta kısıtlamasının sebebi buydu.

## Bilinen kısıtlar 🔒

### Meta / Instagram API şu an ÇALIŞMIYOR
Kullanıcının Meta developer hesabı 3 Ağustos 2026'dan beri kısıtlı. AUSCAMP ve UKCAMP token'ları da ölü (`code=190 "Application has been deleted"`). Erişim dönene kadar **IG yayını her üç markada da manuel**: görseli Asana'dan indir → boyutlandır → caption'ı `pbcopy` → kullanıcı elle paylaşır.
Detay ve çıkış yolları: `~/.claude/.../memory/reference-auscamp-ig-publish.md`.
**Bu araştırma/brief/caption/Asana akışını etkilemez** — sistem yayın olmadan tam çalışır.

### Asana Priority custom field'ı eklenemedi
MediaCamp workspace'i API üzerinden custom field eklemeye izin vermiyor (`custom_fields_premium_only`). AUSCAMP/UKCAMP'teki `Priority` alanı eski bir premium döneminden kalma.
**Sonuç:** DENTCAMP task'larında Priority set edilmiyor. Asana planı yükseltilirse:
```bash
TOKEN=$(tr -d ' \t\r\n' < ~/Documents/"DENTCAMP Claude"/.asana_token)
curl -s -X POST "https://app.asana.com/api/1.0/projects/<ID>/addCustomFieldSetting" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"data":{"custom_field":"<ID>","is_important":true}}'
```

## Teyit edilecek 📌

1. **Sabit haftalık ritim var mı?**
   AUSCAMP'te Çarşamba=webinar, Pazar=story sabit. DENTCAMP'te sabit gün henüz yok — `dentcamp-haftalik-planlayici` şu an esnek çalışıyor (`05` dokümanındaki öneri: haftada 4 post + 2 story günü). Lansman sonrası netleşince agent güncellenir.

2. **Mentör içerik izni.** Anlaşmalar sürüyor. İzin gelene kadar T6/T7 (mentör/ekip tanıtımı) üretilmiyor ve mentör sayısı/ismi hiçbir içerikte geçmiyor.

3. **Webinar takvimi.** Kurulunca T1/T2 devreye girer.

## Lansman sonrası yapılacaklar 🔄
- ~2 ay sonra `veri_arsivi/` altına @dentcamptr post verisi toplanır.
- `05_DENTCAMP_Lansman_Icerik_Stratejisi.md` → gerçek analizle `05_DENTCAMP_Instagram_Analiz.md` olarak yeniden yazılır.
- `01` ve `02` dokümanları gerçek feed'e göre revize edilir — ikisi de şu an **kurucu/varsayımsal** (geçmiş post verisi olmadan yazıldı).

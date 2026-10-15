# DENTCAMP — Instagram Organik Paylaşım Otomasyonu

@dentcamptr hesabına Graph API (Instagram Content Publishing) ile **organik** gönderi
yayınlar: tek görsel · carousel · reels. **Reklam değil** — normal feed paylaşımı.

## 2 önemli gerçek (kısıt)
1. **Görsel/video PUBLIC bir https URL'den çekilir.** Yerel dosya yüklenemez.
   Kaynak: bir hosting/bucket, ya da **Asana attachment `download_url`** (public + süreli).
2. **API'de ileri tarih ZAMANLAMA yok** — `media_publish` **anında** yayınlar.
   Belirli saat için **cron** ya da Meta Business Suite (yayinci agent).

## Kurulum
```bash
pip install requests
cp .env.example .env    # META_ACCESS_TOKEN + META_IG_USER_ID (@dentcamptr) doldur
export $(grep -v '^#' .env | xargs)
```
> ⚠️ `META_IG_USER_ID` hardcode DEĞİL — @dentcamptr business ID'sini .env'e sen girmelisin.
> Fallback YOKTUR: env boşsa script durur. Böylece yanlışlıkla @camp2aus / @camp2uk hesabına gönderim imkânsız.

## Kullanım
```bash
# DRY-RUN (varsayılan — yayınlamaz)
python publish_instagram.py --type carousel --images https://.../1.jpg https://.../2.jpg --caption-file cap.txt
# tek görsel
python publish_instagram.py --type single --image https://.../kapak.jpg --caption-file cap.txt
# reels
python publish_instagram.py --type reels --video https://.../reel.mp4 --caption-file cap.txt
# GERÇEK yayın (ANINDA canlı) — çift onay
python publish_instagram.py --type carousel --images ... --caption-file cap.txt --live --yes
```

## Guardrail
- Varsayılan **dry-run**; `--live` için `--yes` şart.
- Yayınlanan gönderi **anında canlıdır** → `--live` yalnız kullanıcı onayıyla.
- Görseller https olmalı; caption dosyadan (`--caption-file`).

## DENTCAMP akışına bağlanışı
- **caption:** `dentcamp-caption-uretici` üretir → `cap.txt`.
- **görsel:** Asana task ekinden `download_url` (public) ya da bucket.
- **planlama:** anlık = bu script; ileri tarih = cron ya da Business Suite (`dentcamp-yayinci`).

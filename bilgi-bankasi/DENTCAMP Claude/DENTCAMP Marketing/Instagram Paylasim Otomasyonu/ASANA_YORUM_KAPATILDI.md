# Asana yorumu KAPATILDI (31 Ağustos 2026)

Kullanıcının kararı: **yayın otomasyonu Asana'ya hiçbir şey yazmaz.** Üç markada da geçerli
(AUSCAMP / UKCAMP / DENTCAMP).

## Ne kaldırıldı

Make senaryolarındaki (`AUSCAMP IG Yayın` 9655711, `UKCAMP IG Yayın` 9655811,
`DENTCAMP IG Yayın` 9655812) her rotanın **hata kolundaki** `asana:CreateStory`
modülleri silindi. Başarı kolunda zaten Asana modülü yoktu — MAKE_SENARYO.md'deki
"PAYLAŞILDI yorumu" adımı 14 Ağu düzenlemesinde uygulanmamıştı, doküman eskiydi.

`make_publish.py`'den `--task` argümanı ve webhook payload'ındaki `asana_task_gid`
alanı kaldırıldı.

Yayın hatası artık yalnız webhook yanıtından okunuyor (`{"error": "..."}`) — script
hatayı ekrana basıyor, bilgi kaybı yok.

## Geri almak gerekirse

Her rotanın IG modülünün `onerror` dizisinin BAŞINA şu modül eklenir (id'ler:
carousel 31, photo 41, reel 51; `<IG_ID>` sırasıyla 10 / 3 / 50):

```json
{
  "id": 31,
  "mapper": {
    "text": "YAYIN HATASI — {{<IG_ID>.error.message}}",
    "task_gid": "{{2.asana_task_gid}}",
    "selectOrMap": "map"
  },
  "module": "asana:CreateStory",
  "version": 2,
  "metadata": { "designer": { "x": 600, "y": 0 } },
  "parameters": { "__IMTCONN__": 14511837 }
}
```

Reels rotasında designer konumu `{"x": 600, "y": 300}`. Asana bağlantısı:
`__IMTCONN__ 14511837`. Ayrıca `make_publish.py`'ye `--task` geri eklenip payload'a
`asana_task_gid` konur.

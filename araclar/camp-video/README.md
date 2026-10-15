# CAMP VIDEO

CAMPVERSE ders kayıtlarının kurgu hattı. Kurallar `~/.claude/skills/camp-video/SKILL.md`'de,
zanaat kuralları `~/Developer/video-use/SKILL.md`'de. Bu dosya yalnız klasörü tarif eder.

## Akış

```
wa_ders_cek.py → talimat_coz.py → yt-dlp → sessizlik.py → asr.py → normalize.py → render.py → takip.py
```

## Klasör

| Yol | İçerik |
|---|---|
| `bin/` | hattın araçları |
| `brand/campverse/opener.mp4` | 6,006 sn marka açılışı (kullanıcının örnek teslim videosundan) |
| `projects/<proje>/ders.mp4` | ham Loom indirmesi, klasörün kökünde TEK video |
| `projects/<proje>/edit/` | video-use düzeni: sessizlik, transkript, ders_1080, edl, final |
| `teslim/campverse/` | kapıları geçmiş final |
| `takip/` | takip tablosu (xlsx) + yapıştırmaya hazır TSV |

## Çalışma zamanları

| İş | Yorumlayıcı |
|---|---|
| WhatsApp çekimi | `~/camp-lead-crm/.venv/bin/python` (websocket-client burada) |
| Video, ASR, ayrıştırma | `~/Developer/video-use/.venv/bin/python` |
| Takip tablosu | `python3` (openpyxl burada) |

## Ajanlar

`camp-video-hazirlik` → `camp-video-kurgucu` → `camp-video-denetci` → kullanıcı onayı → teslim

## Sabitler

- Kanvas 1920x1080, siyah yan bant, 24 fps, AAC stereo 48 kHz
- Loom tavanı 1152x720 (16:10), 1080p yok
- Kesim sınırı `silencedetect`ten gelir, transkriptten değil
- Kapanış kartı yok, Loom arayüzü kırpılmaz
- Paylaşılan müfredat tablosuna yazılmaz

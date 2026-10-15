# CAMP REELS
Webinar kaydı → 1080x1920 webinar kesiti reels (DENTCAMP / UKCAMP / AUSCAMP). Kurallar ve akış: `~/.claude/skills/camp-reels/SKILL.md`. Format analizi: `analiz/RAPOR.md`.

- `bin/hat.py`        tek giriş (hazırlık / --uret)
- `bin/hazirla.py`    ses, sessizlik, kelime zamanlı transkript
- `bin/yerlesim.py`   Zoom düzeni (paylaşım / konuşmacı / slayt) + kontrol görseli
- `bin/anlar_brief.py` anlar agent'ı için brief
- `bin/uret.py`       render (sınır: kelime + sessizlik), altyazı (ASS), 2 geçişli loudnorm
- `bin/denetle.py`    R1-R7 kapıları + şerit görseller
- `bin/onizleme.py`   out/ONIZLEME.html
- `brands/*.json`     renk, altyazı stili, ASR sözlüğü, kalıcı düzeltmeler
- `analiz/`           @camp2uk analizi (veri, kareler, transkriptler)

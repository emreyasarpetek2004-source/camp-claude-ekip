#!/bin/bash
# Model kesim listesi hazir olan dersleri uretir.
# Birden fazla isci calisabilir: her ders icin atomik kilit (mkdir) alinir,
# kilidi alamayan isci o dersi atlar. Boylece iki kodlama ayni dosyaya girmez.
KOK=~/camp-video
VENV=~/Developer/video-use/.venv/bin/python
ISCI=${1:-1}
LOG=$KOK/takip/uret_kuyruk.log
mkdir -p "$KOK/takip"

temizle() { [ -n "$KILIT" ] && rmdir "$KILIT" 2>/dev/null; exit; }
trap temizle INT TERM EXIT

while true; do
  is=0
  for d in "$KOK"/projects/*/; do
    n=$(basename "$d")
    [ -s "$d/edit/model_kesim.json" ] || continue
    # Balon plani (05.10.2026, kullanıcı secimi B) kesim listesinden sonra degismis olabilir:
    # final ikisinden de yeni degilse yeniden basilir.
    if [ -s "$d/edit/final.mp4" ] && [ "$d/edit/final.mp4" -nt "$d/edit/model_kesim.json" ] \
       && { [ ! -f "$d/edit/balon_plan.json" ] || [ "$d/edit/final.mp4" -nt "$d/edit/balon_plan.json" ]; }; then
      continue
    fi
    # Denetimde kalmis ve kesim listesi o gunden beri degismemisse bekle: ayni
    # kusurlu kurguyu tekrar tekrar basmanin anlami yok, duzeltme bekleniyor.
    if [ -f "$d/edit/.denetim_kaldi" ] && [ "$d/edit/.denetim_kaldi" -nt "$d/edit/model_kesim.json" ] \
       && { [ ! -f "$d/edit/balon_plan.json" ] || [ "$d/edit/.denetim_kaldi" -nt "$d/edit/balon_plan.json" ]; }; then
      continue
    fi
    KILIT="$d/edit/.uretiliyor"
    mkdir "$KILIT" 2>/dev/null || { KILIT=""; continue; }

    vid=$(python3 -c "
import json
k=json.load(open('$KOK/takip/ders_kayitlari.json'))
r=k if isinstance(k,list) else k.get('kayit',k)
h='$n'.split('-')[-1]
print(next((x['loom_vid'] for x in r if isinstance(x,dict) and x.get('loom_vid','').startswith(h)),''))" 2>/dev/null)
    if [ -z "$vid" ]; then
      echo "$(date +%H:%M) [i$ISCI] vid bulunamadi: $n" >> "$LOG"; rmdir "$KILIT"; KILIT=""; continue
    fi

    echo "$(date +%H:%M) [i$ISCI] === $n" >> "$LOG"
    if ! $VENV "$KOK/bin/hat.py" "$vid" --model --kuru >> "$LOG" 2>&1; then
      echo "$(date +%H:%M) [i$ISCI] EDL KURULAMADI: $n" >> "$LOG"; rmdir "$KILIT"; KILIT=""; continue
    fi
    if ! $VENV "$KOK/bin/hat.py" "$vid" --uret >> "$LOG" 2>&1; then
      echo "$(date +%H:%M) [i$ISCI] URETIM/DENETIM KALDI: $n" >> "$LOG"; rmdir "$KILIT"; KILIT=""; continue
    fi
    echo "$(date +%H:%M) [i$ISCI] TAMAM: $n" >> "$LOG"
    rmdir "$KILIT"; KILIT=""
    is=1
  done
  [ "$is" = "0" ] && sleep 90
done

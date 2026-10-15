#!/bin/bash
# Transkripti/sessizlik haritasi olmayan dersleri sirayla hazirlar ve brief'ini basar.
# ASR GPU'yu tek basina kullanir, bu yuzden seri calisir.
KOK=~/camp-video
VENV=~/Developer/video-use/.venv/bin/python
LOG=$KOK/takip/hazirla_kuyruk.log
mkdir -p "$KOK/takip"

for d in "$KOK"/projects/*/; do
  n=$(basename "$d")
  vid="$d/ders.mp4"
  [ -f "$vid" ] || { echo "$(date +%H:%M) ATLA $n (ham yok)" >> "$LOG"; continue; }
  mkdir -p "$d/edit"

  if [ ! -s "$d/edit/sessizlik.json" ]; then
    echo "$(date +%H:%M) sessizlik: $n" >> "$LOG"
    $VENV "$KOK/bin/sessizlik.py" "$vid" --out "$d/edit/sessizlik.json" >> "$LOG" 2>&1 \
      || echo "$(date +%H:%M) HATA sessizlik $n" >> "$LOG"
  fi

  if [ ! -s "$d/edit/transkript_tam.json" ]; then
    echo "$(date +%H:%M) ASR: $n" >> "$LOG"
    $VENV "$KOK/bin/asr.py" "$vid" --tam --out "$d/edit/transkript_tam.json" >> "$LOG" 2>&1 \
      || { echo "$(date +%H:%M) HATA asr $n" >> "$LOG"; rm -f "$d/edit/transkript_tam.json"; }
  fi

  if [ -s "$d/edit/brief.md" ]; then
    echo "$(date +%H:%M) brief zaten var: $n" >> "$LOG"
  elif [ -s "$d/edit/transkript_tam.json" ] && [ -s "$d/edit/sessizlik.json" ]; then
    $VENV "$KOK/bin/kurgu_brief.py" "projects/$n" >> "$LOG" 2>&1 \
      && echo "$(date +%H:%M) BRIEF HAZIR $n" >> "$LOG" \
      || echo "$(date +%H:%M) HATA brief $n" >> "$LOG"
  fi
done
echo "$(date +%H:%M) KUYRUK BITTI" >> "$LOG"

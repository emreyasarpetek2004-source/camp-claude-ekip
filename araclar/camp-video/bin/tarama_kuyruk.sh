#!/bin/bash
# Teslim edilen tum dersleri sirayla tarar (ASR GPU'yu tek basina kullanir).
KOK=~/camp-video
VENV=~/Developer/video-use/.venv/bin/python
LOG=$KOK/takip/tarama_kuyruk.log
mkdir -p "$KOK/takip/teslim_tarama"
cd "$KOK" || exit 1
for f in ~/Downloads/"CAMPVERSE Dersler"/Editli/*.mp4; do
  ad=$(basename "$f")
  case "$ad" in "00 - "*) continue;; esac
  hedef="$KOK/takip/teslim_tarama/${ad%.mp4}.json"
  if [ -s "$hedef" ] && python3 -c "
import json,sys
d=json.load(open('$hedef'))
sys.exit(0 if isinstance(d.get('segment'),list) else 1)" 2>/dev/null; then
    continue
  fi
  rm -f "$hedef"
  echo "$(date +%H:%M) TARANIYOR $ad" >> "$LOG"
  $VENV "$KOK/bin/teslim_tara.py" "$ad" >> "$LOG" 2>&1 || echo "$(date +%H:%M) HATA $ad" >> "$LOG"
done
echo "$(date +%H:%M) TARAMA KUYRUGU BITTI" >> "$LOG"

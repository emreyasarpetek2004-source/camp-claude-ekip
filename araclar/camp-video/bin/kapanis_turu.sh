#!/bin/bash
# Uretim bitince: degisen derslerin teslim hallerini YENIDEN tara, sonra denetle.
# Kurgu degistigi icin eski tarama gecersiz. (23.09.2026)
KOK=~/camp-video
VENV=~/Developer/video-use/.venv/bin/python
LOG=$KOK/takip/kapanis_turu.log
cd "$KOK" || exit 1

# 1) uretim kuyrugu bosalana kadar bekle
while true; do
  bekleyen=$(for d in projects/*/; do
    [ -s "$d/edit/model_kesim.json" ] || continue
    if [ ! -s "$d/edit/final.mp4" ] || [ "$d/edit/model_kesim.json" -nt "$d/edit/final.mp4" ]; then echo x; fi
  done | wc -l | tr -d ' ')
  calisan=$(pgrep -f "bin/hat.py" | wc -l | tr -d ' ')
  [ "$bekleyen" = "0" ] && [ "$calisan" = "0" ] && break
  sleep 60
done
echo "$(date +%H:%M) uretim bitti, yeniden tarama basliyor" >> "$LOG"

# 2) teslim dosyasi taramadan yeniyse yeniden tara
for f in ~/Downloads/"CAMPVERSE Dersler"/Editli/*.mp4; do
  ad=$(basename "$f"); case "$ad" in "00 - "*) continue;; esac
  t="$KOK/takip/teslim_tarama/${ad%.mp4}.json"
  # mtime'a GUVENME: teslim_coz.py dosyayi yeniden yazinca tazeleniyor.
  # bayat_tarama.py teslim videosunun SURESINI tarama kaydiyla karsilastirir.
  if [ -s "$t" ] && ! $VENV "$KOK/bin/bayat_tarama.py" | grep -qxF "$t"; then continue; fi
  echo "$(date +%H:%M) yeniden tara: $ad" >> "$LOG"
  rm -f "$t"
  $VENV "$KOK/bin/teslim_tara.py" "$ad" >> "$LOG" 2>&1
done

# 3) denetim
echo "$(date +%H:%M) === DENETIM ===" >> "$LOG"
$VENV "$KOK/bin/acilis_kesim_denetle.py" >> "$LOG" 2>&1
$VENV "$KOK/bin/teslim_coz.py" >> "$LOG" 2>&1
$VENV "$KOK/bin/kapanis_dogrula.py" >> "$LOG" 2>&1
$VENV "$KOK/bin/talimat_kapsama.py" >> "$LOG" 2>&1
echo "$(date +%H:%M) KAPANIS TURU BITTI" >> "$LOG"

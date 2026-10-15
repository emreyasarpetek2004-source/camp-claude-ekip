#!/bin/bash
# Uretim bitene kadar bekler, degisen dersleri yeniden tarar, sonra tum denetimi calistirir.
KOK=~/camp-video
VENV=~/Developer/video-use/.venv/bin/python
LOG=$KOK/takip/kapanis_turu.log
cd "$KOK" || exit 1

while pgrep -f "bin/hat.py" >/dev/null || pgrep -f "uret_kuyruk.sh" >/dev/null; do sleep 45; done
echo "$(date +%H:%M) uretim bitti, bayat taramalar yenileniyor" >> "$LOG"

# ders adlarinda BOSLUK var: $(...) kelime bolmesi yapar, satir satir okunmali.
$VENV bin/bayat_tarama.py > /tmp/bayat_liste.txt
while IFS= read -r t; do
  [ -n "$t" ] || continue
  ad=$(basename "$t" .json)
  echo "$(date +%H:%M) yeniden tara: $ad" >> "$LOG"
  rm -f "$t"
  # < /dev/null sart: teslim_tara.py stdin'i tuketirse dongunun kalan satirlari yutulur
  # (23 Eyl 2026: CH29 bu yuzden hic taranmadi)
  $VENV bin/teslim_tara.py "$ad.mp4" < /dev/null >> "$LOG" 2>&1
done < /tmp/bayat_liste.txt

echo "$(date +%H:%M) === DENETIM ===" >> "$LOG"
for k in acilis_kesim_denetle teslim_coz kapanis_dogrula talimat_kapsama; do
  echo "--- $k ---" >> "$LOG"
  $VENV "bin/$k.py" >> "$LOG" 2>&1 || echo "  $k HATA" >> "$LOG"
done
echo "$(date +%H:%M) KAPANIS TURU BITTI" >> "$LOG"

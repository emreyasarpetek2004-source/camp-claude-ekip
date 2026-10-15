#!/bin/bash
# GECE BEKCISI (06.10.2026, kullanıcı: "sabaha her sey bitmis olsun, takilmasin durmasin").
# 5 dk'da bir:
#  1. uret_kuyruk.sh iscileri (1 ve 2) yasiyor mu; olmusse yeniden baslatir.
#  2. Takilma: bir dersin parca/ klasorunde 40 dk boyunca hic dosya buyumediyse o dersin
#     surecleri oldurulur, kilit kaldirilir (parcalar anahtarli: yarim parca yeniden kullanilmaz).
#  3. Denetimde kalmis ama videosu guncel dersler yeniden kodlamadan tekrar denetlenir
#     (bin/yeniden_denetle.sh). Kurgu kaynakli kalanlar (G7/G11/G14) takip/sabah_listesi.txt'ye.
#  4. Disk < 12 GB ise iscileri durdurur (yarim cikti uretmesin), loga yazar.
# Log: takip/gece_bekcisi.log
KOK=~/camp-video; LOG=$KOK/takip/gece_bekcisi.log
cd "$KOK" || exit 1
while true; do
  T=$(date +%H:%M)
  bos=$(df -g ~ | tail -1 | awk '{print $4}')
  if [ "$bos" -lt 12 ]; then
    echo "$T DISK $bos GB: iscileri durduruyorum" >> "$LOG"
    for p in $(pgrep -f "bin/uret_kuyruk.sh"); do pkill -P $p; kill $p; done
    sleep 300; continue
  fi
  for i in 1 2; do
    if ! pgrep -f "bin/uret_kuyruk.sh $i\$" > /dev/null; then
      echo "$T isci $i yok -> baslatildi" >> "$LOG"
      nohup caffeinate -i bash bin/uret_kuyruk.sh $i > /dev/null 2>&1 &
      sleep 5
    fi
  done
  # takilma denetimi
  for k in projects/*/edit/.uretiliyor; do
    [ -d "$k" ] || continue
    e=$(dirname "$k"); pr=$(dirname "$e")
    yas=$(( $(date +%s) - $(stat -f %m "$k") ))
    [ "$yas" -lt 2400 ] && continue
    son=$(find "$e/parca" "$e/final.mp4" -newermt "-40 minutes" 2>/dev/null | head -1)
    if [ -z "$son" ]; then
      echo "$T TAKILMA: $(basename $pr) 40 dk ilerlemedi -> surecler olduruldu" >> "$LOG"
      for p in $(pgrep -f "$(basename $pr)"); do pkill -P $p 2>/dev/null; kill $p 2>/dev/null; done
      rmdir "$k" 2>/dev/null
    fi
  done
  # denetci kaynakli kalanlari yeniden sina
  out=$(bash bin/yeniden_denetle.sh 2>&1)
  [ -n "$out" ] && echo "$T yeniden denetim:" >> "$LOG" && echo "$out" >> "$LOG"
  # kurgu kaynakli kalanlar -> sabah listesi
  : > takip/sabah_listesi.txt
  for f in projects/*/edit/.denetim_kaldi; do
    [ -f "$f" ] || continue
    e=$(dirname "$f"); [ "$f" -nt "$e/model_kesim.json" ] || continue
    echo "$(basename $(dirname $e)): $(grep 'KALDI ' "$f" | sed 's/^ *//' | cut -c1-200 | tr '\n' ' ')" >> takip/sabah_listesi.txt
  done
  n=$(ls teslim/campverse/*.mp4 2>/dev/null | wc -l | tr -d ' ')
  yeni=$(find teslim/campverse -name "*.mp4" -newer takip/.v2_basladi 2>/dev/null | wc -l | tr -d ' ')
  echo "$T durum: v2 teslim $yeni/72 · disk $bos GB · kalan liste $(wc -l < takip/sabah_listesi.txt)" >> "$LOG"
  sleep 300
done

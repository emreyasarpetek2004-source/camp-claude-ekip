#!/bin/bash
# Takilmis surecleri kendi kendine temizler.
# Bugun ucu de ayni kokten geldi: oksuz kalan ffmpeg/ASR surecleri bellegi kilitledi.
while true; do
  # 15 dk'dan uzun sure calisip CPU'su %5'in altinda olan mlx/ffmpeg = takilmis
  ps -eo pid,etime,pcpu,comm | grep -E "mlx-whisper|ffmpeg" | grep -v grep | while read pid et cpu comm; do
    dk=$(echo "$et" | awk -F: '{if(NF==3) print $1*60+$2; else print $1}')
    if [ "${dk:-0}" -ge 15 ] 2>/dev/null; then
      if [ "$(echo "$cpu < 5" | bc 2>/dev/null)" = "1" ]; then
        echo "$(date +%H:%M) BEKCI: takilmis surec kesildi pid=$pid sure=$et cpu=$cpu $comm" >> /tmp/bekci.log
        kill -9 "$pid" 2>/dev/null
      fi
    fi
  done
  sleep 120
done

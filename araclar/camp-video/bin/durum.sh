#!/bin/bash
cd ~/camp-video
say() { pgrep -f "$1" 2>/dev/null | wc -l | tr -d ' '; }
say1() { pgrep -f "$1" 2>/dev/null | head -1 | wc -l | tr -d ' '; }
E=$(ls ~/Downloads/"CAMPVERSE Dersler"/Editli/*.mp4 2>/dev/null | wc -l | tr -d ' ')
H=$(ls ~/Downloads/"CAMPVERSE Dersler"/Ham/*.mp4 2>/dev/null | wc -l | tr -d ' ')
T=$(ls projects/*/edit/transkript_tam.json 2>/dev/null | wc -l | tr -d ' ')
S=$(ls projects/*/edit/sessizlik.json 2>/dev/null | wc -l | tr -d ' ')
B=$(ls projects/*/edit/brief.md 2>/dev/null | wc -l | tr -d ' ')
K=$(ls projects/*/edit/model_kesim.json 2>/dev/null | wc -l | tr -d ' ')
F=$(ls projects/*/edit/final.mp4 2>/dev/null | wc -l | tr -d ' ')
P=$(ls -d projects/*/ 2>/dev/null | wc -l | tr -d ' ')

echo "$(date +%H:%M) · $P ders · sessizlik $S · transkript $T · brief $B · KESIM LISTESI $K · final $F"
echo "  teslim: $E editli, $H ham · disk $(df -h ~|tail -1|awk '{print $4}') bos"

# su an ne isleniyor
now=$(pgrep -fl "asr.py|sessizlik.py|olustur.py|yt-dlp" 2>/dev/null \
  | grep -o 'campverse-[a-z0-9-]*' | sed 's/campverse-//;s/-[0-9a-f]\{8\}$//' | sort -u | paste -sd', ' -)
[ -n "$now" ] && echo "  isleniyor: $now"
echo "  surecler: asr $(say mlx_whisper) · ffmpeg $(say '^/Users.*ffmpeg') · indirme $(say 'uv/tools/yt-dlp')"
tail -3 takip/hazirla_kuyruk.log 2>/dev/null | grep -E "ASR:|BRIEF|HATA|BITTI" | sed 's/^/  /'

#!/bin/bash
# Denetimde KALMIS ama final.mp4'u guncel (edl'den yeni) dersleri YENIDEN KODLAMADAN
# guncel denetciyle tekrar sinar; gecen teslim edilir. Denetci duzeltildikten sonra
# dogru basilmis dersi bosuna yeniden kodlamamak icin. (06.10.2026)
KOK=~/camp-video; VENV=~/Developer/video-use/.venv/bin/python
# Once: eski planla basilmis final varsa sil (kuyruk yeniden basar). Bos cikti = degisiklik yok.
u=$($VENV "$KOK/bin/plan_uzlas.py" 2>&1); case "$u" in *"basilacak 0 "*) ;; *) echo "$u";; esac
for d in "$KOK"/projects/*/; do
  e="$d/edit"
  [ -f "$e/.denetim_kaldi" ] && [ -s "$e/final.mp4" ] && [ "$e/final.mp4" -nt "$e/edl.json" ] || continue
  # Denetci kodu ya da balon plani son denetimden beri degismediyse ayni sonuc cikar: atla
  yeni=0
  for f in "$KOK"/bin/denetle.py "$KOK"/bin/balon_senkron.py "$KOK"/bin/hayalet_kontrol.py "$e/balon_plan.json"; do
    [ "$f" -nt "$e/.denetim_kaldi" ] && yeni=1
  done
  [ "$yeni" = 1 ] || continue
  mkdir "$e/.uretiliyor" 2>/dev/null || continue
  n=$(basename "$d"); h=${n##*-}
  vid=$(python3 -c "
import json;k=json.load(open('$KOK/takip/ders_kayitlari.json'));r=k if isinstance(k,list) else k.get('kayit',k)
print(next((x['loom_vid'] for x in r if isinstance(x,dict) and x.get('loom_vid','').startswith('$h')),''))")
  if [ -n "$vid" ]; then
    echo "== $n"
    $VENV "$KOK/bin/hat.py" "$vid" --uret --yalniz-denetim < /dev/null 2>&1 | grep -E "KALDI |TESLIM|DENETIM:"
  fi
  rmdir "$e/.uretiliyor"
done

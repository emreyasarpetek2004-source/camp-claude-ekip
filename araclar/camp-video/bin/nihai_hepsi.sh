#!/bin/bash
# kesim_nihai.json'u olan ama henuz islenmemis dersleri uygular (05.10.2026).
cd ~/camp-video
for p in projects/*/; do
  p=${p%/}; n=$p/edit/kesim_nihai.json; m=$p/edit/model_kesim.json
  [ -f $n ] || continue
  [ -d $p/edit/.uretiliyor ] && { echo "atla (uretimde): $p"; continue; }
  grep -q '"yeniden_tarama"' $m 2>/dev/null && [ $m -nt $n ] && continue
  python3 bin/nihai_uygula.py $p < /dev/null
  echo "  kod=$?"
done

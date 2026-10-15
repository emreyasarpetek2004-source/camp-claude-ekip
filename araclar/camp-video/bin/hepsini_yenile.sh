#!/bin/bash
# Yeni lojistik dedektoruyle TUM dersleri bastan isle (kullanıcı: "hepsine tekrar yap")
cd ~/camp-video
HAM=~/Downloads/"CAMPVERSE Dersler"/Ham
python3 - <<'PY' > /tmp/yenile_sirasi.txt
import json,os,sys
sys.path.insert(0,'bin'); import hat
KOK=os.path.expanduser('~/camp-video')
for x in json.load(open('takip/dersler.json')):
    P=os.path.join(KOK,'projects','campverse-%s-%s'%(hat.slug('CH%02d %s'%(x['no'],x['chapter'])),x['vid'][:8]))
    ham=os.path.join(P,'ders.mp4')
    yedek=os.path.expanduser('~/Downloads/CAMPVERSE Dersler/Ham/%02d - %s (ham).mp4'%(x['no'],x['chapter'].strip()))
    if os.path.exists(ham) or os.path.exists(yedek):
        print('%s|%s|%s' % (x['vid'], ham, yedek))
PY
while IFS='|' read -r vid ham yedek; do
  [ -f "$ham" ] || ln "$yedek" "$ham" 2>/dev/null
  [ -f "$ham" ] || continue
  P=$(dirname "$ham")
  rm -rf "$P/edit/parca" "$P/edit/final.mp4" "$P/edit/kesimler.json" "$P/edit/edl_imza.txt"
  echo "=== $vid ==="
  python3 -u bin/hat.py "$vid" --hazirla < /dev/null 2>&1 | grep -E "kesim:|hizalandi|HATA" | sed 's/^/  /'
  python3 -u bin/hat.py "$vid" --uret < /dev/null 2>&1 | grep -E "TESLIM:|DENETIM|HATA" | sed 's/^/  /'
done < /tmp/yenile_sirasi.txt
echo "=== HEPSI BITTI ==="

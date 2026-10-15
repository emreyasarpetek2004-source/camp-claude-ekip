#!/bin/bash
# Verilen derslerde: sinir kontrol -> enerji cukuruna tasi -> yeniden uygula -> tekrar kontrol
cd ~/camp-video
python3 bin/sinir_kontrol.py "$@" > takip/sinir_kontrol.log
[ -s takip/sinir_kontrol.log ] || { echo "sinirlar temiz"; exit 0; }
cat takip/sinir_kontrol.log
python3 bin/sinir_duzelt.py | tail -3
bash bin/nihai_hepsi.sh 2>&1 | grep -vE "^atla"
python3 bin/sinir_kontrol.py "$@"

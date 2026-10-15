#!/bin/bash
# Uretimdeyken atlanan dersleri, basim bitince yeniden uygular (05.10.2026).
cd ~/camp-video
for i in $(seq 1 200); do
  out=$(bash bin/nihai_hepsi.sh 2>&1)
  echo "$out" | grep -v "^atla" | grep . && echo "$(date +%H:%M) ^ uygulandi"
  sleep 180
done >> takip/nihai_bekci.log 2>&1

#!/bin/bash
set -e
cd ~/auscamp-webinar
export VERCEL_TOKEN="$(cat ~/.auscamp_vercel_token)"
bash scripts/deploy.sh
for s in cv-is-basvurulari-4-eki uzmanlik-denkligi-basvuru-belgeleri-11-eki radyoloji-konu-anlatimi-18-eki mcq-soru-cozumu-25-eki; do
  echo "$s: $(curl -s -o /dev/null -w "%{http_code}" https://webinar.auscamp.com.tr/webinar/$s)"
done
curl -s https://webinar.auscamp.com.tr | grep -o "<title>[^<]*</title>"

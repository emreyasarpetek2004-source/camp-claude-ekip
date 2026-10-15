#!/bin/bash
set -e
cd ~/auscamp-webinar
export VERCEL_TOKEN="$(cat ~/.auscamp_vercel_token)"
bash scripts/deploy.sh >/dev/null
JS=$(curl -s https://webinar.auscamp.com.tr | grep -o 'assets/index-[A-Za-z0-9_-]*\.js')
curl -s "https://webinar.auscamp.com.tr/$JS" | grep -q "Süreç hakkında bilgi al" && echo "CANLI: bilgi kutusu yayında" || echo "HATA: canlıda yeni sürüm yok"

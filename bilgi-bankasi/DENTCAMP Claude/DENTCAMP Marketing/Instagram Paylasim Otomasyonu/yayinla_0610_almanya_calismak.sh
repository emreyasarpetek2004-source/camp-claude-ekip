#!/usr/bin/env bash
# 02.10 Almanya'da Diş Hekimi Olarak Çalışmak (seri 2/4) — DENTCAMP carousel 5 görsel, caption varyant 2
# Deneme:  bash yayinla_0610_almanya_calismak.sh
# Canlı:   bash yayinla_0610_almanya_calismak.sh --live --yes
set -euo pipefail
cd "$(dirname "$0")"
TOKEN=$(tr -d ' \t\r\n' < ~/Documents/"DENTCAMP Claude"/.asana_token)
URLS=()
for A in <ID> <ID> <ID> <ID> <ID>; do
  U=$(curl -s -H "Authorization: Bearer $TOKEN" "https://app.asana.com/api/1.0/attachments/$A?opt_fields=download_url" \
    | python3 -c "import json,sys;print(json.load(sys.stdin)['data']['download_url'])")
  curl -sI "$U" | grep -iE "^HTTP|content-type" | tr '\n' ' '; echo
  URLS+=("$U")
done
python3 make_publish.py --brand dentcamp --ig-type carousel --caption cap_0610_almanya_calismak_SECILEN.txt "$@" --media "${URLS[@]}"

#!/usr/bin/env bash
# 30.09 Almanya'da Sürecin İkinci Adımı: Fachsprachenprüfung (seri 3/4) — DENTCAMP carousel 5 görsel, caption varyant 1
# Deneme:  bash yayinla_3009_almanya_fsp.sh
# Canlı:   bash yayinla_3009_almanya_fsp.sh --live --yes
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
python3 make_publish.py --brand dentcamp --ig-type carousel --caption cap_3009_almanya_fsp_SECILEN.txt "$@" --media "${URLS[@]}"

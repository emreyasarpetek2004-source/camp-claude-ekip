#!/usr/bin/env bash
# 01.10 ABD'de Diş Hekimi Olarak Çalışmak (seri 3/4) — DENTCAMP carousel 5 görsel, caption varyant 2
# Deneme:  bash yayinla_0110_abd_calismak.sh
# Canlı:   bash yayinla_0110_abd_calismak.sh --live --yes
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
python3 make_publish.py --brand dentcamp --ig-type carousel --caption cap_0110_abd_calismak_SECILEN.txt "$@" --media "${URLS[@]}"

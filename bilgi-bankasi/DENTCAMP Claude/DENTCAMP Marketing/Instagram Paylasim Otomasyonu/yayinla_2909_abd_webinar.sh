#!/usr/bin/env bash
# 29.09 Amerika'da Diş Hekimliği Çalışma Şartları webinarı — DENTCAMP tek görsel (Ekim takvimi 02, 4:5), caption varyant 1
set -euo pipefail
cd "$(dirname "$0")"
TOKEN=$(tr -d ' \t\r\n' < ~/Documents/"DENTCAMP Claude"/.asana_token)
URL=$(curl -s -H "Authorization: Bearer $TOKEN" "https://app.asana.com/api/1.0/attachments/<ID>?opt_fields=download_url" \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['data']['download_url'])")
echo "Görsel: ekim webinar takvimi-02.jpg"
curl -sI "$URL" | grep -iE "^HTTP|content-type"
python3 make_publish.py --brand dentcamp --ig-type photo --caption cap_2909_abd_webinar_SECILEN.txt --live --yes --media "$URL"

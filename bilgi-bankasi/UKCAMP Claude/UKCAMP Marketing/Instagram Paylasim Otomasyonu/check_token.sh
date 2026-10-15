#!/bin/bash
# UKCAMP — Meta/Instagram token sağlık kontrolü
# Kullanım:  bash check_token.sh            → .env'deki META_ACCESS_TOKEN'ı test eder
#            bash check_token.sh "TOKEN"    → verilen token'ı test eder
set -uo pipefail
ENV_FILE="$(cd "$(dirname "$0")" && pwd)/.env"
API="https://graph.facebook.com/$(grep -h '^META_API_VERSION' "$ENV_FILE" 2>/dev/null | cut -d= -f2- | tr -d ' \r\n' || echo v23.0)"

TOKEN="${1:-}"
[ -z "$TOKEN" ] && TOKEN=$(grep -h "^META_ACCESS_TOKEN" "$ENV_FILE" 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"'"'"' \t\r\n')
IG_USER_ID=$(grep -h "^META_IG_USER_ID" "$ENV_FILE" 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"'"'"' \t\r\n')
[ -z "$TOKEN" ] && { echo "✗ Token yok ($ENV_FILE içinde META_ACCESS_TOKEN boş)"; exit 1; }

echo "== 1) Token kimliği =="
me=$(curl -s -G "$API/me" --data-urlencode "fields=id,name" --data-urlencode "access_token=$TOKEN")
echo "$me"
echo "$me" | grep -q '"error"' && { echo "✗ Token geçersiz — setup_meta_token.py ile yenile."; exit 1; }

echo
echo "== 2) Son kullanma + izinler =="
curl -s -G "$API/debug_token" --data-urlencode "input_token=$TOKEN" --data-urlencode "access_token=$TOKEN" | python3 -c '
import sys, json, datetime
d = json.load(sys.stdin).get("data", {})
exp = d.get("expires_at")
print("  expires_at :", "0 → SÜRESİZ ✅" if exp in (0, None) else f"{exp} → {datetime.datetime.fromtimestamp(exp):%d.%m.%Y %H:%M} ⚠️ süreli")
print("  app        :", d.get("application"), d.get("app_id"))
print("  geçerli    :", d.get("is_valid"))
print("  izinler    :", ", ".join(d.get("scopes", [])) or "-")
'

echo
echo "== 3) @camp2uk hesabına erişim (IG ID: ${IG_USER_ID:-yok}) =="
if [ -n "$IG_USER_ID" ]; then
  curl -s -G "$API/$IG_USER_ID" --data-urlencode "fields=username,followers_count,media_count" --data-urlencode "access_token=$TOKEN"; echo
else
  echo "  ✗ .env içinde META_IG_USER_ID boş"
fi

echo
echo "== 4) Yayın izni =="
curl -s -G "$API/debug_token" --data-urlencode "input_token=$TOKEN" --data-urlencode "access_token=$TOKEN" \
  | grep -q "instagram_content_publish" \
  && echo "  ✅ instagram_content_publish var — carousel yayınlanabilir" \
  || echo "  ✗ instagram_content_publish YOK — token'ı bu izinle yeniden üret"

#!/usr/bin/env bash
# 09.10 Almanya'da yıllık izin (Almanya webinar reels 5/6) — DENTCAMP reel, caption varyant 1
# Video Asana'da değil: geçici olarak auscamp-webinar Vercel public'ine konur, yayından sonra silinir.
# Deneme:  bash yayinla_0910_almanya_yillik_izin.sh
# Canlı:   bash yayinla_0910_almanya_yillik_izin.sh --live --yes
set -euo pipefail
cd "$(dirname "$0")"
OTO="$PWD"
SRC="$HOME/Downloads/DENTCAMP Almanya Reels/05 - Yillik izin.mp4"
NAME="dc-reels-0910-yillik-izin.mp4"
WEB="$HOME/auscamp-webinar"
URL="https://auscamp-webinar.vercel.app/$NAME"
export VERCEL_TOKEN="$(tr -d ' \t\r\n' < ~/.auscamp_vercel_token)"

temizle() {
  echo "→ video public'ten siliniyor + yeniden deploy"
  rm -f "$WEB/public/$NAME"
  (cd "$WEB" && bash scripts/deploy.sh >/dev/null)
  curl -sI "$URL" | grep -i "content-type"
}
trap temizle EXIT

cp "$SRC" "$WEB/public/$NAME"
(cd "$WEB" && bash scripts/deploy.sh)
echo "→ URL kontrol"
curl -sI "$URL" | grep -iE "^HTTP|content-type|content-length"
curl -sI "$URL" | grep -qi "content-type: video/mp4" || { echo "HATA: video yayında değil"; exit 1; }

cd "$OTO"
python3 make_publish.py --brand dentcamp --ig-type reel \
  --caption cap_0910_almanya_yillik_izin_SECILEN.txt \
  --yt-title "Almanya'da diş hekimi yılda kaç gün izin kullanır? #Shorts" \
  "$@" --media "$URL"

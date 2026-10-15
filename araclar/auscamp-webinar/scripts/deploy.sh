#!/usr/bin/env bash
# AUSCAMP webinar — production deploy (Vercel, prebuilt Build Output API).
#
# Neden prebuilt: bu ortamdan Vercel'in normal build+upload'u büyük payload'da
# soket kopmasıyla başarısız oluyor; vercel.json rewrites / config.json SPA
# fallback derin route'larda (404) çalışmıyor. Çözüm: her webinar slug'ı için
# fiziksel index.html üret + prebuilt yükle (küçük payload, kesin routing).
#
# Kullanım:
#   VERCEL_TOKEN=xxxxx bash scripts/deploy.sh
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="$HOME/.bun/bin:$PATH"

[ -z "${VERCEL_TOKEN:-}" ] && { echo "HATA: VERCEL_TOKEN gerekli"; exit 1; }

echo "→ build"
bun run build

echo "→ Build Output API paketi"
rm -rf .vercel/output
mkdir -p .vercel/output/static
cp -R dist/. .vercel/output/static/

# Her webinar slug'ı için fiziksel route dosyası (SPA derin-route düzeltmesi).
SLUGS=$(grep -oE 'slug: "[^"]+"' src/config/webinars.ts | sed 's/slug: "//; s/"//')
echo "→ route dosyaları: $SLUGS"
for slug in $SLUGS; do
  mkdir -p ".vercel/output/static/webinar/$slug"
  cp dist/index.html ".vercel/output/static/webinar/$slug/index.html"
done

cat > .vercel/output/config.json <<'JSON'
{ "version": 3, "routes": [
  { "src": "/assets/(.*)", "headers": { "cache-control": "public, max-age=31536000, immutable" }, "continue": true },
  { "handle": "filesystem" },
  { "src": "/.*", "dest": "/index.html" }
] }
JSON

echo "→ deploy (prod, prebuilt)"
bunx vercel deploy --prebuilt --prod --yes --scope auscamp --token "$VERCEL_TOKEN"

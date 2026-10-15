#!/usr/bin/env python3
"""
Metricool uzerinden Instagram (ve diger aglara) gonderi zamanlar/yayinlar.

Neden: Meta developer hesabi kisitli oldugu icin kendi Graph API yolumuz kapali
(publish_instagram.py calismaz). Metricool onayli bir Meta partneri, yayini kendi
uygulamasi uzerinden yapar -> bizim kisitlamamiz onu etkilemez. Ayrica Graph API'de
olmayan ILERI TARIH ZAMANLAMA burada var.

Kimlik: X-Mc-Auth header + userId + blogId (query). Token: Metricool > Ayarlar > API
(Advanced/Custom planlarda mevcut). Kimlik bilgileri ayni klasordeki .env dosyasindan
okunur:
    METRICOOL_TOKEN=...
    METRICOOL_USER_ID=...
    METRICOOL_BLOG_ID=...        # marka (brand) id, --brands ile listelenir

Guardrail: varsayilan DRY-RUN. Gercek kayit icin --live --yes gerekir.
(bkz. feedback-auscamp-onaysiz-planlama-yok: kullanıcı onaylamadan hicbir sey planlanmaz.)

Kullanim:
  # 1) Baglantiyi ve markalari dogrula
  python3 metricool_publish.py --brands

  # 2) Zamanlanmis gonderi (dry-run -> sonra --live --yes)
  python3 metricool_publish.py \
      --network instagram \
      --caption cap.txt \
      --media "https://auscamp-webinar.vercel.app/gorsel.jpg" \
      --when "2026-08-16 13:00"

  # Taslak olarak birak (kullanıcı panelden onaylayip zamanlar):
  python3 metricool_publish.py ... --draft
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://app.metricool.com/api"
ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
DEFAULT_TZ = "Europe/Istanbul"

# Metricool'un ScheduledPost.providers[].network alaninda bekledigi adlar
NETWORKS = {
    "instagram", "facebook", "twitter", "linkedin", "tiktok",
    "youtube", "pinterest", "threads", "bluesky", "gmb",
}


def load_env(path=ENV_PATH):
    env = {}
    if not os.path.exists(path):
        return env
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def creds(args):
    env = load_env()
    token = args.token or os.environ.get("METRICOOL_TOKEN") or env.get("METRICOOL_TOKEN")
    user_id = args.user_id or os.environ.get("METRICOOL_USER_ID") or env.get("METRICOOL_USER_ID")
    blog_id = args.blog_id or os.environ.get("METRICOOL_BLOG_ID") or env.get("METRICOOL_BLOG_ID")
    if not token or not user_id:
        sys.exit(
            "HATA: METRICOOL_TOKEN ve METRICOOL_USER_ID gerekli.\n"
            f"  {ENV_PATH} dosyasina ekle ya da --token / --user-id ile ver.\n"
            "  Token: Metricool > Ayarlar (Account Settings) > API"
        )
    return token, user_id, blog_id


def call(method, path, token, params=None, body=None, timeout=60):
    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("X-Mc-Auth", token)
    req.add_header("Accept", "application/json")
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, (json.loads(raw) if raw.strip() else None)
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")
        try:
            parsed = json.loads(raw)
        except ValueError:
            parsed = raw
        return exc.code, parsed
    except urllib.error.URLError as exc:
        sys.exit(f"HATA: Metricool'a baglanilamadi: {exc.reason}")


def die_on_error(status, payload, ctx):
    if status == 401 or status == 403:
        sys.exit(
            f"HATA ({status}) {ctx}: token reddedildi.\n"
            "  - Token'i Metricool > Ayarlar > API'den yeniden kopyala.\n"
            "  - API erisimi Advanced ve Custom planlarda var; plan dusukse endpoint kapalidir.\n"
            f"  Yanit: {payload}"
        )
    if status >= 400:
        sys.exit(f"HATA ({status}) {ctx}: {json.dumps(payload, ensure_ascii=False, indent=2) if isinstance(payload, (dict, list)) else payload}")


def cmd_brands(args):
    token, user_id, _ = creds(args)
    status, payload = call("GET", "/v2/settings/brands", token, {"userId": user_id})
    die_on_error(status, payload, "markalar listelenirken")
    items = payload.get("data", payload) if isinstance(payload, dict) else payload
    if not isinstance(items, list):
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    print(f"{len(items)} marka bulundu:\n")
    for b in items:
        bid = b.get("id") or b.get("blogId")
        label = b.get("label") or b.get("title") or b.get("name") or "?"
        nets = [k for k in ("instagram", "facebook", "twitter", "linkedin", "tiktok", "threads")
                if b.get(k) or b.get(k + "Connected")]
        print(f"  blogId={bid:<12} {label}" + (f"   [{', '.join(nets)}]" if nets else ""))
    print("\nKullanacagin blogId'yi .env icine METRICOOL_BLOG_ID olarak yaz.")


def read_caption(args):
    if args.caption_text:
        return args.caption_text
    if args.caption:
        with open(args.caption, encoding="utf-8") as fh:
            return fh.read().strip()
    sys.exit("HATA: --caption <dosya> ya da --caption-text <metin> ver.")


def normalize_when(value):
    """'2026-08-16 13:00' -> '2026-08-16T13:00:00' (Metricool yerel saat + timezone bekler)."""
    v = value.strip().replace(" ", "T")
    parts = v.split("T")
    if len(parts) != 2:
        sys.exit("HATA: --when formati 'YYYY-MM-DD HH:MM' olmali.")
    hhmm = parts[1]
    if hhmm.count(":") == 1:
        hhmm += ":00"
    return f"{parts[0]}T{hhmm}"


def cmd_schedule(args):
    token, user_id, blog_id = creds(args)
    if not blog_id:
        sys.exit("HATA: blogId gerekli. Once `--brands` ile listele, sonra .env'e METRICOOL_BLOG_ID yaz.")

    network = args.network.lower()
    if network not in NETWORKS:
        sys.exit(f"HATA: bilinmeyen ag '{network}'. Gecerli: {', '.join(sorted(NETWORKS))}")

    caption = read_caption(args)
    when = normalize_when(args.when)

    for url in args.media:
        if not url.lower().startswith("https://"):
            sys.exit(
                f"HATA: medya public bir https URL olmali (yerel dosya kabul edilmez): {url}\n"
                "  Pratik yol: gorseli ~/auscamp-webinar/public/ icine koy -> scripts/deploy.sh -> URL'yi kullan.\n"
                "  Ucuncu taraf gecici host (tmpfiles/catbox) KULLANMA."
            )

    post = {
        "publicationDate": {"dateTime": when, "timezone": args.timezone},
        "text": caption,
        "providers": [{"network": network}],
        "media": list(args.media),
        "autoPublish": not args.draft,
        "draft": bool(args.draft),
        "shortener": False,
        "saveExternalMediaFiles": True,
    }
    if args.alt_text:
        post["mediaAltText"] = list(args.alt_text)
    if args.first_comment:
        post["firstCommentText"] = args.first_comment
    if network == "instagram":
        post["instagramData"] = {"autoPublish": not args.draft, "type": args.ig_type.upper()}

    params = {"userId": user_id, "blogId": blog_id}

    print("=" * 72)
    print(f"Ag           : {network}" + (f" ({args.ig_type})" if network == "instagram" else ""))
    print(f"Zaman        : {when}  ({args.timezone})")
    print(f"Mod          : {'TASLAK (draft)' if args.draft else 'OTOMATIK YAYIN'}")
    print(f"Medya        : {len(args.media)} adet")
    for url in args.media:
        print(f"               {url}")
    print(f"Caption      : {len(caption)} karakter")
    print("-" * 72)
    print(caption)
    print("=" * 72)

    if not (args.live and args.yes):
        print("\nDRY-RUN — Metricool'a hicbir sey gonderilmedi.")
        print("Gonderilecek govde:")
        print(json.dumps(post, ensure_ascii=False, indent=2))
        print("\nGercekten kaydetmek icin: --live --yes")
        return

    status, payload = call("POST", "/v2/scheduler/posts", token, params, post)
    die_on_error(status, payload, "gonderi olusturulurken")
    data = payload.get("data", payload) if isinstance(payload, dict) else payload
    post_id = (data or {}).get("id") if isinstance(data, dict) else None
    print(f"\n✓ Metricool'a kaydedildi (HTTP {status})" + (f" — post id: {post_id}" if post_id else ""))
    print("  Takvimden dogrula: https://app.metricool.com/planning")


def main():
    ap = argparse.ArgumentParser(description="Metricool ile gonderi zamanla/yayinla")
    ap.add_argument("--brands", action="store_true", help="Markalari (blogId) listele ve cik")
    ap.add_argument("--network", default="instagram", help="instagram, facebook, linkedin, ...")
    ap.add_argument("--caption", help="Caption dosyasi (utf-8)")
    ap.add_argument("--caption-text", help="Caption metni (dogrudan)")
    ap.add_argument("--media", nargs="*", default=[], help="Public https gorsel/video URL'leri (carousel icin sirayla)")
    ap.add_argument("--alt-text", nargs="*", help="Medya alt metinleri (medya sirasiyla)")
    ap.add_argument("--first-comment", help="Ilk yorum metni")
    ap.add_argument("--when", help="'YYYY-MM-DD HH:MM' yerel saat")
    ap.add_argument("--timezone", default=DEFAULT_TZ, help=f"varsayilan {DEFAULT_TZ}")
    ap.add_argument("--ig-type", default="POST", choices=["POST", "REEL", "STORY"], help="Instagram gonderi tipi")
    ap.add_argument("--draft", action="store_true", help="Otomatik yayinlama; taslak olarak birak")
    ap.add_argument("--live", action="store_true", help="Gercekten Metricool'a yaz")
    ap.add_argument("--yes", action="store_true", help="--live ile birlikte zorunlu onay")
    ap.add_argument("--token", help="METRICOOL_TOKEN yerine")
    ap.add_argument("--user-id", help="METRICOOL_USER_ID yerine")
    ap.add_argument("--blog-id", help="METRICOOL_BLOG_ID yerine")
    args = ap.parse_args()

    if args.brands:
        cmd_brands(args)
        return
    if not args.when:
        sys.exit("HATA: --when gerekli ('YYYY-MM-DD HH:MM'). Marka listesi icin --brands.")
    if not args.media:
        sys.exit("HATA: --media ile en az bir public https URL ver.")
    cmd_schedule(args)


if __name__ == "__main__":
    main()

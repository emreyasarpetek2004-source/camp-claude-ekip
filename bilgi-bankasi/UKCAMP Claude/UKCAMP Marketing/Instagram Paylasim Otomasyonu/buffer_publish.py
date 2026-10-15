#!/usr/bin/env python3
"""
Buffer uzerinden Instagram (ve diger aglara) gonderi zamanlar.

Neden: Meta developer hesabi kisitli oldugu icin kendi Graph API yolumuz kapali
(publish_instagram.py calismaz). Buffer yayini kendi uygulamasi uzerinden yapar ->
bizim kisitlamamiz onu etkilemez. Ayrica Graph API'de olmayan ILERI TARIH ZAMANLAMA
burada var. Metricool'dan farki: Buffer'da API UCRETSIZ PLANDA dahil
(1 anahtar, 3.000 istek/ay, 3 kanal, kanal basina 10 planli gonderi).

Kimlik: Authorization: Bearer <BUFFER_API_KEY>. Anahtar:
Buffer > Settings > API (https://publish.buffer.com/settings/api).
Kimlik bilgileri ayni klasordeki .env dosyasindan okunur:
    BUFFER_API_KEY=...
    BUFFER_ORG_ID=...           # --channels ile listelenir
    BUFFER_CHANNEL_ID=...       # bu markanin Instagram kanali, --channels ile listelenir

BUFFER_CHANNEL_ID icin HARDCODE FALLBACK YOK. Env bossa script durur -- cunku
UKCAMP/DENTCAMP kopyalarinda ayni AUSCAMP kanali kalirsa yanlis markanin hesabina
gonderim riski dogar (META_IG_USER_ID'de bu hatayi bir kez yasadik).

Guardrail: varsayilan DRY-RUN. Gercek kayit icin --live --yes gerekir.
(bkz. feedback-auscamp-onaysiz-planlama-yok: kullanıcı onaylamadan hicbir sey planlanmaz.)

KRITIK -- SURELI/IMZALI URL KULLANMA: Buffer medyayi gonderi YAYINLANDIGI anda ceker,
olusturuldugu anda degil. Imzali URL (S3 presigned, Asana download_url, Cloudinary
signed) createPost sirasinda calisir ama yayin vaktine kadar expire olur ve gonderi
SESSIZCE basarisiz olur. Kalici host kullan: ~/auscamp-webinar/public/ -> deploy.sh.
Script bu tur URL'leri preflight'ta reddeder.

Kullanim:
  # 1) Baglantiyi, organizasyonu ve kanallari dogrula
  python3 buffer_publish.py --channels

  # 2) Zamanlanmis carousel (dry-run -> sonra --live --yes)
  python3 buffer_publish.py \
      --caption cap.txt \
      --media "https://auscamp-webinar.vercel.app/s1.jpg" \
              "https://auscamp-webinar.vercel.app/s2.jpg" \
      --when "2026-08-16 13:00"

  # Buffer'in kendi siraya koyma mantigina birak (dueAt verilmez):
  python3 buffer_publish.py --caption cap.txt --media "..." --queue
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone as _tz
from zoneinfo import ZoneInfo

BASE = "https://api.buffer.com"
ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
DEFAULT_TZ = "Europe/Istanbul"

IMAGE_TYPES = {"image/jpeg", "image/jpg"}
VIDEO_TYPES = {"video/mp4", "video/quicktime"}
MAX_IMAGE_BYTES = 8 * 1024 * 1024
MAX_VIDEO_BYTES = 300 * 1024 * 1024

# Imzali/gecici URL isaretleri -- yayin vaktinde expire olup sessiz hataya yol acar
SIGNED_URL_MARKERS = (
    "x-amz-signature", "x-amz-credential", "x-goog-signature", "expires=",
    "signature=", "token=", "se=", "sig=",
)


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

    def pick(cli, name):
        return cli or os.environ.get(name) or env.get(name)

    token = pick(args.token, "BUFFER_API_KEY")
    org_id = pick(args.org_id, "BUFFER_ORG_ID")
    channel_id = pick(args.channel_id, "BUFFER_CHANNEL_ID")
    if not token:
        sys.exit(
            "HATA: BUFFER_API_KEY gerekli.\n"
            f"  {ENV_PATH} dosyasina ekle ya da --token ile ver.\n"
            "  Anahtar: https://publish.buffer.com/settings/api"
        )
    return token, org_id, channel_id


def gql(token, query, timeout=60, ctx="istek"):
    body = json.dumps({"query": query}).encode("utf-8")
    req = urllib.request.Request(BASE, data=body, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")
        if exc.code == 401:
            sys.exit(
                f"HATA (401) {ctx}: API anahtari reddedildi.\n"
                "  - Anahtari https://publish.buffer.com/settings/api adresinden yeniden kopyala.\n"
                "  - Buffer hesabinin e-postasi dogrulanmis olmali.\n"
                f"  Yanit: {raw}"
            )
        if exc.code == 429:
            sys.exit(
                f"HATA (429) {ctx}: istek kotasi doldu.\n"
                "  Ucretsiz plan: 3.000 istek/ay. Bir sure bekle ya da plani yukselt.\n"
                f"  Yanit: {raw}"
            )
        sys.exit(f"HATA ({exc.code}) {ctx}: {raw}")
    except urllib.error.URLError as exc:
        sys.exit(f"HATA: Buffer'a baglanilamadi: {exc.reason}")

    if payload.get("errors"):
        msgs = "\n".join(f"  - {e.get('message', e)}" for e in payload["errors"])
        sys.exit(f"HATA {ctx} (GraphQL):\n{msgs}")
    return payload.get("data") or {}


def cmd_channels(args):
    token, _, _ = creds(args)
    data = gql(token, "query { account { organizations { id name } } }",
               ctx="organizasyonlar listelenirken")
    orgs = ((data.get("account") or {}).get("organizations")) or []
    if not orgs:
        sys.exit("HATA: hesapta organizasyon bulunamadi. Buffer'da en az bir kanal bagli olmali.")

    print(f"{len(orgs)} organizasyon bulundu:\n")
    for org in orgs:
        oid = org.get("id")
        print(f"  orgId={oid}   {org.get('name') or '?'}")
        ch_data = gql(
            token,
            "query { channels(input: { organizationId: %s }) { id name service } }" % json.dumps(oid),
            ctx="kanallar listelenirken",
        )
        for ch in ch_data.get("channels") or []:
            mark = " <-- Instagram" if (ch.get("service") or "").lower() == "instagram" else ""
            print(f"      channelId={ch.get('id'):<28} {ch.get('name') or '?':<24} "
                  f"[{ch.get('service') or '?'}]{mark}")
        print()
    print("Kullanacagin degerleri .env icine yaz: BUFFER_ORG_ID ve BUFFER_CHANNEL_ID")


def read_caption(args):
    if args.caption_text:
        return args.caption_text
    if args.caption:
        with open(args.caption, encoding="utf-8") as fh:
            return fh.read().strip()
    sys.exit("HATA: --caption <dosya> ya da --caption-text <metin> ver.")


def to_utc(value, tz_name):
    """'2026-08-16 13:00' (yerel) -> '2026-08-16T10:00:00.000Z' (Buffer UTC bekler)."""
    v = value.strip().replace("T", " ")
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            naive = datetime.strptime(v, fmt)
            break
        except ValueError:
            naive = None
    if naive is None:
        sys.exit("HATA: --when formati 'YYYY-MM-DD HH:MM' olmali.")
    try:
        local = naive.replace(tzinfo=ZoneInfo(tz_name))
    except Exception as exc:
        sys.exit(f"HATA: gecersiz timezone '{tz_name}': {exc}")
    utc = local.astimezone(_tz.utc)
    if utc <= datetime.now(_tz.utc):
        sys.exit(
            f"HATA: --when gecmis bir zaman ({value} {tz_name}). Ileri bir tarih ver."
        )
    return utc.strftime("%Y-%m-%dT%H:%M:%S.000Z"), local


def probe(url, timeout=30):
    """URL'nin basliklarini dondur: (status, content_type, content_length)."""
    def _try(method, extra=None):
        req = urllib.request.Request(url, method=method)
        req.add_header("User-Agent", "Mozilla/5.0")
        if extra:
            for k, v in extra.items():
                req.add_header(k, v)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            ctype = (resp.headers.get("Content-Type") or "").split(";")[0].strip().lower()
            clen = resp.headers.get("Content-Length")
            return resp.status, ctype, (int(clen) if clen and clen.isdigit() else None)

    try:
        return _try("HEAD")
    except urllib.error.HTTPError as exc:
        if exc.code not in (403, 405, 501):
            return exc.code, None, None
    except urllib.error.URLError:
        pass
    # Bazi host'lar HEAD'i reddeder -> tek bayt GET ile dene
    try:
        return _try("GET", {"Range": "bytes=0-0"})
    except urllib.error.HTTPError as exc:
        return exc.code, None, None
    except urllib.error.URLError as exc:
        return None, f"baglanti hatasi: {exc.reason}", None


def preflight(urls, allow_signed=False):
    """Medya URL'lerini saglayiciya hic istek atmadan yerelde dogrula. Sorun varsa cikar.

    allow_signed: Buffer'da False olmali -- medyayi YAYIN aninda cektigi icin imzali URL
    o zamana kadar expire olur ve gonderi sessizce duser. Make'te True verilir: senaryo
    calisma aninda URL'yi cekip Instagram'a hemen aktarir, dolayisiyla Asana'nin sureli
    download_url'i gecerli ve tercih edilen kaynaktir.
    """
    problems = []
    kinds = []
    print("Preflight -- medya URL'leri dogrulaniyor:")
    for url in urls:
        low = url.lower()
        if not low.startswith("https://"):
            problems.append(
                f"{url}\n      -> public bir https URL olmali (yerel dosya kabul edilmez).\n"
                "         Gorseli ~/auscamp-webinar/public/ icine koy -> scripts/deploy.sh."
            )
            kinds.append(None)
            continue

        query = urllib.parse.urlparse(low).query
        hit = [] if allow_signed else [m for m in SIGNED_URL_MARKERS if m in query]
        if hit:
            problems.append(
                f"{url}\n      -> SURELI/IMZALI URL gorunuyor ({', '.join(hit)}).\n"
                "         Buffer medyayi YAYIN aninda ceker; bu URL o zamana kadar expire olur\n"
                "         ve gonderi sessizce basarisiz olur. Kalici host kullan."
            )
            kinds.append(None)
            continue

        status, ctype, clen = probe(url)
        if status != 200 and status != 206:
            problems.append(f"{url}\n      -> erisilemedi (HTTP {status}, {ctype or '-'}).")
            kinds.append(None)
            continue

        if ctype in IMAGE_TYPES:
            kind = "image"
            if clen and clen > MAX_IMAGE_BYTES:
                problems.append(f"{url}\n      -> gorsel {clen/1048576:.1f} MB, sinir 8 MB.")
        elif ctype in VIDEO_TYPES:
            kind = "video"
            if clen and clen > MAX_VIDEO_BYTES:
                problems.append(f"{url}\n      -> video {clen/1048576:.1f} MB, sinir 300 MB.")
        elif ctype == "image/png":
            kind = None
            problems.append(
                f"{url}\n      -> PNG. Instagram API'si PNG kabul ETMEZ, gonderi reddedilir.\n"
                "         JPEG'e cevir: sips -s format jpeg -Z 1350 girdi.png --out cikti.jpg"
            )
        else:
            kind = None
            problems.append(
                f"{url}\n      -> beklenmeyen Content-Type '{ctype}'.\n"
                "         Gorsel image/jpeg, video video/mp4 olmali. URL dosyaya dogrudan mi isaret ediyor?"
            )
        kinds.append(kind)
        if kind:
            size = f"{clen/1048576:.2f} MB" if clen else "boyut bilinmiyor"
            print(f"  OK  {ctype or '?':<16} {size:<18} {url}")

    if problems:
        print("\nPREFLIGHT BASARISIZ -- Buffer'a hicbir istek atilmadi:\n")
        for p in problems:
            print(f"  X {p}\n")
        sys.exit(1)
    print()
    return kinds


def build_mutation(caption, channel_id, mode, due_at, urls, kinds, ig_type,
                   share_to_feed, first_comment):
    """GraphQL mutation'i inline literal olarak kur.

    Degisken (variables) kullanilmiyor: dokumanda input tipi bir yerde PostInput,
    baska yerde CreatePostInput olarak geciyor. Inline literal her iki durumda calisir.
    Metinler json.dumps ile kacisliyor (GraphQL string literali JSON string ile uyumlu),
    enum degerleri tirnaksiz kalir.
    """
    assets = ", ".join(
        "{ %s: { url: %s } }" % (kind, json.dumps(url))
        for url, kind in zip(urls, kinds)
    )

    meta_fields = [f"type: {ig_type}", f"shouldShareToFeed: {'true' if share_to_feed else 'false'}"]
    if first_comment:
        meta_fields.append(f"firstComment: {json.dumps(first_comment)}")

    fields = [
        f"text: {json.dumps(caption)}",
        f"channelId: {json.dumps(channel_id)}",
        "schedulingType: automatic",
        f"mode: {mode}",
    ]
    if due_at:
        fields.append(f"dueAt: {json.dumps(due_at)}")
    fields.append(f"assets: [{assets}]")
    fields.append("metadata: { instagram: { %s } }" % ", ".join(meta_fields))

    return (
        "mutation CreatePost {\n"
        "  createPost(input: { %s }) {\n"
        "    ... on PostActionSuccess { post { id dueAt } }\n"
        "    ... on LimitReachedError { message }\n"
        "    ... on MutationError { message }\n"
        "  }\n"
        "}" % "\n    ".join(fields)
    )


def cmd_schedule(args):
    token, _, channel_id = creds(args)
    if not channel_id:
        sys.exit(
            "HATA: BUFFER_CHANNEL_ID gerekli (fallback yok -- yanlis markaya gonderim riski).\n"
            "  Once `--channels` ile listele, sonra .env'e BUFFER_CHANNEL_ID yaz."
        )

    caption = read_caption(args)
    if len(caption) > 2200:
        sys.exit(f"HATA: caption {len(caption)} karakter, Instagram siniri 2.200.")

    ig_type = args.ig_type
    n = len(args.media)
    if ig_type in ("reel", "story") and n != 1:
        sys.exit(f"HATA: {ig_type} icin tek medya gerekir ({n} verildi).")
    if ig_type in ("post", "carousel") and not (1 <= n <= 10):
        sys.exit(f"HATA: gonderi icin 1-10 medya gerekir ({n} verildi). Carousel: 2-10.")

    kinds = preflight(args.media)

    if args.queue:
        mode, due_at, local = "addToQueue", None, None
    else:
        if not args.when:
            sys.exit("HATA: --when gerekli ('YYYY-MM-DD HH:MM') ya da --queue kullan.")
        mode = "customScheduled"
        due_at, local = to_utc(args.when, args.timezone)

    mutation = build_mutation(
        caption, channel_id, mode, due_at, args.media, kinds, ig_type,
        share_to_feed=not args.no_share_to_feed, first_comment=args.first_comment,
    )

    carousel = " (carousel)" if n > 1 and ig_type in ("post", "carousel") else ""
    print("=" * 72)
    print(f"Kanal        : {channel_id}")
    print(f"Tip          : instagram / {ig_type}{carousel}")
    if due_at:
        print(f"Zaman        : {local.strftime('%Y-%m-%d %H:%M')} {args.timezone}  ->  {due_at} (UTC)")
    else:
        print("Zaman        : Buffer siraya koyacak (addToQueue)")
    print(f"Medya        : {n} adet")
    for url in args.media:
        print(f"               {url}")
    print(f"Caption      : {len(caption)} karakter")
    print("-" * 72)
    print(caption)
    print("=" * 72)

    if not (args.live and args.yes):
        print("\nDRY-RUN -- Buffer'a hicbir sey gonderilmedi.")
        print("Gonderilecek mutation:")
        print(mutation)
        print("\nGercekten kaydetmek icin: --live --yes")
        return

    data = gql(token, mutation, ctx="gonderi olusturulurken")
    result = data.get("createPost") or {}
    if result.get("message"):
        sys.exit(
            f"HATA: Buffer gonderiyi reddetti: {result['message']}\n"
            "  Medya URL'si ile ilgiliyse: public, dogrudan, https ve kalici olmali."
        )
    post = result.get("post") or {}
    print(f"\n✓ Buffer'a kaydedildi -- post id: {post.get('id')}")
    if post.get("dueAt"):
        print(f"  Yayin zamani (UTC): {post['dueAt']}")
    print("  Takvimden dogrula: https://publish.buffer.com/calendar")


def main():
    ap = argparse.ArgumentParser(description="Buffer ile Instagram gonderisi zamanla")
    ap.add_argument("--channels", action="store_true",
                    help="Organizasyonlari ve kanallari (channelId) listele ve cik")
    ap.add_argument("--caption", help="Caption dosyasi (utf-8)")
    ap.add_argument("--caption-text", help="Caption metni (dogrudan)")
    ap.add_argument("--media", nargs="*", default=[],
                    help="Public https gorsel/video URL'leri (carousel icin sirayla)")
    ap.add_argument("--when", help="'YYYY-MM-DD HH:MM' yerel saat")
    ap.add_argument("--timezone", default=DEFAULT_TZ, help=f"varsayilan {DEFAULT_TZ}")
    ap.add_argument("--queue", action="store_true",
                    help="Tarih verme; Buffer'in sonraki bos slotuna koy (addToQueue)")
    ap.add_argument("--ig-type", default="post", choices=["post", "carousel", "reel", "story"],
                    help="Instagram gonderi tipi. 2-10 gorsel + 'post' = carousel")
    ap.add_argument("--first-comment", help="Ilk yorum metni")
    ap.add_argument("--no-share-to-feed", action="store_true",
                    help="Reel'i feed'de gosterme (shouldShareToFeed: false)")
    ap.add_argument("--live", action="store_true", help="Gercekten Buffer'a yaz")
    ap.add_argument("--yes", action="store_true", help="--live ile birlikte zorunlu onay")
    ap.add_argument("--token", help="BUFFER_API_KEY yerine")
    ap.add_argument("--org-id", help="BUFFER_ORG_ID yerine")
    ap.add_argument("--channel-id", help="BUFFER_CHANNEL_ID yerine")
    args = ap.parse_args()

    if args.channels:
        cmd_channels(args)
        return
    if not args.media:
        sys.exit("HATA: --media ile en az bir public https URL ver. Kanal listesi icin --channels.")
    cmd_schedule(args)


if __name__ == "__main__":
    main()

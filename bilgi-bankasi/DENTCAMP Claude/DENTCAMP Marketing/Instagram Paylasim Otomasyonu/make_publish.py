#!/usr/bin/env python3
"""
Make (make.com) webhook'unu tetikleyerek Instagram gonderisi yayinlar.

SEKIL A -- "Make yayinci, karar verici degil":
Bu script takvimi taramaz, caption uretmez, karar vermez. Kullanıcı caption'i sectikten
SONRA cagrilir; Make tarafi carousel'i kurar ve Instagram'a yayinlar. Asana'ya HICBIR
SEY yazilmaz -- yayin sonrasi yorum ozelligi 31 Agu 2026'da kullanicinin karariyla kapatildi
(bkz. ASANA_YORUM_KAPATILDI.md).

Neden Make: Meta developer hesabi kisitli oldugu icin kendi Graph API yolumuz kapali
(publish_instagram.py calismaz). Make yayini kendi uygulamasi uzerinden yapar.
Buffer'a gore avantaji: Make, Asana'nin sureli download_url'ini calisma aninda cekip
Instagram'a hemen veriyor -> gorseli Vercel'e koyma adimi TAMAMEN GEREKSIZ. Ayrica
bulutta calisir, bilgisayarin kapali olmasi onemli degil.

Neden takvim taramali otomatik senaryo DEGIL: Asana task'inda caption YOK
(bkz. feedback-ukcamp-task-assign "brief, caption koyma") ve akis geregi caption'i
Kullanıcı 5 varyant arasindan seciyor (feedback-auscamp-paylas-akisi). Kendi kendine
calisan bir senaryo caption'i uydurmak zorunda kalirdi -> kural ihlali.

Kimlik: .env icindeki MAKE_WEBHOOK_URL (Make senaryosundaki Custom webhook adresi).
Webhook adresi bir SIRDIR -- adresi bilen herkes yayin tetikleyebilir. .env'de tut.

Guardrail: varsayilan DRY-RUN. Gercek yayin icin --live --yes gerekir.
(bkz. feedback-auscamp-onaysiz-planlama-yok)

Kullanim:
  # Onay sonrasi carousel yayini (once dry-run, sonra --live --yes)
  python3 make_publish.py \
      --caption cap.txt \
      --media "<asana download_url 1>" "<asana download_url 2>"

  # Tek gorsel
  python3 make_publish.py --caption cap.txt --media "<url>" --ig-type photo

  # Reels -- KAPAK SEC ve yayindan once goz ile dogrula
  python3 make_publish.py --caption cap.txt --media "<video url>" --ig-type reel \
      --cover-ms 2500 --cover-preview ~/Downloads/video.mov
  # Ureilen .kapak-2500ms.jpg dosyasini ac, kapak dogruysa --live --yes ile tekrar calistir.
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

# Kardes script'ten yeniden kullanim -- ayni klasorde, ayni konvansiyonlar.
# (buffer_publish.py sadece __main__ altinda calisir, import guvenli.)
from buffer_publish import ENV_PATH, load_env, preflight, read_caption

MAX_CAPTION = 2200

# YouTube Shorts (5 Eki 2026, kullanıcı): DENTCAMP'te her reels ayni anda YouTube'a da cikar.
# Make'in youtube:uploadVideo modulu baslik/aciklamada < ve > karakterini reddediyor;
# baslik siniri 100 karakter. Baslik = secilen caption'in ilk satiri + #Shorts.
YT_TITLE_MAX = 100
YT_SHORTS_TAG = " #Shorts"
YOUTUBE_BRANDS = {"dentcamp"}


def yt_clean(text):
    return text.replace("<", "").replace(">", "")


def yt_title_from_caption(caption):
    """Caption'in ilk bos olmayan satirindan Shorts basligi turetir (<=100 karakter)."""
    first = next((ln.strip() for ln in caption.splitlines() if ln.strip()), "")
    first = yt_clean(first)
    room = YT_TITLE_MAX - len(YT_SHORTS_TAG)
    if len(first) > room:
        cut = first[:room - 1].rsplit(" ", 1)[0].rstrip(" ,;:-")
        first = cut + "…"
    return first + YT_SHORTS_TAG


def video_duration_ms(path):
    """Yerel videonun suresi (ms). ffprobe yoksa/okunamazsa None."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", path],
            capture_output=True, text=True, timeout=30,
        )
        return int(float(out.stdout.strip()) * 1000) if out.returncode == 0 else None
    except (OSError, ValueError, subprocess.SubprocessError):
        return None


def render_cover(path, ms):
    """Kapak karesini JPEG olarak cikarir; uretilen dosyanin yolunu doner.

    Neden var: Instagram YAYINLANMIS bir reels'in kapagini DEGISTIRMIYOR -- kapak
    yalnizca paylasim aninda (thumb_offset) belirleniyor. Yanlis kare secildiyse tek
    care gonderiyi silip yeniden atmak. Bu yuzden kapak yayindan ONCE goz ile
    dogrulanmali. (14 Agu 2026'da tam bu yasandi: thumb_offset=0 idi, videonun ilk
    karesinde henuz baslik/soru yazisi ekrana girmemisti -> kapaksiz gorunen reels.)
    """
    base, _ = os.path.splitext(path)
    out = f"{base}.kapak-{ms}ms.jpg"
    try:
        res = subprocess.run(
            ["ffmpeg", "-y", "-ss", str(ms / 1000.0), "-i", path,
             "-frames:v", "1", "-q:v", "2", out],
            capture_output=True, text=True, timeout=120,
        )
    except OSError:
        return None, "ffmpeg bulunamadi -- kapak onizlemesi uretilemedi."
    if res.returncode != 0 or not os.path.exists(out):
        return None, f"ffmpeg kapak karesini cikaramadi: {res.stderr.strip()[:200]}"
    return out, None


def webhook_url(args):
    env = load_env()
    url = args.webhook or os.environ.get("MAKE_WEBHOOK_URL") or env.get("MAKE_WEBHOOK_URL")
    if not url:
        sys.exit(
            "HATA: MAKE_WEBHOOK_URL gerekli.\n"
            f"  {ENV_PATH} dosyasina ekle ya da --webhook ile ver.\n"
            "  Adres: Make senaryosundaki Custom webhook modulunun URL'si\n"
            "  (Make > senaryo > Webhooks > Custom webhook > Copy address to clipboard)."
        )
    if not url.startswith("https://"):
        sys.exit(f"HATA: webhook adresi https olmali: {url}")
    return url


def post_json(url, payload, timeout=180):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json; charset=utf-8")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", "replace")
            return resp.status, raw
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")
        if exc.code == 400 and "not accepting" in raw.lower():
            sys.exit(
                f"HATA (400): Make webhook'u istek kabul etmiyor.\n"
                "  Senaryo AKTIF mi? Make'te senaryonun sol altindaki anahtar ON olmali.\n"
                "  (Tek seferlik test icin 'Run once' da yeterli.)\n"
                f"  Yanit: {raw}"
            )
        sys.exit(f"HATA ({exc.code}) webhook tetiklenirken: {raw}")
    except urllib.error.URLError as exc:
        sys.exit(f"HATA: Make'e baglanilamadi: {exc.reason}")


def main():
    ap = argparse.ArgumentParser(description="Make webhook'u ile Instagram gonderisi yayinla")
    ap.add_argument("--caption", help="Caption dosyasi (utf-8)")
    ap.add_argument("--caption-text", help="Caption metni (dogrudan)")
    ap.add_argument("--media", nargs="*", default=[],
                    help="Gorsel/video URL'leri (carousel icin SIRAYLA). Asana download_url olabilir.")
    ap.add_argument("--ig-type", default="carousel", choices=["carousel", "photo", "reel"],
                    help="Make tarafinda hangi modulun calisacagini secer")
    ap.add_argument("--cover-ms", type=int, default=0, metavar="MS",
                    help="REELS KAPAGI: videonun kacinci milisaniyesindeki kare kapak olsun "
                         "(Instagram thumb_offset). Varsayilan 0 = ilk kare; konusan kafa "
                         "videolarinda ilk karede genelde baslik/yazi HENUZ YOK.")
    ap.add_argument("--cover-preview", metavar="VIDEO",
                    help="Yerel video dosyasinin yolu. Verilirse --cover-ms karesi JPEG olarak "
                         "cikarilir ve yayindan ONCE goz ile dogrulanabilir. Reels'te siddetle "
                         "onerilir: yayinlanmis reels'in kapagi Instagram'da DEGISTIRILEMEZ.")
    # --marka, caption_uret.py ile ayni adlandirma olsun diye takma ad (Turkce tutarlilik).
    ap.add_argument("--brand", "--marka", dest="brand", default="auscamp",
                    choices=["auscamp", "ukcamp", "dentcamp"],
                    help="Hangi markanin Make senaryosu/IG baglantisi kullanilacak")
    ap.add_argument("--no-youtube", action="store_true",
                    help="Reels'i YouTube Shorts'a GONDERME (DENTCAMP'te varsayilan: gonder)")
    ap.add_argument("--yt-title", help="YouTube basligi (verilmezse caption'in ilk satiri + #Shorts)")
    ap.add_argument("--live", action="store_true", help="Gercekten Make'i tetikle")
    ap.add_argument("--yes", action="store_true", help="--live ile birlikte zorunlu onay")
    ap.add_argument("--webhook", help="MAKE_WEBHOOK_URL yerine")
    args = ap.parse_args()

    if not args.media:
        sys.exit("HATA: --media ile en az bir URL ver.")

    caption = read_caption(args)
    if len(caption) > MAX_CAPTION:
        sys.exit(f"HATA: caption {len(caption)} karakter, Instagram siniri {MAX_CAPTION}.")

    n = len(args.media)
    if args.ig_type == "carousel" and not (2 <= n <= 10):
        sys.exit(f"HATA: carousel icin 2-10 gorsel gerekir ({n} verildi). Tek gorsel: --ig-type photo")
    if args.ig_type in ("photo", "reel") and n != 1:
        sys.exit(f"HATA: {args.ig_type} icin tek medya gerekir ({n} verildi).")

    # --- REELS KAPAGI -------------------------------------------------------
    # Instagram kapagi yalnizca paylasim aninda kabul ediyor; yayindan sonra
    # degistirilemiyor (Make modulunde de guncelleme alani yok). Bu yuzden kapak
    # burada acikca secilir ve mumkunse yayindan once JPEG olarak goz ile dogrulanir.
    if args.cover_ms < 0:
        sys.exit("HATA: --cover-ms negatif olamaz.")
    if args.cover_ms and args.ig_type != "reel":
        sys.exit(f"HATA: --cover-ms yalnizca reels icin gecerli ({args.ig_type} verildi).")

    cover_jpg = None
    if args.cover_preview:
        if not os.path.exists(args.cover_preview):
            sys.exit(f"HATA: --cover-preview dosyasi yok: {args.cover_preview}")
        sure = video_duration_ms(args.cover_preview)
        if sure is not None and args.cover_ms >= sure:
            sys.exit(
                f"HATA: --cover-ms {args.cover_ms} ms, videonun suresinden ({sure} ms) buyuk.\n"
                "  Kapak karesi videonun icinde olmali."
            )
        cover_jpg, hata = render_cover(args.cover_preview, args.cover_ms)
        if hata:
            sys.exit(f"HATA: {hata}")

    # Asana download_url'leri SURELI -- ama Make calisma aninda cekip Instagram'a
    # hemen verdigi icin sorun degil. Yine de erisilebilirligi burada dogruluyoruz;
    # preflight ayrica PNG ve yanlis Content-Type'i yakalar (Instagram JPEG istiyor).
    kinds = preflight(args.media, allow_signed=True)

    # Make'in carousel modulu (instagram-business:CreateCarouselPhoto) `files` alaninda
    # NESNE DIZISI bekliyor: her oge media_type + image_url/video_url. Bunu Make icinde
    # string dizisinden uretmek zahmetli oldugu icin hazir sekilde gonderiyoruz.
    # `media` yine gonderiliyor: photo yolu {{2.media[1]}} ile onu okuyor.
    files = [
        {"media_type": "VIDEO" if kind == "video" else "IMAGE",
         ("video_url" if kind == "video" else "image_url"): url}
        for url, kind in zip(args.media, kinds)
    ]

    # Reels rotasi video_url bekliyor: goruntu URL'si verilirse Make'te degil,
    # Meta tarafinda anlamsiz bir hata olarak donerdi -- burada erken yakala.
    if args.ig_type == "reel" and kinds[0] != "video":
        sys.exit(f"HATA: reels icin video URL'si gerekir (gelen tur: {kinds[0]}).")

    payload = {
        "brand": args.brand,
        "ig_type": args.ig_type,
        "caption": caption,
        "media": list(args.media),
        "files": files,
        # Make senaryosundaki reels rotasi bunu {{2.thumb_offset}} olarak okuyor.
        # photo/carousel rotalari kullanmiyor; her zaman gonderiliyor ki eslesme bos kalmasin.
        "thumb_offset": args.cover_ms,
    }

    youtube = (args.ig_type == "reel" and args.brand in YOUTUBE_BRANDS
               and not args.no_youtube)
    if args.yt_title and not youtube:
        sys.exit("HATA: --yt-title yalnizca YouTube'a giden reels'te gecerli.")
    # Make'teki YouTube modulu {{2.youtube}} filtresine bakiyor; her zaman gonder.
    payload["youtube"] = youtube
    if youtube:
        title = yt_clean(args.yt_title.strip()) if args.yt_title else yt_title_from_caption(caption)
        if not title.strip():
            sys.exit("HATA: YouTube basligi bos -- --yt-title ile ver.")
        if len(title) > YT_TITLE_MAX:
            sys.exit(f"HATA: YouTube basligi {len(title)} karakter, sinir {YT_TITLE_MAX}.")
        payload["yt_title"] = title
        payload["yt_description"] = yt_clean(caption)

    print("=" * 72)
    print(f"Marka        : {args.brand}")
    print(f"Tip          : {args.ig_type}")
    print(f"Medya        : {n} adet")
    for url in args.media:
        print(f"               {url[:100]}{'...' if len(url) > 100 else ''}")
    print("Asana        : yazilmayacak (yayin sonrasi yorum kapali)")
    if args.ig_type == "reel":
        print(f"Kapak        : {args.cover_ms} ms"
              f"{' (ILK KARE)' if args.cover_ms == 0 else ''}")
        if cover_jpg:
            print(f"               onizleme: {cover_jpg}")
            print("               ^ YAYINDAN ONCE AC VE BAK -- kapak sonradan degistirilemez.")
        else:
            print("               ⚠ onizleme yok. Yerel dosyayi --cover-preview ile ver:")
            print("                 kapak yanlissa tek care gonderiyi silip yeniden atmak.")
    if youtube:
        print(f"YouTube      : Shorts, herkese acik -- baslik ({len(payload['yt_title'])}):")
        print(f"               {payload['yt_title']}")
    elif args.ig_type == "reel":
        print("YouTube      : gonderilmeyecek")
    print(f"Caption      : {len(caption)} karakter")
    print("-" * 72)
    print(caption)
    print("=" * 72)

    if not (args.live and args.yes):
        print("\nDRY-RUN -- Make tetiklenmedi, Instagram'a hicbir sey gitmedi.")
        print("Gonderilecek payload:")
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        print("\nGercekten yayinlamak icin: --live --yes")
        return

    url = webhook_url(args)
    print("\nMake tetikleniyor (yayin ANINDA canli olur)...")
    status, raw = post_json(url, payload)

    try:
        parsed = json.loads(raw)
    except ValueError:
        parsed = None

    print(f"\n✓ Make yanit verdi (HTTP {status})")
    if isinstance(parsed, dict):
        if parsed.get("error"):
            sys.exit(f"HATA: Make senaryosu hata dondurdu: {parsed['error']}")
        # Make'in Instagram modulu permalink DONDURMUYOR -- tek cikti alani "Post ID".
        # Permalink sayisal medya kimliginden turetilemez (shortcode gerekir), o yuzden
        # post_id'yi de kabul ediyoruz. Gercek link istenirse senaryoya Graph API
        # cagrisi ekleyip permalink cekilir.
        permalink = parsed.get("permalink") or parsed.get("url")
        post_id = parsed.get("post_id") or parsed.get("postId") or parsed.get("id")
        if permalink:
            print(f"  Gonderi: {permalink}")
        elif post_id:
            print(f"  Gonderi Post ID: {post_id}")
            print("  Link icin: Instagram uygulamasindan ya da Business Suite'ten kontrol et.")
        else:
            print(f"  Yanit: {json.dumps(parsed, ensure_ascii=False)}")
        yt_hata = None
        if youtube:
            if parsed.get("yt_video_id"):
                print(f"  YouTube Shorts: https://youtube.com/shorts/{parsed['yt_video_id']}")
            else:
                yt_hata = parsed.get("yt_error") or "yanitta yt_video_id yok"
    else:
        print(f"  Yanit: {raw[:500]}")
        # Make webhook'u 180 sn icinde yanit alamazsa "Accepted" doner; senaryo
        # arkada calismaya devam eder. Sonucu ancak History gosterir.
        yt_hata = ("Make zamaninda yanit vermedi -- IG ve YouTube sonucunu History'den kontrol et"
                   if youtube else None)
    # Bolge hesaba gore degisir (eu1/eu2/us1...) -- webhook host'undan tureterek dogru linki ver.
    bolge = urllib.parse.urlparse(url).hostname or ""
    bolge = bolge.split(".")[1] if bolge.startswith("hook.") and bolge.count(".") >= 2 else ""
    print(f"  Make'te dogrula: https://{bolge or 'www'}.make.com/  (senaryo > History)")
    if yt_hata:
        # IG gonderisi geri alinmaz; YouTube ayrica (elle ya da yeniden) atilir.
        sys.exit(f"\n⚠ YOUTUBE: {yt_hata}\n  Instagram tarafi yukaridaki gibi; YouTube yuklemesini ayrica tamamla.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
AUSCAMP — Instagram Organik Paylaşım Otomasyonu (Content Publishing API)
========================================================================
@camp2aus hesabına Graph API ile organik gönderi yayınlar: tek görsel, carousel
(çoklu görsel) veya reels. Reklam DEĞİL — normal feed paylaşımı.

İKİ ÖNEMLİ GERÇEK:
1) Görseller/videolar PUBLIC bir https URL'den çekilir (Meta indirir). Yerel dosya
   yüklenemez. Kaynak: bir hosting/bucket ya da Asana attachment `download_url`
   (süreli/public — hemen yayında işe yarar).
2) API'de ileri tarihe ZAMANLAMA yok — `media_publish` ANINDA yayınlar. Belirli
   saatte istiyorsan bir zamanlayıcı (cron) hedef saatte bu script'i tetikler.

Kimlik: aynı Meta token (izin: instagram_content_publish, instagram_basic,
pages_show_list, pages_read_engagement). Token env'de: META_ACCESS_TOKEN.
IG hesabı: META_IG_USER_ID = @camp2aus business ID'si, .env'den gelir. ZORUNLU —
varsayılan/fallback YOKTUR; env boşsa script durur (yanlış markanın hesabına
gönderimi önlemek için).

VARSAYILAN dry-run: hiçbir şey yayınlamaz, planı yazar. --live --yes ile yayınlar.
Yayınlanan gönderi ANINDA canlıdır (feed'e düşer) — dikkat: bu geri alınamaz
(silinebilir ama yayınlanmış olur). O yüzden --live yalnız kullanıcı onayıyla.

Kullanım:
  export $(grep -v '^#' .env | xargs)     # META_ACCESS_TOKEN + META_IG_USER_ID
  # tek görsel (dry-run)
  python publish_instagram.py --type single --image https://.../1.jpg --caption-file cap.txt
  # carousel
  python publish_instagram.py --type carousel --images https://.../1.jpg https://.../2.jpg --caption-file cap.txt
  # reels
  python publish_instagram.py --type reels --video https://.../reel.mp4 --caption-file cap.txt
  # gerçekten yayınla
  python publish_instagram.py --type carousel --images ... --caption-file cap.txt --live --yes
"""
import argparse, os, sys, time

API_VERSION = os.environ.get("META_API_VERSION", "v23.0")
BASE = f"https://graph.facebook.com/{API_VERSION}"


def _requests():
    try:
        import requests; return requests
    except ImportError:
        sys.exit("HATA: 'requests' gerekli (canlı için). pip install requests")


def _env(k):
    v = os.environ.get(k)
    if not v:
        sys.exit(f"HATA: {k} ortam değişkeni tanımlı değil.")
    return v


def _handle(r):
    try:
        b = r.json()
    except ValueError:
        r.raise_for_status(); return {}
    if r.status_code >= 400 or "error" in b:
        e = b.get("error", {})
        d = e.get("error_user_msg") or e.get("error_user_title") or ""
        raise RuntimeError(f"Graph hatası ({r.status_code}): {e.get('message')} "
                           f"| code={e.get('code')} sub={e.get('error_subcode')}"
                           + (f"\n  → {d}" if d else ""))
    return b


def post(path, **data):
    data["access_token"] = _env("META_ACCESS_TOKEN")
    return _handle(_requests().post(f"{BASE}/{path}", data=data))


def get(path, **params):
    params["access_token"] = _env("META_ACCESS_TOKEN")
    return _handle(_requests().get(f"{BASE}/{path}", params=params))


def create_photo_container(ig, image_url, caption=None, carousel_item=False):
    d = {"image_url": image_url}
    if carousel_item:
        d["is_carousel_item"] = "true"
    if caption is not None:
        d["caption"] = caption
    return post(f"{ig}/media", **d)["id"]


def create_carousel_container(ig, child_ids, caption):
    return post(f"{ig}/media", media_type="CAROUSEL",
                children=",".join(child_ids), caption=caption)["id"]


def create_reels_container(ig, video_url, caption):
    return post(f"{ig}/media", media_type="REELS", video_url=video_url, caption=caption)["id"]


def wait_ready(container_id, tries=20, delay=4, label="medya"):
    """Container FINISHED olana kadar bekle. FOTOĞRAF İÇİN DE ZORUNLU.

    Beklemeden media_publish çağırmak `code=9007 sub=2207027 Media ID is not
    available` üretiyor; bu da tekrar denemelerle gereksiz başarısız çağrı
    yığını demek. Platform Terms 7.e.i.2 riskinin kaynağı buydu.
    """
    for i in range(tries):
        st = get(container_id, fields="status_code").get("status_code")
        if st == "FINISHED":
            return True
        if st == "ERROR":
            raise RuntimeError(f"{label} işleme ERROR — container {container_id}")
        time.sleep(min(delay * (1.5 ** i), 30))  # üstel backoff, tavan 30sn
    raise RuntimeError(f"{label} zamanında hazır olmadı (timeout) — container {container_id}")


def publish(ig, container_id):
    return post(f"{ig}/media_publish", creation_id=container_id)["id"]


def preflight(url):
    """Graph'a HİÇ çağrı yapmadan önce URL'yi yerel olarak doğrula.

    Meta'ya ulaşılamayan/yanlış tipte URL vermek başarısız container çağrısı
    üretir. Onu API'ye değil, burada yakalıyoruz.
    Döner: (ok: bool, mesaj: str)
    """
    if not url.startswith("https://"):
        return False, "https:// ile başlamıyor (Meta yalnız https çeker)"
    try:
        r = _requests().get(url, stream=True, timeout=20,
                            headers={"Range": "bytes=0-1023"})
    except Exception as e:
        return False, f"URL'ye erişilemedi: {type(e).__name__}"
    code = r.status_code
    ctype = (r.headers.get("Content-Type") or "").split(";")[0].strip().lower()
    clen = r.headers.get("Content-Range", "").split("/")[-1]
    r.close()
    if code not in (200, 206):
        return False, f"HTTP {code} döndü (200/206 bekleniyordu)"
    if ctype.startswith("text/") or ctype in ("", "application/octet-stream"):
        return False, f"Content-Type '{ctype or 'yok'}' — görsel/video değil (yönlendirme sayfası olabilir)"
    if not (ctype.startswith("image/") or ctype.startswith("video/")):
        return False, f"Content-Type '{ctype}' desteklenmiyor"
    try:
        mb = int(clen) / 1_000_000
        if ctype.startswith("image/") and mb > 8:
            return False, f"görsel {mb:.1f} MB — Instagram sınırı 8 MB"
    except (ValueError, TypeError):
        mb = None
    return True, f"{ctype}" + (f", {mb:.1f} MB" if mb else "")


def validate_urls(urls, warnings, live=False):
    """Yayın öncesi tüm medya URL'lerini doğrula. live=True ise hata fırlatır."""
    problems = []
    for u in urls:
        ok, msg = preflight(u)
        line = f"{'✓' if ok else '✗'} {u[:70]}{'…' if len(u) > 70 else ''} → {msg}"
        (warnings if ok else problems).append(line)
    warnings.extend(problems)
    if problems and live:
        raise RuntimeError(
            "Yayın iptal — Meta'ya hatalı URL göndermemek için önce bunları düzelt:\n  "
            + "\n  ".join(problems))


def main():
    ap = argparse.ArgumentParser(description="AUSCAMP Instagram organik paylaşım (Content Publishing API)")
    ap.add_argument("--type", choices=["single", "carousel", "reels"], required=True)
    ap.add_argument("--image", help="tek görsel public URL (single)")
    ap.add_argument("--images", nargs="+", help="carousel görsel public URL'leri (2-10)")
    ap.add_argument("--video", help="reels video public URL")
    ap.add_argument("--caption", help="metin")
    ap.add_argument("--caption-file", help="metni dosyadan oku")
    ap.add_argument("--live", action="store_true", help="gerçekten yayınla (varsayılan dry-run)")
    ap.add_argument("--yes", action="store_true", help="--live için zorunlu onay")
    args = ap.parse_args()

    # Fallback YOK (10.08.2026): env boşsa dur. Eskiden burada @camp2aus ID'si
    # hardcode duruyordu; aynı satır UKCAMP/DENTCAMP kopyalarına da taşınmıştı ve
    # env boşken yanlış markanın hesabına gönderim riski yaratıyordu. ID artık .env'de.
    ig = (os.environ.get("META_IG_USER_ID") or "").strip()
    if not ig:
        sys.exit("HATA: META_IG_USER_ID boş. .env'i yükle:\n"
                 "  export $(grep -v '^#' .env | xargs)\n"
                 "Varsayılan hesap YOKTUR — yanlış hesaba gönderimi önlemek için durdum.")
    caption = args.caption
    if args.caption_file:
        caption = open(args.caption_file, encoding="utf-8").read().strip()
    caption = caption or ""

    warnings = []
    if args.type == "single":
        if not args.image: sys.exit("--image gerekli")
        media = [args.image]
    elif args.type == "carousel":
        if not args.images or len(args.images) < 2: sys.exit("--images en az 2 URL gerekli")
        media = args.images
    else:  # reels
        if not args.video: sys.exit("--video gerekli")
        media = [args.video]
    validate_urls(media, warnings, live=args.live)

    # --- DRY-RUN ---
    if not args.live:
        print("=" * 60)
        # Hesap adı sabit yazılmaz: ig değişkeni ne ise o gösterilir, yoksa yanlış
        # ID ile çalışırken ekranda yine "@camp2aus" görünür ve yanıltır.
        hesap = "@camp2aus" if ig == "<ID>" else "⚠️ BEKLENMEYEN HESAP"
        print(f"DRY-RUN · Instagram {args.type.upper()} · {hesap} · IG_USER_ID={ig} · (yayınlanmadı)")
        print("=" * 60)
        for i, m in enumerate(media, 1):
            print(f"  medya {i}: {m}")
        print("\nCAPTION:\n  " + caption.replace("\n", "\n  "))
        print("\n⚠️  " + "\n  ".join(warnings) if warnings else "\n✓ Uyarı yok.")
        print("\nGerçek yayın için: --live --yes  (ANINDA canlı olur)")
        return

    # --- LIVE ---
    if not args.yes:
        sys.exit("Güvenlik: --live için --yes de gerekli. Yayın ANINDA canlı olur.")

    if args.type == "single":
        cid = create_photo_container(ig, media[0], caption=caption)
        print(f"✓ container: {cid} (hazır olması bekleniyor...)")
        wait_ready(cid, label="görsel")
        pid = publish(ig, cid)
    elif args.type == "carousel":
        children = []
        for i, m in enumerate(media, 1):
            c = create_photo_container(ig, m, carousel_item=True)
            wait_ready(c, label=f"slayt {i}")
            children.append(c); print(f"  ✓ slayt {i} hazır: {c}")
        cont = create_carousel_container(ig, children, caption)
        print(f"✓ carousel container: {cont} (hazır olması bekleniyor...)")
        wait_ready(cont, label="carousel")
        pid = publish(ig, cont)
    else:
        cont = create_reels_container(ig, media[0], caption)
        print(f"✓ reels container: {cont} (işleniyor...)")
        wait_ready(cont)
        pid = publish(ig, cont)

    print(f"\n✓ YAYINLANDI — media id: {pid}")
    try:
        info = get(pid, fields="permalink")
        print(f"Link: {info.get('permalink')}")
    except RuntimeError:
        pass


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        sys.exit(f"\n✗ {e}\n")
    except KeyboardInterrupt:
        sys.exit("\n✗ İptal edildi.\n")

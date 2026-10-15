#!/usr/bin/env python3
"""
Meta token kurulumu — CAMP Group (UKCAMP + AUSCAMP)
===================================================
Eski token'ın app'i silindiği için (OAuthException 190) tüm Meta otomasyonu durdu.
Bu script yeni token'ı alır, uzun ömürlüye çevirir, hangi Instagram hesaplarına
eriştiğini bulur ve ilgili .env dosyalarını günceller.

İKİ KULLANIM:

1) Graph API Explorer'dan alınan KISA ÖMÜRLÜ user token ile (app id + secret gerekir):
     python3 setup_meta_token.py --app-id 1234 --app-secret abcd --token EAAG...
   → 60 günlük uzun ömürlü token'a çevirir.

2) Business Manager'dan alınan SYSTEM USER token ile (süresiz, önerilen):
     python3 setup_meta_token.py --token EAAG...
   → çevirmez, doğrudan doğrular.

Ek bayraklar:
  --write      .env dosyalarını gerçekten günceller (varsayılan: sadece rapor)
  --api v23.0  API sürümü

Gerekli izinler: instagram_content_publish, instagram_basic, pages_show_list,
pages_read_engagement (+ reklam otomasyonu için ads_management, business_management).
"""
import argparse, json, os, sys, urllib.parse, urllib.request, datetime

ENV_FILES = [
    ("UKCAMP · IG yayın",
     "~/Documents/UKCAMP Claude/UKCAMP Marketing/Instagram Paylasim Otomasyonu/.env"),
    ("AUSCAMP · Meta reklam",
     "~/Documents/AUSCAMP Claude/AUSCAMP Marketing/Sosyal Medya Disi Reklamlar/Meta Reklam Otomasyonu/.env"),
    ("AUSCAMP · IG yayın",
     "~/Documents/AUSCAMP Claude/AUSCAMP Marketing/Instagram Paylasim Otomasyonu/.env"),
]
# .env dosyası → o markanın IG kullanıcı adı (META_IG_USER_ID bununla eşleşir)
ENV_IG_HANDLE = {
    "UKCAMP · IG yayın": "camp2uk",
    "AUSCAMP · Meta reklam": "camp2aus",
    "AUSCAMP · IG yayın": "camp2aus",
}


def get(api, path, **params):
    url = f"https://graph.facebook.com/{api}/{path}?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        try:
            return json.load(e)
        except Exception:
            return {"error": {"message": f"HTTP {e.code}"}}
    except Exception as e:
        return {"error": {"message": str(e)}}


def die(msg):
    print(f"\n✗ {msg}")
    sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--token", required=True, help="Kısa ömürlü user token VEYA system user token")
    ap.add_argument("--app-id")
    ap.add_argument("--app-secret")
    ap.add_argument("--api", default="v23.0")
    ap.add_argument("--write", action="store_true", help=".env dosyalarını güncelle")
    a = ap.parse_args()

    token = a.token.strip()

    # 1) Uzun ömürlüye çevir (app id + secret verildiyse)
    if a.app_id and a.app_secret:
        print("== 1) Uzun ömürlü token'a çevriliyor ==")
        r = get(a.api, "oauth/access_token", grant_type="fb_exchange_token",
                client_id=a.app_id, client_secret=a.app_secret, fb_exchange_token=token)
        if "error" in r:
            die(f"Çevirme başarısız: {r['error'].get('message')}")
        token = r["access_token"]
        print(f"   ✓ yeni token alındı ({len(token)} karakter)")
    else:
        print("== 1) Çevirme atlandı (app id/secret verilmedi — system user token varsayılıyor) ==")

    # 2) Doğrula
    print("\n== 2) Token doğrulanıyor ==")
    me = get(a.api, "me", fields="id,name", access_token=token)
    if "error" in me:
        die(f"Token geçersiz: {me['error'].get('message')}")
    print(f"   ✓ kimlik: {me.get('name')} ({me.get('id')})")

    dbg = get(a.api, "debug_token", input_token=token, access_token=token).get("data", {})
    exp = dbg.get("expires_at")
    if exp in (0, None):
        print("   ✓ son kullanma: SÜRESİZ")
    else:
        print("   ⚠ son kullanma:", datetime.datetime.fromtimestamp(exp).strftime("%d.%m.%Y %H:%M"))
    scopes = dbg.get("scopes", [])
    print("   izinler:", ", ".join(scopes) or "-")
    for need in ("instagram_content_publish", "instagram_basic", "pages_show_list"):
        print(("   ✓ " if need in scopes else "   ✗ EKSİK: ") + need)

    # 3) Sayfalar ve bağlı IG hesapları
    print("\n== 3) Erişilebilen Instagram hesapları ==")
    pages = get(a.api, "me/accounts",
                fields="id,name,instagram_business_account{id,username}",
                limit=100, access_token=token)
    if "error" in pages:
        die(f"Sayfa listesi alınamadı: {pages['error'].get('message')}")
    handles = {}
    for p in pages.get("data", []):
        ig = p.get("instagram_business_account")
        if ig:
            handles[ig.get("username", "").lower()] = ig["id"]
            print(f"   • {p['name']} → @{ig.get('username')} (IG ID: {ig['id']})")
        else:
            print(f"   • {p['name']} → bağlı IG hesabı yok")
    if not handles:
        die("Hiç IG Business hesabı görünmüyor. Token'ın pages_show_list + instagram_basic izni ve "
            "Kullanıcının sayfa yöneticiliği olduğundan emin ol.")

    # 4) .env dosyalarını güncelle
    print("\n== 4) .env dosyaları ==")
    for label, path in ENV_FILES:
        path = os.path.expanduser(path)
        want = ENV_IG_HANDLE[label]
        ig_id = handles.get(want)
        if not os.path.exists(path):
            print(f"   – {label}: dosya yok ({path}) — atlandı")
            continue
        if not ig_id:
            print(f"   ⚠ {label}: @{want} bu token'da görünmüyor — sadece token güncellenecek")
        lines, seen = [], set()
        with open(path) as f:
            for line in f:
                k = line.split("=", 1)[0].strip()
                if k == "META_ACCESS_TOKEN":
                    lines.append(f"META_ACCESS_TOKEN={token}\n"); seen.add(k)
                elif k == "META_IG_USER_ID" and ig_id:
                    lines.append(f"META_IG_USER_ID={ig_id}\n"); seen.add(k)
                else:
                    lines.append(line)
        if "META_ACCESS_TOKEN" not in seen:
            lines.append(f"META_ACCESS_TOKEN={token}\n")
        if ig_id and "META_IG_USER_ID" not in seen:
            lines.append(f"META_IG_USER_ID={ig_id}\n")
        if a.write:
            with open(path, "w") as f:
                f.writelines(lines)
            print(f"   ✓ {label}: güncellendi ({'@'+want+' → '+ig_id if ig_id else 'yalnız token'})")
        else:
            print(f"   (kuru çalışma) {label}: güncellenecekti ({'@'+want+' → '+ig_id if ig_id else 'yalnız token'})")

    if not a.write:
        print("\n→ Gerçekten yazmak için aynı komutu --write ile çalıştır.")
    else:
        print("\n✓ Bitti. Doğrulama:  bash check_token.sh")


if __name__ == "__main__":
    main()

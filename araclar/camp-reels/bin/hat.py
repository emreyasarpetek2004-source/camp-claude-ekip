#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CAMP REELS hattı: tek giriş noktası.

1) Hazırlık (olgu):  python3 bin/hat.py <kayit.mp4> --marka dentcamp [--ad dentcamp-0110-almanya]
     hazirla -> yerlesim -> anlar_brief. Sonunda brief yolunu basar.
2) Karar (model):    Claude, camp-reels-anlar agent'ına edit/brief.md'yi verir, dönen JSON'u edit/anlar.json'a yazar.
3) Üretim+denetim:   python3 bin/hat.py <proje_dizini> --uret [--taslak] [--no 2]
     uret -> denetle -> out/ONIZLEME.html                                   (v1: düz @camp2uk şablonu)

v2 (premium, Remotion):
  python3 bin/hat.py <proje> --kes                -> edit/klip_NN/ (klip.json + slayt şeridi)  ; kamera geçişi uyarısı
  [camp-reels-yonetmen her reels için -> edit/yonetmen_NN.json ; görsel istekleri -> camp-reels-gorsel / Higgsfield]
  python3 bin/hat.py <proje> --v2 [--no 2] [--taslak]  -> sahne.py -> Remotion render -> denetle R1-R11 -> ONIZLEME

Yayın YOK. Asana'ya yazma YOK. Çıktı yalnız out/.
"""
import argparse
import json
import os
import subprocess
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = os.path.expanduser("~/Developer/video-use/.venv/bin/python")  # numpy/PIL/scipy burada


def kos(*arg):
    print("\n$ " + " ".join(os.path.basename(a) if i == 0 else a for i, a in enumerate(arg)), flush=True)
    r = subprocess.run([PY] + list(arg), stdin=subprocess.DEVNULL)
    return r.returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("hedef", help="kayıt dosyası (hazırlık) ya da proje dizini (--uret)")
    ap.add_argument("--marka", choices=["dentcamp", "ukcamp", "auscamp"])
    ap.add_argument("--ad")
    ap.add_argument("--uret", action="store_true")
    ap.add_argument("--kes", action="store_true")
    ap.add_argument("--v2", action="store_true")
    ap.add_argument("--taslak", action="store_true")
    ap.add_argument("--no", type=int, action="append", default=[])
    a = ap.parse_args()
    b = os.path.join(KOK, "bin")

    if a.kes or a.v2:
        proje = os.path.abspath(a.hedef)
        if a.kes:
            sys.exit(kos(os.path.join(b, "kes.py"), proje, *sum((["--no", str(n)] for n in a.no), [])))
        anlar = json.load(open(os.path.join(proje, "edit", "anlar.json")))["reels"]
        nolar = a.no or [r["no"] for r in anlar]
        node = os.path.expanduser("~/.local/node/bin/node")
        env = dict(os.environ, PATH=os.path.dirname(node) + ":" + os.environ["PATH"])
        basilan = []
        for n in nolar:
            if not os.path.exists(os.path.join(proje, "edit", "yonetmen_%02d.json" % n)):
                print("reels %02d: yonetmen_%02d.json yok, atlandı" % (n, n))
                continue
            kod = kos(os.path.join(b, "sahne.py"), proje, "--no", str(n))
            if kod == 2:
                print("  (bekleyen görsel isteği var; görselsiz basılıyor)")
            elif kod:
                sys.exit("sahne.py hata")
            r = subprocess.run([node, os.path.join(KOK, "remotion", "render.mjs"), proje, str(n)] +
                               (["--taslak"] if a.taslak else []), env=env, cwd=os.path.join(KOK, "remotion"),
                               stdin=subprocess.DEVNULL)
            if r.returncode:
                sys.exit("render hata: reels %02d" % n)
            # SFX konuşmanın üstüne binince tepe -1 dBTP'yi aşabiliyor (ölçüldü: -0,9): video kopyalanır, sese limiter
            out = os.path.join(proje, "out", "reels_%02d.mp4" % n)
            gecici = out + ".tmp.mp4"
            subprocess.run([os.path.expanduser("~/.local/bin/ffmpeg"), "-nostdin", "-v", "error", "-y", "-i", out, "-c:v", "copy",
                            "-af", "alimiter=limit=0.79:attack=2:release=40:level=disabled", "-c:a", "aac", "-b:a", "192k",
                            "-ar", "48000", "-movflags", "+faststart", gecici], check=True, stdin=subprocess.DEVNULL)
            os.replace(gecici, out)
            basilan.append(str(n))
        d = kos(os.path.join(b, "denetle.py"), proje, *basilan) if basilan else 1
        kos(os.path.join(b, "onizleme.py"), proje)
        print("\nDENETİM: %s" % ("TÜM KAPILAR GEÇTİ" if d == 0 else "KALAN VAR, edit/denetim/rapor.json"))
        print("Sıradaki: camp-reels-denetci (gözle) -> kullanıcı. Önizleme: %s/out/ONIZLEME.html" % proje)
        sys.exit(d)

    if not a.uret:
        if not a.marka:
            sys.exit("--marka zorunlu")
        st = os.statvfs(os.path.expanduser("~"))
        bos_gb = st.f_bavail * st.f_frsize / 1e9
        if bos_gb < 5:
            sys.exit("Diskte %.1f GB boş: en az 5 GB gerekli" % bos_gb)
        arg = [os.path.join(b, "hazirla.py"), a.hedef, "--marka", a.marka] + (["--ad", a.ad] if a.ad else [])
        p = subprocess.run([PY] + arg, capture_output=True, text=True, stdin=subprocess.DEVNULL)
        sys.stdout.write(p.stdout)
        if p.returncode:
            sys.stderr.write(p.stderr[-2000:])
            sys.exit("hazirla başarısız")
        proje = [l.split(" ", 1)[1] for l in p.stdout.splitlines() if l.startswith("PROJE ")][0]
        if kos(os.path.join(b, "yerlesim.py"), proje) or kos(os.path.join(b, "anlar_brief.py"), proje):
            sys.exit("hazırlık başarısız")
        print("\nHAZIR. Gözle bak: %s/edit/yerlesim_kontrol.jpg" % proje)
        print("Sıradaki: camp-reels-anlar agent'ı -> %s/edit/brief.md -> JSON'u %s/edit/anlar.json'a yaz" % (proje, proje))
        print("Sonra: python3 bin/hat.py %s --uret" % proje)
        return

    proje = os.path.abspath(a.hedef)
    if not os.path.exists(os.path.join(proje, "edit", "anlar.json")):
        sys.exit("edit/anlar.json yok: önce anlar agent'ı")
    ek = (["--taslak"] if a.taslak else []) + sum((["--no", str(n)] for n in a.no), [])
    if kos(os.path.join(b, "uret.py"), proje, *ek):
        sys.exit("üretim başarısız")
    d = kos(os.path.join(b, "denetle.py"), proje)
    kos(os.path.join(b, "onizleme.py"), proje)
    print("\nDENETİM: %s" % ("TÜM KAPILAR GEÇTİ" if d == 0 else "KALAN VAR, edit/denetim/rapor.json"))
    print("Önizleme: %s/out/ONIZLEME.html" % proje)
    sys.exit(d)


if __name__ == "__main__":
    main()

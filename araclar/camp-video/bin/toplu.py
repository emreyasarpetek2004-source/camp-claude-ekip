#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tüm dersleri BÖLÜM SIRASIYLA kurgular. Her ders bittiğinde diski temizler.

Kullanım:
    python3 bin/toplu.py            # 1. bölümden başla, hepsini yap
    python3 bin/toplu.py --bas 5 --bit 10
"""
import argparse
import json
import os
import subprocess
import sys
import time

KOK = os.path.expanduser("~/camp-video")
sys.path.insert(0, os.path.join(KOK, "bin"))
import hat

YTDLP = os.path.expanduser("~/.local/bin/yt-dlp")


def proje_yolu(x):
    ad = "CH%02d %s" % (x["no"], x["chapter"])
    return os.path.join(KOK, "projects", "campverse-%s-%s" % (hat.slug(ad), x["vid"][:8]))


def onden_indir(x):
    """Sıradaki dersi ŞİMDİ indirmeye başla; bu ders kodlanırken ağ boş durmasın.

    Kilit dosyası şart: hat.py aynı dosyayı ikinci kez indirmeye kalkmasın, beklesin.
    """
    if not x:
        return
    proje = proje_yolu(x)
    ham = os.path.join(proje, "ders.mp4")
    kilit = os.path.join(proje, ".indiriliyor")
    if os.path.exists(ham) or os.path.exists(kilit):
        return
    k = hat.kayit_bul(x["vid"])
    if not k:
        return
    os.makedirs(proje, exist_ok=True)
    open(kilit, "w").write("1")
    cmd = ('%s --no-playlist -f "bv*+ba/b" -o "%s/ders.%%(ext)s" "%s" >/dev/null 2>&1; rm -f "%s"'
           % (YTDLP, proje, k["url"], kilit))
    subprocess.Popen(["bash", "-c", cmd], start_new_session=True)
    print("      (sonraki ders onden indiriliyor: CH%02d)" % x["no"])
    time.sleep(15)   # Loom hiz siniri: istekler arasina asgari aralik


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bas", type=int, default=1)
    ap.add_argument("--bit", type=int, default=999)
    ap.add_argument("--kuru", action="store_true")
    a = ap.parse_args()

    wa = json.load(open(os.path.join(KOK, "takip/ders_kayitlari.json")))["kayit"]
    lm = json.load(open(os.path.expanduser("~/campverse-slides/mufredat/loom_mapped.json")))
    wa_vid = {k["loom_vid"] for k in wa}
    dersler = sorted([x for x in lm if x.get("no") and x["vid"] in wa_vid],
                     key=lambda x: x["no"])
    dersler = [x for x in dersler if a.bas <= x["no"] <= a.bit]
    print("SIRA: %d ders (bolum %d-%d)\n" % (len(dersler), dersler[0]["no"], dersler[-1]["no"]))

    kayit = []
    for idx, x in enumerate(dersler):
        hedef = os.path.join(KOK, "teslim/campverse", "%02d - %s.mp4" % (x["no"], x["chapter"].strip()))
        if os.path.exists(hedef):
            print("CH%02d %-42s zaten var, atlandi" % (x["no"], x["chapter"][:42]))
            continue
        t = time.time()
        if not a.kuru:
            onden_indir(dersler[idx + 1] if idx + 1 < len(dersler) else None)
        cmd = ["python3", os.path.join(KOK, "bin/hat.py"), x["vid"]]
        if a.kuru:
            cmd.append("--kuru")
        r = subprocess.run(cmd, capture_output=True, text=True)
        ok = "TESLIM:" in r.stdout
        ozet = [l for l in r.stdout.splitlines() if "kesim:" in l or "TESLIM" in l
                or "DENETIM" in l or "HATA" in l or "DUR:" in l or "UYARI" in l]
        print("CH%02d %-42s %s  (%.1f dk)" % (x["no"], x["chapter"][:42],
                                              "OK" if ok else "SORUN", (time.time() - t) / 60))
        for o in ozet:
            print("      " + o.strip())
        if not ok:
            print("      " + (r.stdout.strip().splitlines() or ["?"])[-1][:200])
        kayit.append({"no": x["no"], "bolum": x["chapter"], "ok": ok})
        pes_pese = 0
        for k in reversed(kayit):
            if k["ok"]:
                break
            pes_pese += 1
        if pes_pese >= 2:
            print("\nDUR: ust uste %d ders basarisiz. Sebep bulunmadan devam etmek"
                  " Loom hiz sinirini tetikliyor." % pes_pese)
            break
        json.dump(kayit, open(os.path.join(KOK, "takip/toplu_durum.json"), "w"),
                  ensure_ascii=False, indent=1)
    print("\nBITTI: %d/%d basarili" % (sum(1 for k in kayit if k["ok"]), len(kayit)))


if __name__ == "__main__":
    main()

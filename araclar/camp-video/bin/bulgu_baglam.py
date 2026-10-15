#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Teslim taramasindaki bulgular icin BAGLAM cikarir ve kurgu zamanini
KAYNAK zamanina cevirir, boylece kesim listesine eklenebilir hale gelir.
"""
import json, os, sys, glob

KOK = os.path.expanduser("~/camp-video")
D = os.path.join(KOK, "takip", "teslim_tarama")

def proje_bul(teslim_ad):
    """'16 - ABDOMINAL PAIN' -> projects/campverse-ch16-...'"""
    no = teslim_ad.split(" - ")[0].strip()
    for p in sorted(glob.glob(os.path.join(KOK, "projects", "*"))):
        if os.path.basename(p).startswith("campverse-ch%s-" % no):
            return p
    return None

def kaynak_zamani(edl, t):
    """kurgu saniyesi -> kaynak saniyesi"""
    akan = 0.0
    for r in edl["ranges"]:
        b, e = r["start"], r["end"]
        if akan <= t <= akan + (e - b):
            return b + (t - akan)
        akan += e - b
    return None

def baglam(segler, bas, once=45.0, sonra=35.0):
    return [s for s in segler if s["bit"] >= bas - once and s["bas"] <= bas + sonra]

if __name__ == "__main__":
    turler = set(sys.argv[1:]) or {"meta", "ilan", "sozsuz_ses"}
    for f in sorted(os.listdir(D)):
        if not f.endswith(".json"): continue
        d = json.load(open(os.path.join(D, f)))
        bulgular = [b for b in d.get("bulgu", []) if b["tur"] in turler]
        if not bulgular: continue
        ders = f[:-5]
        p = proje_bul(ders)
        edl = json.load(open(os.path.join(p, "edit", "edl.json"))) if p and os.path.exists(os.path.join(p,"edit","edl.json")) else None
        print("\n" + "=" * 78)
        print("%s   (%s)" % (ders, os.path.basename(p) if p else "PROJE YOK"))
        for b in bulgular:
            ks = kaynak_zamani(edl, b["bas"]) if edl else None
            print("\n  --- %s  kurgu %.1f  ·  KAYNAK %s" %
                  (b["tur"], b["bas"], ("%.1f" % ks) if ks else "?"))
            for s in baglam(d.get("segment", []), b["bas"]):
                im = ">>" if abs(s["bas"] - b["bas"]) < 0.6 else "  "
                print("   %s [%7.1f-%7.1f] %s" % (im, s["bas"], s["bit"], s["metin"]))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kesim YARIM CUMLE ustunde mi basliyor, onu bulur.

Kullanıcı (23.09.2026): "burayi keselim diyor ya, oncesine de her zaman dikkat;
boyle yarim cumle varsa o da gitmeli."

Hoca yeniden cekim ilan etmeden once genelde cumleye baslayip bitiremiyor.
Model kesimi ilanin basindan aliyor, bu da yarim cumleyi videoda birakiyor.
Burada kesim sinirinin bir cumlenin ORTASINA dusup dusmedigine bakilir; dusuyorsa
o cumlenin basi (tamamlanan son cumlenin sonu) onerilir.
"""
import json
import os
import re
import sys

KOK = os.path.expanduser("~/camp-video")
sys.path.insert(0, os.path.join(KOK, "bin"))
from tekrar_bul import segmentleri_birlestir  # noqa: E402

BITIS = re.compile(r"[.!?]\s*$")


def main():
    acik = 0
    for ad in sorted(os.listdir(os.path.join(KOK, "projects"))):
        edit = os.path.join(KOK, "projects", ad, "edit")
        ty = os.path.join(edit, "transkript_tam.json")
        ey = os.path.join(edit, "edl.json")
        if not (os.path.exists(ty) and os.path.exists(ey)):
            continue
        try:
            seg = [x for w in json.load(open(ty))["pencere"] for x in w["segment"]]
            seg.sort(key=lambda s: s["bas"])
            seg = segmentleri_birlestir(seg)
            edl = json.load(open(ey))
        except Exception:
            continue
        rs = edl["ranges"]
        for i in range(len(rs) - 1):
            if rs[i].get("source") != "DERS":
                continue
            S = float(rs[i]["end"])
            for s in seg:
                a, b = float(s["bas"]), float(s["bit"])
                # cumle kesim sinirini ASIYOR ve icine en az 1 sn giriyor
                if a + 0.4 < S < b - 1.0:
                    kalan = s["metin"][:70]
                    if BITIS.search(s["metin"][:int(len(s["metin"]) * (S - a) / max(0.01, b - a))]):
                        break          # kesimden onceki kisim zaten cumle bitirmis
                    print("  %-42s kesim %8.2f  cumle %8.2f-%8.2f  uzatma %.1f sn"
                          % (ad.replace("campverse-", "")[:42], S, a, b, S - a))
                    print("      %s" % kalan)
                    acik += 1
                    break
    print("\nYARIM CUMLE USTUNDE BASLAYAN KESIM: %d" % acik)


if __name__ == "__main__":
    main()

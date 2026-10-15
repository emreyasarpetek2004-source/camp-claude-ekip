#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Anlar agent'ı için brief (OLGU katmanı): zaman damgalı cümleler + o anki ekran düzeni.

Satır biçimi:  [bas-son] (D) cümle
  D = P paylaşım (slayt+konuşmacı) | K yalnız konuşmacı | S yalnız slayt
Uzun duraklamalar (>=1,5 sn) ayrı satır olarak işaretlenir; konu geçişini görmeyi kolaylaştırır.

Kullanım: python3 bin/anlar_brief.py <proje>   ->  edit/brief.md
"""
import json
import os
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    proje = os.path.abspath(sys.argv[1])
    meta = json.load(open(os.path.join(proje, "proje.json")))
    kj = json.load(open(os.path.join(proje, "edit", "kelimeler.json")))
    yer = json.load(open(os.path.join(proje, "edit", "yerlesim.json")))
    ornek = yer["ornek"]
    harf = {"paylasim": "P", "konusmaci": "K", "slayt": "S"}

    def duzen(t):
        o = min(ornek, key=lambda x: abs(x["t"] - t)) if ornek else None
        return harf.get(o["tip"], "?") if o else "?"

    # whisper segmentleri parçalı gelir; cümle sonu (. ? !) ya da 0,8 sn duraklamaya kadar birleştir
    birlesik = []
    for c in kj["cumle"]:
        o = birlesik[-1] if birlesik else None
        if o and c["b"] - o["e"] < 0.8 and not o["metin"].rstrip().endswith((".", "?", "!")) and c["e"] - o["b"] < 30:
            o["e"] = c["e"]
            o["metin"] = o["metin"].rstrip() + " " + c["metin"].lstrip()
        else:
            birlesik.append({"b": c["b"], "e": c["e"], "metin": c["metin"]})

    satir, onceki_son = [], None
    for c in birlesik:
        if onceki_son is not None and c["b"] - onceki_son >= 1.5:
            satir.append("   -- %.1f sn duraklama --" % (c["b"] - onceki_son))
        satir.append("[%.1f-%.1f] (%s) %s" % (c["b"], c["e"], duzen(c["b"]), c["metin"]))
        onceki_son = c["e"]

    sure = float(json.load(open(os.path.join(proje, "edit", "probe.json")))["format"]["duration"])
    bas = ("# ANLAR BRIEF: %s\n\nMarka: %s | Kayıt: %.0f dk | Düzen dağılımı: %s\n"
           "Düzen kodu: P = slayt + konuşmacı (tercih edilen), K = yalnız konuşmacı, S = yalnız slayt\n"
           "Zamanlar saniye. Cümleler whisper segmentidir; kesim sınırını script kelimeye oturtur.\n\n"
           % (meta["ad"], meta["marka"].upper(), sure / 60, yer.get("dagilim")))
    out = os.path.join(proje, "edit", "brief.md")
    open(out, "w").write(bas + "\n".join(satir) + "\n")
    print("%d satır -> %s" % (len(satir), out))


if __name__ == "__main__":
    main()

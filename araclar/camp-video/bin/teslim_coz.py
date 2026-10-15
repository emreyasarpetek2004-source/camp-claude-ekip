#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kayitli teslim taramasini YENIDEN cozumler (ASR calistirmadan).

Kalip degistiginde 51 videoyu bastan dinlemek gerekmesin diye segmentler
JSON'da saklaniyor. (23.09.2026)
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from teslim_tara import ILAN, META

KOK = os.path.expanduser("~/camp-video")
D = os.path.join(KOK, "takip", "teslim_tarama")

for f in sorted(os.listdir(D)):
    if not f.endswith(".json"):
        continue
    d = json.load(open(os.path.join(D, f)))
    if not isinstance(d.get("segment"), list):
        print("%-46s ESKI BICIM, yeniden taranmali" % f[:46]); continue
    yeni = [b for b in d.get("bulgu", []) if b["tur"] == "sozsuz_ses"]
    for s in d.get("segment", []):
        if ILAN.search(s["metin"]):
            yeni.append({"tur": "ilan", "bas": s["bas"], "bit": s["bit"], "metin": s["metin"]})
        elif META.search(s["metin"]):
            yeni.append({"tur": "meta", "bas": s["bas"], "bit": s["bit"], "metin": s["metin"]})
    yeni.sort(key=lambda b: b["bas"])
    d["bulgu"] = yeni
    json.dump(d, open(os.path.join(D, f), "w"), ensure_ascii=False, indent=1)
    il = sum(1 for b in yeni if b["tur"] == "ilan")
    me = sum(1 for b in yeni if b["tur"] == "meta")
    so = sum(1 for b in yeni if b["tur"] == "sozsuz_ses")
    print("%-46s %2d ilan · %2d meta · %2d sozsuz" % (f[:46], il, me, so))
    for b in yeni:
        if b["tur"] != "sozsuz_ses":
            print("     %d:%05.2f  %-4s %s" % (b["bas"]//60, b["bas"]%60, b["tur"], b["metin"][:88]))

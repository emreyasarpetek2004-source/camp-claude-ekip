#!/usr/bin/env python3
"""Balon planlarini yeniden uretir; YAMA geometrisi degismeyen derste plan dosyasinin tarihini
geri alir ki kuyruk o dersi bosuna yeniden basmasin. Degisenleri listeler. (06.10.2026)
Kullanim: bin/plan_yenile.py projects/campverse-ch*   (ch70 atlanir: plan yok)
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import balon_plan

degisen = []
for pr in sys.argv[1:]:
    pr = pr.rstrip("/"); pp = os.path.join(pr, "edit", "balon_plan.json")
    if not os.path.exists(pp):
        continue
    eski = json.load(open(pp)); st = os.stat(pp)
    yeni = balon_plan.plan(pr)
    yeni = json.load(open(pp))
    ayni = all(eski.get(k) == yeni.get(k) for k in ("yama", "x", "y", "cap", "balon_kaynak", "balonsuz"))
    if ayni:
        os.utime(pp, (st.st_atime, st.st_mtime))
    else:
        degisen.append(os.path.basename(pr)[10:40])
print("plani degisen %d ders: %s" % (len(degisen), " ".join(degisen)))

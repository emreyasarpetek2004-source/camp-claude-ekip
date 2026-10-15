#!/usr/bin/env python3
"""dikis_bulgu_*.json duzeltmelerini kesim_nihai.json'a isler (05.10.2026).
Islenen bulgu dosyasi takip/.dikis_islendi_<grup> ile isaretlenir."""
import glob, json, os, sys
KOK = os.path.expanduser("~/camp-video")
dokunulan = set()
for bf in sorted(glob.glob(KOK + "/takip/dikis_bulgu_*.json")):
    g = os.path.basename(bf)[12:-5]; isaret = KOK + "/takip/.dikis_islendi_" + g
    if os.path.exists(isaret) and os.path.getmtime(isaret) >= os.path.getmtime(bf): continue
    for d in json.load(open(bf)).get("duzelt", []):
        p = glob.glob(KOK + "/projects/" + d["ders"].split("/")[-1] + "*")
        if not p: print("ders yok", d["ders"]); continue
        nf = p[0] + "/edit/kesim_nihai.json"; n = json.load(open(nf))
        ea, eb = d["eski"]; ya, yb = d["yeni"]
        k = min(n["kesimler"], key=lambda k: abs(k["bas"] - ea) + abs(k["bit"] - eb))
        if abs(k["bas"] - ea) + abs(k["bit"] - eb) > 1.0:
            print("eslesmedi", d["ders"][10:30], d["eski"]); continue
        k["bas"], k["bit"] = float(ya), float(yb)
        k["gerekce"] = (k.get("gerekce", "") + " | dikis denetimi: " + d.get("aciklama", ""))[:500]
        L = sorted(n["kesimler"], key=lambda x: x["bas"]); M = []
        for x in L:
            if M and x["bas"] <= M[-1]["bit"] + 0.3:
                M[-1]["bit"] = max(M[-1]["bit"], x["bit"])
            else: M.append(x)
        n["kesimler"] = M; json.dump(n, open(nf, "w"), ensure_ascii=False, indent=1)
        dokunulan.add(p[0]); print(g, d["ders"][10:30], "#%s" % d.get("n"), d["eski"], "->", d["yeni"], "kusur", d.get("kusur"))
    open(isaret, "w").write("ok")
open(KOK + "/takip/.dikis_dokunulan", "w").write("\n".join(sorted(dokunulan)))

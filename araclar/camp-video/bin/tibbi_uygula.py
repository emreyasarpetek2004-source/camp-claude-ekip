#!/usr/bin/env python3
"""tibbi_karar.json'daki "kes" kararlarini kesim_nihai.json'a ekler (05.10.2026).
Islenen karar edit/.tibbi_islendi ile isaretlenir; karar degisirse yeniden islenir.
Sonra bin/nihai_hepsi.sh calistirilmali (EDL + kontrol)."""
import glob, json, os
for f in sorted(glob.glob(os.path.expanduser("~/camp-video/projects/*/edit/tibbi_karar.json"))):
    e = os.path.dirname(f); isaret = e + "/.tibbi_islendi"
    if os.path.exists(isaret) and os.path.getmtime(isaret) >= os.path.getmtime(f):
        continue
    t = json.load(open(f)); nf = e + "/kesim_nihai.json"; n = json.load(open(nf))
    L = list(n["kesimler"])
    for k in t.get("kes", []):
        L.append({"bas": float(k["bas"]), "bit": float(k["bit"]), "tur": "tibbi_hata", "kaynak": "tibbi",
                  "gerekce": "TIBBI HATA: '%s' (dogrusu: %s)" % (k.get("yanlis", ""), k.get("dogrusu", "")),
                  "dikis": k.get("dikis", "")})
    L.sort(key=lambda x: x["bas"]); M = []
    for x in L:
        if M and x["bas"] <= M[-1]["bit"] + 0.3:
            M[-1]["bit"] = max(M[-1]["bit"], x["bit"])
            M[-1]["gerekce"] = (M[-1].get("gerekce", "") + " + " + x.get("gerekce", ""))[:500]
            if x.get("talimat"): M[-1]["talimat"] = x["talimat"]
        else:
            M.append(dict(x))
    n["kesimler"] = M
    json.dump(n, open(nf, "w"), ensure_ascii=False, indent=1)
    open(isaret, "w").write("ok")
    print(os.path.basename(os.path.dirname(e))[10:40], "+%d tibbi kesim" % len(t.get("kes", [])),
          "| kalsin %d | ele %d" % (len(t.get("kalsin", [])), len(t.get("ele", []))))

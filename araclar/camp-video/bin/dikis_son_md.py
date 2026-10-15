#!/usr/bin/env python3
"""kesim_metni_son.json -> edit/dikis_son.md (denetim icin kisa metin)."""
import glob, json, os
for f in sorted(glob.glob(os.path.expanduser("~/camp-video/projects/*/edit/kesim_metni_son.json"))):
    e = os.path.dirname(f); km = json.load(open(f))
    try: tur = {(round(k["bas"], 1), round(k["bit"], 1)): k.get("tur", "") for k in json.load(open(e + "/model_kesim.json"))["kesimler"]}
    except Exception: tur = {}
    w = lambda L: " ".join("%s@%.2f" % (x[2], x[0]) for x in L)
    out = []
    for i, k in enumerate(km, 1):
        t = min(tur.items(), key=lambda kv: abs(kv[0][0] - k["bas"]) + abs(kv[0][1] - k["bit"]))[1] if tur else ""
        out += ["#%d  ham %.2f–%.2f (%.1f sn) [%s]" % (i, k["bas"], k["bit"], k["bit"] - k["bas"], t),
                "   ÖNCE : …" + w(k["once"][-8:]), "   KESİK: " + w(k["ic"])[:600], "   SONRA: " + w(k["sonra"][:8]) + "…", ""]
    open(e + "/dikis_son.md", "w").write("\n".join(out))
print("ok")

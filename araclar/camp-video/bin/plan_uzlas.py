#!/usr/bin/env python3
"""final.mp4 hangi balon planiyla basildi (edit/yerlesim.json) -> guncel balon_plan.json ile ayni mi?
Degilse final silinir, kuyruk yeniden basar. Uretimdeki derse (.uretiliyor) dokunulmaz. (06.10.2026)
Kullanim: bin/plan_uzlas.py [--kuru]
"""
import glob, json, os, sys
KOK = os.path.expanduser("~/camp-video")
kuru = "--kuru" in sys.argv
ANAH = ("yama", "x", "y", "cap", "balon_kaynak", "balonsuz")
sil = []
for e in sorted(glob.glob(KOK + "/projects/campverse-ch*/edit")):
    pp, yj, fin = e + "/balon_plan.json", e + "/yerlesim.json", e + "/final.mp4"
    if not (os.path.exists(pp) and os.path.exists(fin)) or os.path.isdir(e + "/.uretiliyor"):
        continue
    plan = json.load(open(pp))
    try:
        kul = json.load(open(yj)).get("balon_plan") or {}
    except (OSError, ValueError):
        kul = {}
    def norm(k, v):
        if k == "yama" and isinstance(v, dict):
            v = {a: b for a, b in v.items() if not (a == "sag" and not b)}   # sag:0 = alan yok
        return v or None
    fark = [k for k in ANAH if norm(k, kul.get(k)) != norm(k, plan.get(k))]
    if not fark:
        # Plan icerikce ayni: tarihi finalden eskiye cek ki kuyruk bosuna yeniden basmasin
        fm = os.path.getmtime(fin)
        if os.path.getmtime(pp) >= fm and not kuru:
            os.utime(pp, (fm - 60, fm - 60))
    if fark:
        sil.append((os.path.basename(os.path.dirname(e))[10:16], fark))
        if not kuru:
            os.remove(fin)
            for f in (e + "/.denetim_kaldi",):
                if os.path.exists(f): os.remove(f)
print("yeniden basilacak %d ders:" % len(sil), " ".join("%s(%s)" % (a, ",".join(b)) for a, b in sil))

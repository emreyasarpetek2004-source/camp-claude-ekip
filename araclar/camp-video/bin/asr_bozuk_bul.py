#!/usr/bin/env python3
"""Tam transkriptte bozuk (dongu / uydurma / bos) araliklari mekanik olarak bulur.

05.10.2026: ilk 17 dersin yeniden taramasinda bozuk aralik alani yoktu; CH15'te
2982-3362 (6 dk) okunamadan kaldi. Bu arac her derste:
  - ayni metin >=3 kez ust uste (dongu)
  - bilinen uydurma kaliplari ("izlediginiz icin", "altyazi", "abone ol", ...)
  - sessizlik haritasi konusma gosterirken >=8 sn metinsiz bosluk
bulur ve yeniden_tarama.json'daki asr_bozuk'a EKLER (zaten olanlari tekrar etmez).
"""
import glob, json, os, re
UYDURMA = re.compile(r"(izlediğiniz için|altyazı|abone ol|bir sonraki videoda görüşmek|beğenmeyi unutmayın)", re.I)
for p in sorted(glob.glob(os.path.expanduser("~/camp-video/projects/*/edit"))):
    try:
        tr = json.load(open(p + "/transkript_tam.json")); ses = json.load(open(p + "/sessizlik.json"))
        yt_yol = p + "/yeniden_tarama.json"; yt = json.load(open(yt_yol))
    except Exception:
        continue
    seg = [x for w in tr.get("pencere", []) for x in w.get("segment", [])] if isinstance(tr, dict) and "pencere" in tr \
        else tr.get("segments", tr if isinstance(tr, list) else [])
    seg = [{"start": x.get("bas", x.get("start")), "end": x.get("bit", x.get("end")),
            "text": x.get("metin", x.get("text", ""))} for x in seg]
    son = ses["toplam_sure"]; aday = []
    for i, s in enumerate(seg):
        t = (s.get("text") or "").strip()
        if UYDURMA.search(t) and s["start"] < son - 20:
            aday.append((s["start"], s["end"]))
        if i >= 2 and t and t == (seg[i-1].get("text") or "").strip() == (seg[i-2].get("text") or "").strip():
            aday.append((seg[i-2]["start"], s["end"]))
    bos = ses["bosluk"]
    for a, b in zip(seg, seg[1:]):
        g0, g1 = a["end"], b["start"]
        if g1 - g0 >= 8:
            sessiz = sum(max(0, min(g1, x["bit"]) - max(g0, x["bas"])) for x in bos)
            if sessiz < 0.5 * (g1 - g0):
                aday.append((g0, g1))
    aday.sort(); birles = []
    for a, b in aday:
        if birles and a <= birles[-1][1] + 2: birles[-1][1] = max(birles[-1][1], b)
        else: birles.append([a, b])
    var = yt.get("asr_bozuk") or []
    yeni = [{"bas": round(a, 1), "bit": round(b, 1)} for a, b in birles
            if not any(min(b, v["bit"]) - max(a, v["bas"]) > 0 for v in var)]
    if yeni:
        yt["asr_bozuk"] = var + yeni
        json.dump(yt, open(yt_yol, "w"), ensure_ascii=False, indent=1)
        print(os.path.basename(os.path.dirname(p))[10:40], len(yeni), "yeni bozuk aralik", round(sum(x["bit"]-x["bas"] for x in yeni)), "sn")

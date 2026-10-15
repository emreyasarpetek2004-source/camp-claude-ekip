#!/usr/bin/env python3
"""Videoda kalan >=2 sn duraklamalari ~0,7 sn'ye kisaltir (05.10.2026, kullanıcı: "akisi bozan
bosluklar"). Kesim tamamen sessizligin icinde: [bas+0,35, bit-0,35]. Ekran o sirada
DURAGAN degilse (hoca yaziyor/ciziyor) dokunulmaz: freezedetect donuk orani >= %70 sart.
Cikti: kesim_nihai.json'a "tur": "bosluk" kesimleri eklenir; edit/bosluk_rapor.json."""
import glob, json, os, re, subprocess, sys
FF = os.path.expanduser("~/.local/bin/ffmpeg")
ESIK, PAY = 2.0, 0.35
import numpy as np
W, H = 480, 270
def donuk_oran(ham, a, b):
    """Kalem cizgisi ekranin kucuk bir alanini degistirir; ortalama farka bakan
    freezedetect onu GORMUYOR (CH11 1828: hoca yaziyordu, %100 'donuk' cikti).
    Burada ardisik kareler arasinda |fark|>30 olan PIKSEL SAYISI olculur."""
    q = subprocess.run([FF, "-nostats", "-v", "error", "-ss", "%.3f" % a, "-t", "%.3f" % (b - a), "-i", ham,
                        "-vf", "fps=6,scale=%d:%d,format=gray" % (W, H), "-an", "-f", "rawvideo", "-"],
                       capture_output=True)
    f = np.frombuffer(q.stdout, dtype=np.uint8)
    k = len(f) // (W * H)
    if k < 2: return 1.0
    f = f[:k * W * H].reshape(k, H, W).astype(np.int16)
    m = np.ones((H, W), bool)
    m[: int(H * 0.36), int(W * 0.80):] = False   # kamera balonu (sag ust)
    m[:, : int(W * 0.09)] = False                 # Loom paneli/sayac (sol serit)
    degisen = ((np.abs(np.diff(f, axis=0)) > 30) & m).sum(axis=(1, 2))
    return float((degisen < 8).mean())   # 8 pikselden az degisim = duragan
hedef = sys.argv[1:] or sorted(glob.glob(os.path.expanduser("~/camp-video/projects/*")))
for p in hedef:
    e = p + "/edit"
    try:
        edl = json.load(open(e + "/edl.json")); bos = json.load(open(e + "/sessizlik.json"))["bosluk"]
        n = json.load(open(e + "/kesim_nihai.json"))
    except Exception:
        continue
    if os.path.exists(e + "/bosluk_rapor.json"):
        continue
    d = [r for r in edl["ranges"] if r["source"] == "DERS"]; ham = p + "/ders.mp4"
    rap = {"kisaltildi": [], "dokunulmadi": []}
    for x in bos:
        for r in d:
            a = max(x["bas"], r["start"]); c = min(x["bit"], r["end"])
            if c - a >= ESIK and a > r["start"] + 0.5 and c < r["end"] - 0.5:
                o = donuk_oran(ham, a, c)
                k = {"bas": round(a + PAY, 3), "bit": round(c - PAY, 3), "sure": round(c - a, 2), "donuk": round(o, 2)}
                if o >= 0.7:
                    rap["kisaltildi"].append(k)
                    n["kesimler"].append({"bas": k["bas"], "bit": k["bit"], "tur": "bosluk", "kaynak": "bosluk",
                                          "gerekce": "%.1f sn duraklama 0,7 sn'ye kisaltildi (ekran duragan %%%d)" % (c - a, o * 100)})
                else:
                    rap["dokunulmadi"].append(k)
    n["kesimler"].sort(key=lambda z: z["bas"])
    json.dump(n, open(e + "/kesim_nihai.json", "w"), ensure_ascii=False, indent=1)
    json.dump(rap, open(e + "/bosluk_rapor.json", "w"), ensure_ascii=False, indent=1)
    print(os.path.basename(p)[10:40], "kisaltildi", len(rap["kisaltildi"]), "| yaziyor, dokunulmadi", len(rap["dokunulmadi"]), flush=True)

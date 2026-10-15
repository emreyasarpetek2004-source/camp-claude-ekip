#!/usr/bin/env python3
"""Hayalet (orijinal balonun kart icinde kalan izi) ciktida kalmis mi? (05.10.2026)

Halka = hayalet maskesi icinde, yeni balonun disinda kalan alan. Ciktinin bir anini sesle
ham kayda hizalar (balon_senkron.ses_ofset), ham karti 1920x1080'e olcekler; halkadaki
piksellerin hamdakine 8/255'ten yakin olani "hayalet" sayilir. Dolgu iyiyse oran dusuk.
Renk istatistigi bu ayrimi yapamadi (ok logosu ortalamayi cekiyor, ince gri halka kaciyor).
Kullanim: bin/hayalet_kontrol.py <edit klasoru> [--n 6]   cikis 1 = hayalet var
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import balon_senkron as bs

ESIK = 0.6        # gercek hayalet 0,9-1,0; Loom hover cubugu (CH36, birakilir) ~0,44


def kare(video, t, vf):
    q = subprocess.run([bs.FF, "-nostats", "-v", "error", "-ss", "%.3f" % t, "-i", video, "-frames:v", "1",
                        "-vf", vf + ",format=rgb24", "-f", "rawvideo", "-"], capture_output=True)
    a = np.frombuffer(q.stdout, np.uint8)
    return a[:1920 * 1080 * 3].reshape(1080, 1920, 3).astype(float) if a.size >= 1920 * 1080 * 3 else None


def main():
    edit = sys.argv[1].rstrip("/"); n = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 6
    plan = json.load(open(os.path.join(edit, "balon_plan.json"))); y_ = plan.get("yama")
    if not y_:
        print("yama yok"); return
    edl = json.load(open(os.path.join(edit, "edl.json")))
    ham = edl["sources"]["DERS"]; ham = ham if os.path.isabs(ham) else os.path.join(edit, ham)
    final = os.path.join(edit, sys.argv[sys.argv.index("--video") + 1]) if "--video" in sys.argv else os.path.join(edit, "final.mp4")
    kx, ky, kw, kh = plan["kart"]
    am = np.asarray(Image.open(os.path.join(edit, "yama_maske.png"))).astype(float) / 255
    yy, xx = np.mgrid[0:y_["h"], y_["x"]:y_["x"] + y_["w"]]
    bcx, bcy, bR = plan["x"] + plan["cap"] / 2.0, plan["y"] + plan["cap"] / 2.0, plan["cap"] / 2.0
    bx, by, br = plan["balon_kaynak"]; sc = 1920.0 / kw
    hcx, hcy, hr = (bx - kx) * sc, (by - ky) * sc, br * sc
    gercek = ((xx - hcx) ** 2 + (yy - hcy) ** 2) <= (hr - 3) ** 2      # yalniz gercek hayalet
    halka = gercek & (am > 0.95) & (((xx - bcx) ** 2 + (yy - bcy) ** 2) > (bR + 3) ** 2) & (yy >= y_.get("ust", 0))
    seg, t0 = [], 0.0
    for r in edl["ranges"]:
        d = float(r["end"]) - float(r["start"])
        if r["source"] == "DERS": seg.append((t0, t0 + d, float(r["start"])))
        t0 += d
    kotu, olc = [], []
    for i in range(n):
        t = t0 * (i + 0.5) / n
        s0 = next(((t - a) + h for a, b, h in seg if a + 1.5 <= t <= b - 3.5), None)
        if s0 is None: continue
        s0 += bs.ses_ofset(final, t, ham, s0)
        if any(x0 - 2 <= s0 <= x1 + 2 for x0, x1 in plan.get("balonsuz") or []):
            continue                                      # hoca balonu tasimis, yama yok
        F = kare(final, t, "null"); H = kare(ham, s0, "crop=%d:%d:%d:%d,scale=1920:1080:flags=lanczos" % (kw, kh, kx, ky))
        if F is None or H is None: continue
        f = F[0:y_["h"], y_["x"]:y_["x"] + y_["w"]][halka]; h = H[0:y_["h"], y_["x"]:y_["x"] + y_["w"]][halka]
        oran = float((np.abs(f - h).max(axis=1) < 8).mean())
        olc.append("%.2f" % oran)
        if oran > ESIK: kotu.append(round(t, 1))
    print("hayalet orani: %s (esik %.2f)%s" % (" ".join(olc), ESIK, (" | sorunlu t=%s" % kotu) if kotu else ""))
    sys.exit(1 if kotu else 0)


if __name__ == "__main__":
    main()

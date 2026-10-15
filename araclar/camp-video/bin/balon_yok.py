#!/usr/bin/env python3
"""Hoca Loom balonunu kayit sirasinda tasidi mi? (06.10.2026)

CH18/CH20/CH22: son soru bolumunde balon surukleyip slaytin icine (sag orta) koyulmus.
O araliklarda plan yerlesimi eski balon yerini kirpar: tepede koyu yarim daire.
Olcum: kartin USTUNDEKI seritte (balonun tasan tepesi) parlaklik. Balon oradaysa kamera
goruntusu (acik duvar), degilse tarayici zemini (koyu). 1 sn'de bir ornek.
Cikti: edit/balon_plan.json'a "balonsuz": [[bas, bit], ...] (HAM zaman, 1 sn genisletilmis)
Kullanim: bin/balon_yok.py projects/<proje>
"""
import json, os, subprocess, sys
import numpy as np

FF = os.path.expanduser("~/.local/bin/ffmpeg")


def olc(proje):
    edit = os.path.join(proje, "edit"); pp = os.path.join(edit, "balon_plan.json")
    plan = json.load(open(pp))
    kx, ky, kw, kh = plan["kart"]; bx, by, br = plan["balon_kaynak"]
    y0 = int(max(0, by - br) + 1); y1 = int(ky - 2)
    if y1 - y0 < 2:
        st = os.stat(pp); plan["balonsuz"] = []; json.dump(plan, open(pp, "w"), indent=1)
        os.utime(pp, (st.st_atime, st.st_mtime)); return plan, None
    x0 = int(bx - 0.5 * br); w = int(br)
    q = subprocess.run(["nice", "-n", "10", FF, "-nostats", "-v", "error", "-threads", "2",
                        "-i", os.path.join(proje, "ders.mp4"),
                        "-vf", "fps=1,crop=%d:%d:%d:%d,scale=32:4:flags=area,format=gray" % (w, y1 - y0, x0, y0),
                        "-an", "-f", "rawvideo", "-"], capture_output=True)
    f = np.frombuffer(q.stdout, np.uint8).reshape(-1, 128).astype(float)
    a = f.mean(axis=1); sd = f.std(axis=1)
    # Balon YOK = serit tarayici zemininin kendisi: duz (sapma <4) ve koyu (<60, zemin ~44).
    # Yalniz parlakliga bakmak loş kamerada yanildi (CH28: balon yerinde, duvar koyu gri).
    var = ~((sd < 4) & (a < 60))
    # 2 sn'den kisa bosluklari yok say (kamera kararmasi/kafa), kalanlari 1 sn genislet
    ara, i = [], 0
    while i < len(var):
        if not var[i]:
            j = i
            while j < len(var) and not var[j]: j += 1
            if j - i >= 8:          # gercek tasimalar >=68 sn; kisa = los kamera (CH28 5 sn)
                ara.append([max(0.0, i - 1.0), j + 1.0])
            i = j
        else:
            i += 1
    birlesik = []
    for x in ara:
        if birlesik and x[0] <= birlesik[-1][1]: birlesik[-1][1] = x[1]
        else: birlesik.append(x)
    plan["balonsuz"] = birlesik
    st = os.stat(pp)
    json.dump(plan, open(pp, "w"), indent=1)
    if not birlesik:
        # Balon hep yerinde: plan degismedi sayilir, kuyruk bu dersi yeniden basmasin
        os.utime(pp, (st.st_atime, st.st_mtime))
    return plan, a


if __name__ == "__main__":
    for pr in sys.argv[1:]:
        plan, a = olc(pr.rstrip("/"))
        top = sum(b - a_ for a_, b in plan["balonsuz"])
        print(os.path.basename(pr.rstrip("/"))[10:40], "balonsuz %d aralik, %.0f sn" % (len(plan["balonsuz"]), top),
              plan["balonsuz"][:6], "" if a is None else "parlaklik ortanca %.0f min %.0f" % (np.median(a), a.min()))

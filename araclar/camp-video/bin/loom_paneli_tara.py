#!/usr/bin/env python3
"""Teslim edilen videolarda Loom kayit kontrol panelini (sol kenar) arar.

Panel: koyu yuvarlak kutu (x~0-52, y~218-385) + turuncu stop butonu.
Slaytlar beyaz oldugu icin hem koyuluk hem turuncu birlikte aranir.
"""
import subprocess, sys, os, json, glob
import numpy as np

X, Y, W, H = 0, 205, 60, 195
FPS = 2.0
TESLIM = os.path.expanduser("~/Downloads/CAMPVERSE Dersler/Editli")

def tara(yol):
    p = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", yol,
         "-vf", "crop=%d:%d:%d:%d,fps=%g" % (W, H, X, Y, FPS),
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    n = W * H * 3
    varlik = []
    i = 0
    while True:
        ham = p.stdout.read(n)
        if len(ham) < n:
            break
        a = np.frombuffer(ham, dtype=np.uint8).reshape(H, W, 3).astype(np.int16)
        r, g, b = a[..., 0], a[..., 1], a[..., 2]
        koyu = ((r < 75) & (g < 75) & (b < 80)).sum()
        turuncu = ((r > 190) & (g > 55) & (g < 130) & (b < 90)).sum()
        varlik.append(koyu >= 1500 and turuncu >= 250)
        i += 1
    p.stdout.close(); p.wait()
    # ardisik dogru bloklari araliga cevir
    arali, bas = [], None
    for k, v in enumerate(varlik):
        t = k / FPS
        if v and bas is None:
            bas = t
        elif not v and bas is not None:
            arali.append((round(bas, 2), round(t, 2))); bas = None
    if bas is not None:
        arali.append((round(bas, 2), round(len(varlik) / FPS, 2)))
    # 1 sn'den kisa bosluklari birlestir
    bir = []
    for a in arali:
        if bir and a[0] - bir[-1][1] <= 1.0:
            bir[-1] = (bir[-1][0], a[1])
        else:
            bir.append(a)
    return [a for a in bir if a[1] - a[0] >= 0.5]

if __name__ == "__main__":
    hedef = sys.argv[1:] or sorted(glob.glob(TESLIM + "/*.mp4"))
    cikti = {}
    for f in hedef:
        ad = os.path.basename(f)
        if ad.startswith("00 - "):
            continue
        ar = tara(f)
        top = round(sum(b - a for a, b in ar), 1)
        cikti[ad] = {"araliklar": ar, "toplam_s": top}
        print("%-44s %2d blok  %6.1f sn" % (ad, len(ar), top), flush=True)
    yol = os.path.expanduser("~/camp-video/takip/loom_paneli.json")
    json.dump(cikti, open(yol, "w"), ensure_ascii=False, indent=1)
    print("->", yol)

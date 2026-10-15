#!/usr/bin/env python3
"""Teslim edilen videoda SOL KENAR seridini olcer.

Iki soruyu birden yanitlar:
  1. Loom overlay'i (kayit paneli / cizim araç cubugu) ne kadar goruntude?
  2. Overlay yokken o seritte gercek slayt icerigi var mi? (kapatma guvenli mi)
"""
import subprocess, sys, os, json, glob
import numpy as np

SERIT = 64          # kapatmayi dusundugumuz genislik
BAK   = 90          # bu kadar sutun okunur (serit + saginda tampon)
FPS   = 1.0
TESLIM = os.path.expanduser("~/Downloads/CAMPVERSE Dersler/Editli")

def tara(yol):
    p = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", yol,
         "-vf", "crop=%d:1080:0:0,fps=%g" % (BAK, FPS),
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    n = BAK * 1080 * 3
    overlay, icerik_kare, kare = [], 0, 0
    en_kirli = (0.0, -1)       # overlay yokken en cok icerikli kare
    while True:
        ham = p.stdout.read(n)
        if len(ham) < n:
            break
        a = np.frombuffer(ham, dtype=np.uint8).reshape(1080, BAK, 3).astype(np.int16)
        s = a[:, :SERIT, :]
        r, g, b = s[..., 0], s[..., 1], s[..., 2]
        koyu = ((r < 80) & (g < 80) & (b < 85))
        # overlay: dikey olarak yogun koyu blok (>=90 satirda >=20 koyu piksel)
        satir = (koyu.sum(axis=1) >= 20).sum()
        ov = satir >= 90
        overlay.append(ov)
        if not ov:
            beyaz_disi = (((r > 235) & (g > 235) & (b > 235)).sum())
            oran = 1.0 - beyaz_disi / s[..., 0].size
            if oran > en_kirli[0]:
                en_kirli = (round(float(oran), 4), kare)
            if oran > 0.02:
                icerik_kare += 1
        kare += 1
    p.stdout.close(); p.wait()
    arali, bas = [], None
    for k, v in enumerate(overlay):
        t = k / FPS
        if v and bas is None: bas = t
        elif not v and bas is not None:
            arali.append([round(bas,1), round(t,1)]); bas = None
    if bas is not None: arali.append([round(bas,1), round(kare/FPS,1)])
    bir = []
    for a in arali:
        if bir and a[0]-bir[-1][1] <= 2.0: bir[-1][1] = a[1]
        else: bir.append(a)
    return {"kare": kare, "overlay_s": round(sum(b-a for a,b in bir),1),
            "blok": len(bir), "araliklar": bir,
            "icerikli_kare": icerik_kare, "en_kirli_oran": en_kirli[0],
            "en_kirli_sn": round(en_kirli[1]/FPS,1)}

if __name__ == "__main__":
    hedef = sys.argv[1:] or sorted(glob.glob(TESLIM + "/*.mp4"))
    yol = os.path.expanduser("~/camp-video/takip/sol_serit.json")
    cikti = json.load(open(yol)) if os.path.exists(yol) else {}
    for f in hedef:
        ad = os.path.basename(f)
        if ad.startswith("00 - "): continue
        d = tara(f); cikti[ad] = d
        print("%-42s overlay %6.1f/%4ds (%2d blok) · icerikli kare %3d · en kirli %.3f @%ds"
              % (ad[:42], d["overlay_s"], d["kare"], d["blok"],
                 d["icerikli_kare"], d["en_kirli_oran"], d["en_kirli_sn"]), flush=True)
        json.dump(cikti, open(yol,"w"), ensure_ascii=False, indent=1)

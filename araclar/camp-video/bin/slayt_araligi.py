#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bir slaydin ekranda kaldigi araligi ikili aramayla bulur.

Kullanim: slayt_araligi.py <video> <icindeki_an> [x y w h]
Baslik seridini karsilastirir; ayni slayt mi degil mi ona bakar.
"""
import subprocess, sys, tempfile, os
FFMPEG = os.path.expanduser("~/.local/bin/ffmpeg")


def imza(video, t, kutu):
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "f.pgm")
        subprocess.run([FFMPEG, "-v", "error", "-ss", "%.2f" % max(0, t), "-i", video,
                        "-frames:v", "1", "-vf",
                        "crop=%d:%d:%d:%d,scale=64:8,format=gray" % kutu,
                        "-y", p], check=False)
        if not os.path.exists(p):
            return None
        return open(p, "rb").read()[-512:]


def ayni(a, b, tol=14):
    if a is None or b is None:
        return False
    if len(a) != len(b):
        return False
    fark = sum(1 for x, y in zip(a, b) if abs(x - y) > 24)
    return fark <= tol


def sinir(video, ic, kutu, yon, uzak=180.0):
    ref = imza(video, ic, kutu)
    lo, hi = (ic - uzak, ic) if yon == "bas" else (ic, ic + uzak)
    if yon == "bas":
        if ayni(imza(video, max(0, lo), kutu), ref):
            return max(0.0, lo)
        for _ in range(12):
            orta = (lo + hi) / 2
            if ayni(imza(video, orta, kutu), ref):
                hi = orta
            else:
                lo = orta
        return round(hi, 2)
    else:
        if ayni(imza(video, hi, kutu), ref):
            return hi
        for _ in range(12):
            orta = (lo + hi) / 2
            if ayni(imza(video, orta, kutu), ref):
                lo = orta
            else:
                hi = orta
        return round(lo, 2)


if __name__ == "__main__":
    v, t = sys.argv[1], float(sys.argv[2])
    kutu = tuple(int(x) for x in sys.argv[3:7]) if len(sys.argv) > 6 else (620, 36, 60, 84)
    a = sinir(v, t, kutu, "bas")
    b = sinir(v, t, kutu, "bit")
    print("%.2f  %.2f   (%.1f sn)" % (a, b, b - a))

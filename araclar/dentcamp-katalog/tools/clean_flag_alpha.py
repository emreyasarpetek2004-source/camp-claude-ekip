#!/usr/bin/env python3
"""Bayrak kesimlerinde kalan serbest piksel öbeklerini siler.

rembg / gökyüzü silme bazen bayrağın altında kopuk küçük adacıklar bırakıyor.
Kapakta bunlar bayrağın hemen altında serbest gezen gri lekeler olarak görünüyor.
Alfa kanalındaki bağlı bileşenler taranır; en büyüğü (bayrak + direk) dışında
eşikten küçük olan her şey silinir.

Kullanım:  python3 tools/clean_flag_alpha.py [ulke ...]     (varsayılan: dördü)
"""
import pathlib
import sys
from collections import deque

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
MIN_AREA = 16000       # bu alandan küçük ada = artık (tuval 2x olduğu için 4x alan)
STEP = 2               # tarama adımı (hız); maske tam çözünürlükte uygulanır


def clean(key):
    path = IMG / f"bayrak_{key}.png"
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    a = im.split()[3]
    px = a.load()

    seen = bytearray(w * h)
    removed = 0
    for sy in range(0, h, STEP):
        for sx in range(0, w, STEP):
            if px[sx, sy] < 24 or seen[sy * w + sx]:
                continue
            q = deque([(sx, sy)])
            seen[sy * w + sx] = 1
            pts = []
            while q:
                x, y = q.popleft()
                pts.append((x, y))
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx] \
                            and px[nx, ny] >= 24:
                        seen[ny * w + nx] = 1
                        q.append((nx, ny))
            if len(pts) < MIN_AREA:
                for x, y in pts:
                    px[x, y] = 0
                removed += 1

    if removed:
        im.putalpha(a)
        im.save(path)
    print(f"bayrak_{key}.png  {removed} artık ada silindi")


if __name__ == "__main__":
    for k in (sys.argv[1:] or ["aus", "uk", "usa", "deu"]):
        clean(k)

#!/usr/bin/env python3
"""Toplu katalog kapak fotoğrafı: dört ülkenin tek kadrajda birleştiği kare.

Kullanıcının 2 Eylül 2026'da verdiği kapak görseli (`kapak_toplu_src.png`) dört
ülkenin simgesini ve dört bayrağı tek kadrajda taşıyor; dört panelli eski kart
(`make_cover_toplu.py`) bu yüzden bırakıldı, dosyası duruyor.

Kaynak 1448x1086 px (4:3 = 1,3333). Kart ilk turda 452x252pt idi ve kare
dikeyde kırpılıyordu (90 px üstten). Bayrak şeridi kapaktan kalkınca kart
452x339pt'ye büyütüldü; bu ölçü kaynağın oranı olduğu için artık KIRPIM YOK ve
dört simge de tam görünüyor. `UST` payı kutu oranı değişirse diye duruyor.

    python3 tools/make_cover_toplu_foto.py
"""
import pathlib

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / "assets/img"

ORAN = 452 / 339          # CSS'teki .cover-toplu .cv-photo kutusu
UST = 0                   # yukarıdan atılan piksel (kutu kaynağın oranında: kırpım yok)


def main():
    src = Image.open(IMG / "kapak_toplu_src.png").convert("RGB")
    w, h = src.size
    yeni = round(w / ORAN)
    if yeni > h:
        raise SystemExit(f"kaynak çok basık: {w}x{h}, gereken yükseklik {yeni}")
    ust = max(0, min(h - yeni, UST))
    out = IMG / "kapak_toplu_foto.jpg"
    src.crop((0, ust, w, ust + yeni)).save(out, quality=92, subsampling=1)
    print(f"yazıldı: {out.relative_to(ROOT)}  {w}x{yeni}  ust={ust}  "
          f"({out.stat().st_size / 1e3:.0f} KB)")


if __name__ == "__main__":
    main()

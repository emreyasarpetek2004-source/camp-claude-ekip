#!/usr/bin/env python3
"""Bayrak PNG'sindeki alfa deliklerini kapatır.

Sorun: `place_flag_photo.py --sky` gökyüzünü kenardan yayılarak siliyor. Kaynak
fotoğrafın arka planı açık gri/beyaz olduğunda bu yayılma bayrağın KENDİ beyaz
alanlarına da sızıyor — Union Jack'in beyaz şeritleri saydam kalıyor ve kapakta
arka plan görünüyor.

Çözüm: saydam bölgelerden yalnızca GÖRÜNTÜ KENARINA bağlı olanı arka plan say;
bayrağın içinde kalan saydam adacıkları (delikleri) yeniden opak yap. RGB verisi
zaten korunduğu için renkler olduğu gibi geri gelir.

    python3 tools/alfa_delik_kapat.py assets/img/bayrak_uk.png
"""
import pathlib
import sys

from PIL import Image, ImageDraw

ESIK = 128          # bunun altındaki alfa "saydam" sayılır


def kapat(yol):
    yol = pathlib.Path(yol)
    im = Image.open(yol).convert("RGBA")
    a = im.getchannel("A")
    w, h = im.size

    # saydam = 0, opak = 255
    maske = a.point(lambda v: 255 if v >= ESIK else 0).convert("L")

    # 1 px saydam çerçeve ekle: böylece kenara değen tüm arka plan tek parça olur
    calisma = Image.new("L", (w + 2, h + 2), 0)
    calisma.paste(maske, (1, 1))

    # kenardan yayılarak arka planı işaretle
    ImageDraw.floodfill(calisma, (0, 0), 128, thresh=0)

    # hâlâ 0 kalanlar = bayrağın içindeki delikler
    delik = calisma.crop((1, 1, w + 1, h + 1)).point(lambda v: 255 if v == 0 else 0)
    n = sum(delik.histogram()[255:])
    if not n:
        print(f"{yol.name}: delik yok")
        return

    yeni = a.copy()
    yeni.paste(255, (0, 0), delik)
    im.putalpha(yeni)
    im.save(yol)
    print(f"{yol.name}: {n} piksellik delik kapatıldı")


if __name__ == "__main__":
    for y in sys.argv[1:] or ["assets/img/bayrak_uk.png"]:
        kapat(y)

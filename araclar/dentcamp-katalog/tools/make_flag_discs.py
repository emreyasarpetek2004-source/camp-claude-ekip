#!/usr/bin/env python3
"""Mentör kartının arkasındaki bayrak halkası için kare bayrak kırpımı üretir.

Kaynak: assets/flag_src/<key>.png  (Wikimedia resmî düz bayraklar, 2400 px)
Hedef : assets/img/fdisc_<key>.png (512x512)

Daireye çevirmeyi CSS yapıyor (.mflag üzerinde border-radius:50%), bu yüzden
burada alfa maskesi yok; yalnız kare kırpım.

KIRPIM NEDEN ÜLKEYE GÖRE DEĞİŞİYOR:
Dairenin ortasını portre kapatıyor. Portre 86,6pt, disk 112pt; yani okuyucunun
gördüğü tek şey yarıçapın DIŞ %19'u. Bayrağın ayırt edici ögesi bu halkanın içine
düşmezse bayrak tanınmıyor.

  deu — yatay üç bant, her yerde okunur: tam boy kare, ortadan.
  uk  — simetrik Union Jack: tam boy kare, ortadan.
  usa — canton sol üstte: tam boy kare, sola dayalı. Halkada üstte yıldızlar,
        altta şeritler görünüyor.
  aus — TAM BOY KARE ÇALIŞMIYOR. Avustralya bayrağının UK'den tek farkı
        Commonwealth Yıldızı ve Güney Çaprazı; tam boy karede yıldız merkezden
        yarıçapın %60'ında kalıyor, yani portrenin altında gizleniyor ve halkada
        yalnız Union Jack görünüyor. Sonuç: kart UK kartıyla birebir aynı duruyor
        (dört katalogda Anita ve Damla aynı satırda yan yana). Bu yüzden aus'ta
        kırpım daraltıldı ve merkez, Union Jack merkezi ile Commonwealth Yıldızı'nı
        merkezden EŞİT uzaklığa (yarıçapın %90'ı) getirecek noktaya kaydırıldı:
        biri halkanın üst, diğeri alt yanında görünüyor.
"""
import pathlib

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "flag_src"
IMG = ROOT / "assets" / "img"

N = 512
KART = (448, 560)            # mentör kartı 4:5

# (cx, cy, yan): kırpım karesinin merkezi ve kenarı.
# cx bayrak GENİŞLİĞİNE, cy ve yan bayrak YÜKSEKLİĞİNE göre normalize.
KIRPIM = {
    "deu": (0.500, 0.5, 1.000),
    "uk":  (0.500, 0.5, 1.000),
    "usa": (0.263, 0.5, 1.000),   # sola dayalı: canton halkada kalsın
    "aus": (0.208, 0.5, 0.585),   # Union Jack + Commonwealth Yıldızı halkada
}


# Mentör kartının zemini: 4:5 dikey kırpım. Kare kırpımı 4:5'e ölçeklemek bayrağı
# dikeyde %25 geriyor (ABD yıldızları belirgin biçimde bozuluyor), o yüzden ayrı
# varlık üretiliyor. 2:1 bayraktan yalnız %40 genişlik alındığı için kırpım konumu
# ülkeye göre ayarlanıyor:
#   usa 0.0 -> canton (yıldızlar) kadrajda kalsın, sağ kenarda şeritler görünür.
#   aus 0.5 -> sola dayalı kırpım denendi: kartta yalnız Union Jack parçaları
#              kalıyor ve İngiltere kartından ayırt edilemiyor. Ortadan kırpımda
#              solda Union Jack, sağda Commonwealth Yıldızı ve Güney Çaprazı
#              görünüyor; ikisi net ayrışıyor.
#   deu/uk simetrik, ortadan.
KART_SOL = {"deu": 0.5, "uk": 0.5, "usa": 0.0, "aus": 0.5}


def kartlar():
    for key, fx in KART_SOL.items():
        im = Image.open(SRC / f"{key}.png").convert("RGB")
        gen = im.height * KART[0] / KART[1]
        x = (im.width - gen) * fx
        box = (round(x), 0, round(x + gen), im.height)
        out = IMG / f"fkart_{key}.png"
        im.crop(box).resize(KART, Image.LANCZOS).save(out, optimize=True)
        print(f"{out.name:16s} kırpım {box}  {out.stat().st_size / 1024:.0f} KB")


def main():
    kartlar()
    for key, (cx, cy, yan) in KIRPIM.items():
        im = Image.open(SRC / f"{key}.png").convert("RGB")
        s = yan * im.height
        x, y = cx * im.width - s / 2, cy * im.height - s / 2
        x = min(max(x, 0), im.width - s)
        y = min(max(y, 0), im.height - s)
        box = (round(x), round(y), round(x + s), round(y + s))
        kare = im.crop(box).resize((N, N), Image.LANCZOS)
        out = IMG / f"fdisc_{key}.png"
        kare.save(out, optimize=True)
        print(f"{out.name:16s} <- {key}.png {im.width}x{im.height}"
              f"  kırpım {box}  {out.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()

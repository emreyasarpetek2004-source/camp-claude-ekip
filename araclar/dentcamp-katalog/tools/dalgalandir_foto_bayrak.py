#!/usr/bin/env python3
"""Direğe asılı DÜZ bayrak fotoğrafını dalgalandırır.

Girdi : assets/bayrak_kaynak/<key>_direkli_foto.png   (bozulmamış kaynak)
Çıktı : assets/img/bayrak_<key>.png

Neden: kapaktaki dört bayrak fotoğrafik. Üçü gerçekten dalgalanan karelerdi ama
İngiltere'ninki direğe asılı, hiç dalgalanmayan, dümdüz bir kareydi; kapakta
bayrak değil pano gibi duruyordu (kullanıcı, 25 Ağustos 2026). Union Jack'in dış
kenarı beyaz olduğu için beyaza yakın kapak zemininde silüeti de kaybediyordu.

Neden vektörden yeniden üretmedik: tools/make_wave_flags.py resmî SVG'den
kusursuz bir dalgalı bayrak üretiyor ama sonuç düz vektör görünümünde. Diğer üç
kapak fotoğrafik olduğu için tek başına ayrık duruyordu. Bu araç fotoğrafın
kendi dokusunu ve direğini koruyup yalnız BEZİ deforme ediyor.

Model make_wave_flags.wave() ile aynı: hoist tarafında genlik sıfır, fly ucuna
doğru büyüyen zarf; dalganın eğimine göre ışık/gölge. Fark, düz bir SVG yerine
fotoğrafın üzerinde çalışması ve direği yerinde bırakması.

    python3 tools/dalgalandir_foto_bayrak.py uk
"""
import math
import pathlib
import sys

import numpy as np
from PIL import Image, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "bayrak_kaynak"
OUT = ROOT / "assets" / "img"

AMP = 0.085          # bez yüksekliğine oranla tepe genliği
WAVES = 1.35         # bez boyunca kaç dalga
PHASE = 0.60         # dalganın başlangıç fazı
TILT = -0.045        # fly ucuna doğru düşüş (yerçekimi)
SHADE = 0.20         # gölge/ışık şiddeti (fotoğrafta zaten ışık var, düşük tutuluyor)

# Zemin gölgesi: bayrağın silüetini beyaz kapaktan ayırır. Yalnız Union Jack'e
# gerekiyor, çünkü dış kenarı beyaz ve kapak zemini #fcfcfc: gölgesiz basıldığında
# bayrağın nerede bittiği görünmüyor, pano gibi duruyor. Almanya (siyah/altın),
# ABD (kırmızı şerit) ve Avustralya (lacivert) kenarlarıyla zaten ayrışıyor.
# CSS filter yerine PNG'ye gömülüyor: Chrome, filtreli ögeyi baskıya rasterize
# ediyor ve bayrak ekran çözünürlüğüne düşüyor.
GOLGE = dict(dy=9, bulanik=15, siyahlik=0.30)
DIREK_PAY = 1.35     # direk genişliği tespitinde bezin ortalama yüksekliğine oran


def bez_baslangici(alfa):
    """Direğin bittiği, bezin başladığı sütun.

    Direk bezden UZUN: sütun bazlı opak yükseklik direk bölgesinde bezin
    ortalamasının belirgin üstünde. İlk kez bu eşiğin altına düşen sütun bezin
    başlangıcıdır. Sabit bir piksel değeri yazmak yerine ölçmek gerekiyor, çünkü
    aynı araç başka bayrağa da uygulanabilsin.
    """
    yuk = (alfa > 128).sum(axis=0)
    dolu = yuk[yuk > 0]
    esik = np.median(dolu) * DIREK_PAY
    for x in range(len(yuk)):
        if 0 < yuk[x] < esik:
            return x
    return 0


def dalgalandir(im):
    a = np.asarray(im)
    alfa = a[:, :, 3]
    x0, x1 = np.nonzero(alfa.any(axis=0))[0][[0, -1]]
    bez_x = bez_baslangici(alfa)
    sut = (alfa > 128).sum(axis=0)
    bez_h = int(np.median(sut[bez_x:x1 + 1][sut[bez_x:x1 + 1] > 0]))

    cikti = a.copy()
    cikti[:, bez_x:x1 + 1] = 0
    A = AMP * bez_h
    for x in range(bez_x, x1 + 1):
        t = (x - bez_x) / max(1, x1 - bez_x)
        env = t ** 1.25                        # hoist'ta 0, fly ucunda 1
        u = 2 * math.pi * (WAVES * t + PHASE)
        dy = int(round(A * env * math.sin(u) + TILT * bez_h * t))
        f = 1.0 + SHADE * math.cos(u) * env    # yükselen yüz aydınlık
        f *= 1.0 - 0.08 * (1.0 - env)          # hoist'ta bezin kalınlığı hissi
        sutun = a[:, x].astype(np.float32)
        sutun[:, :3] = np.clip(sutun[:, :3] * f, 0, 255)
        if dy >= 0:
            cikti[dy:, x] = sutun[:len(sutun) - dy]
        else:
            cikti[:dy, x] = sutun[-dy:]
    out = Image.fromarray(cikti)
    # Tamsayı kaydırma kenarda 1px merdiven bırakıyor; yalnız alfa yumuşatılıyor.
    out.putalpha(out.getchannel("A").filter(ImageFilter.GaussianBlur(0.8)))
    return golge_bas(out)


def golge_bas(im):
    """Silüetin arkasına yumuşak zemin gölgesi bindirir."""
    a = im.getchannel("A").filter(ImageFilter.GaussianBlur(GOLGE["bulanik"]))
    a = a.point(lambda v: round(v * GOLGE["siyahlik"]))
    golge = Image.new("RGBA", im.size, (0, 0, 0, 0))
    golge.putalpha(a)
    tuval = Image.new("RGBA", im.size, (0, 0, 0, 0))
    tuval.alpha_composite(golge, (0, GOLGE["dy"]))
    tuval.alpha_composite(im)
    return tuval


def main(keys):
    for key in keys:
        src = SRC / f"{key}_direkli_foto.png"
        if not src.exists():
            sys.exit(f"HATA: {src} yok")
        out = dalgalandir(Image.open(src).convert("RGBA"))
        dst = OUT / f"bayrak_{key}.png"
        out.save(dst)
        print(f"{key}: {out.size}  {dst.relative_to(ROOT)}  "
              f"{dst.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main(sys.argv[1:] or ["uk"])

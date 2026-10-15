#!/usr/bin/env python3
"""Mentör portresinin ülke işareti: iki biçimde rozet üretir.

Kaynak: assets/flag_src/<key>.png  (Wikimedia resmî düz bayraklar, 2400 px)
Hedef : assets/img/fdisc_<key>.png  (256x256, daire rozet için kare kırpım)
        assets/img/fchip_<key>.png  (288x216, 4:3 kutuda TAM bayrak)
        assets/img/fwave_<key>.png  (dalgalı gönderli bayrak, alfa sınırına kırpık)

Rozet 12 portrede de aynı dosyadan geliyor, karta gömülmüyor: yeri ve ölçüsü
CSS'ten ayarlanabiliyor ve dosya sayısı 12 yerine 4'te kalıyor.

DAİRE ROZET KIRPIMI ülkeye göre değişir. Bayraklar 5:3 ile 2:1 arasında; kare
kırpım fly ucunu kesiyor ve kesilen yer bayrağın ayırt edici ögesi olabiliyor:

  deu — yatay üç bant, nereden kırpılsa okunur: ortadan.
  uk  — simetrik Union Jack: ortadan.
  usa — canton sol üstte: sola kaydırıldı, yıldızlar rozette kalsın.
  tur — ay-yıldız bayrağın sol yarısında; kırpım 0,415'e kaydırıldı ki hilal
        de yıldız da rozetin içinde kalsın, hilalin ucu kenara dayanmasın.
  aus — ORTADAN KIRPILAMAZ. Avustralya bayrağının UK'den farkı Commonwealth
        Yıldızı ile Güney Haçı; ortadan kare kırpımda Union Jack'in yalnız bir
        parçası ve birkaç yıldız kalıyor, rozet UK rozetiyle karışıyor (Anita
        ile Damla dört katalogda da yan yana basılıyor). Kırpım sola kaydırıldı:
        Union Jack ile Commonwealth Yıldızı birlikte görünüyor.

ÇİP biçiminde kırpım yok: bayrak 4:3 kutuya olduğu gibi oturuyor, yanlarda beyaz
pay kalıyor. Kırpım riski yok ama kutunun kendisi bayrak değil, "etiket" gibi
duruyor. İki biçim de üretiliyor; hangisinin basılacağına tasarım denetimi karar
veriyor.
"""
import pathlib

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "flag_src"
IMG = ROOT / "assets" / "img"

DISC = 256
CHIP = (288, 216)            # 4:3
PAY = 0.06                   # çipte bayrağın çevresindeki beyaz pay

# Daire rozet kırpımının merkezi: bayrak GENİŞLİĞİNE normalize (kenar = yükseklik).
MERKEZ = {"deu": 0.50, "uk": 0.50, "usa": 0.32, "aus": 0.30, "tur": 0.415}


def disc(key):
    im = Image.open(SRC / f"{key}.png").convert("RGB")
    yan = im.height
    x = round(MERKEZ[key] * im.width - yan / 2)
    x = max(0, min(x, im.width - yan))
    return im.crop((x, 0, x + yan, yan)).resize((DISC, DISC), Image.LANCZOS)


def chip(key):
    im = Image.open(SRC / f"{key}.png").convert("RGB")
    kutu = Image.new("RGB", CHIP, (255, 255, 255))
    gen = round(CHIP[0] * (1 - 2 * PAY))
    yuk = round(gen * im.height / im.width)
    if yuk > CHIP[1] * (1 - 2 * PAY):
        yuk = round(CHIP[1] * (1 - 2 * PAY))
        gen = round(yuk * im.width / im.height)
    kutu.paste(im.resize((gen, yuk), Image.LANCZOS),
               ((CHIP[0] - gen) // 2, (CHIP[1] - yuk) // 2))
    return kutu


def wave(key):
    """Kapak ve sayfa köşelerindeki dalgalı bayrağın rozet ölçüsüne kırpılmışı.

    Kaynak bayrak_<key>.png devasa bir şeffaf tuval içinde duruyor (bayrak
    tuvalin yalnız dörtte biri); doğrudan kullanıldığında CSS'teki genişlik
    tuvale uygulanıyor ve bayrak görünmez kalıyor, çerçeve de boş kutu çiziyor.
    Alfa sınırına kırpmak şart.
    """
    im = Image.open(IMG / f"bayrak_{key}.png").convert("RGBA")
    im = im.crop(im.split()[3].getbbox())
    # Dört bayrağın dalgalı render'ı farklı oranda (deu 0,95:1, uk 1,58:1).
    # CSS tek ölçü verdiği için hepsi aynı KARE kutuya, sol üste yaslı
    # oturtuluyor; yoksa ya bayraklar eziliyor ya da her portrede başka boyda.
    im.thumbnail((DISC, DISC), Image.LANCZOS)
    kutu = Image.new("RGBA", (DISC, DISC), (0, 0, 0, 0))
    kutu.paste(im, (0, 0))
    return kutu


def main():
    for key in MERKEZ:
        uret = [("fdisc", disc(key)), ("fchip", chip(key))]
        # Dalgalı bayrak yalnız kapak/köşe dekoru olan dört ülke için var; rozet
        # varyantı olarak da yalnız onlarda üretilebiliyor.
        if (IMG / f"bayrak_{key}.png").exists():
            uret.append(("fwave", wave(key)))
        for ad, im in uret:
            out = IMG / f"{ad}_{key}.png"
            im.save(out, optimize=True)
            print(f"{out.name:20s} {im.size[0]}x{im.size[1]}  "
                  f"{out.stat().st_size / 1024:4.0f} KB")


if __name__ == "__main__":
    main()

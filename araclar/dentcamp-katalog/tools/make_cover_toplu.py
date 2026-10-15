#!/usr/bin/env python3
"""Toplu katalog kapak fotoğrafı: dört ülke karesi tek kartta.

Ülke kataloglarında kapak kartında o ülkenin tek fotoğrafı var. Toplu katalog
dört ülkeyi birden anlattığı için kart dört dikey panele bölünüyor; tek bir
ülkenin fotoğrafını seçmek belgeyi o ülkeye yanlış biçimde meylettiriyordu.

Panel sırası kapaktaki bayrak şeridiyle ve gövdedeki ülke sırasıyla aynı:
Almanya, Avustralya, İngiltere, ABD.

Kart CSS'te 452x252pt; burada 300 dpi karşılığı (1883x1050 px) üretiliyor.

    python3 tools/make_cover_toplu.py
"""
import pathlib

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / "assets/img"

SIRA = ["deu", "aus", "uk", "usa"]

# Panelin kaynağın hangi noktasını göstereceği (genişliğin oranı olarak).
# ORTADAN kırpmak DENENDİ VE BIRAKILDI: dört kapak fotoğrafı da aynı kliniği,
# aynı üniteyi ve aynı iki hekimi gösteriyor; ortadan kırpınca dört panel tek
# fotoğrafın dört kopyası gibi duruyordu. Ülkeyi ayırt ettiren tek şey camdaki
# manzara, o da kadrajın SOLUNDA: Berlin kulesi ve Brandenburg Kapısı, Opera
# Binası ve Harbour Bridge, Westminster ve Big Ben, Empire State.
ODAK = {"deu": 0.20, "aus": 0.25, "uk": 0.28, "usa": 0.20}

# Panel yüksekliği kaynağın tamamı olunca alt üçte bir zemin ve pencere denizliği
# kalıyor: manzara küçülüyor. ZOOM kadrajı büyütür, DIKEY manzarayı kadrajın
# neresine oturtacağını söyler (0 = üst kenar).
ZOOM = 1.3
DIKEY = 0.34
W, H = 1883, 1050          # 452x252pt @ ~300 dpi
ARA = 8                    # paneller arası beyaz fuga (px) ≈ 1,9pt


def main():
    n = len(SIRA)
    pw = (W - ARA * (n - 1)) // n
    tuval = Image.new("RGB", (W, H), (252, 252, 252))
    x = 0
    for key in SIRA:
        src = Image.open(IMG / f"kapak_{key}.jpg").convert("RGB")
        # Panel dikey; kaynak yatay. Yüksekliğe göre ölçekleyip ORTADAN kırp:
        # kapak fotoğraflarının konusu (şehir silüeti / bina) ortada duruyor.
        o = max(pw / src.width, H / src.height) * ZOOM
        im = src.resize((round(src.width * o), round(src.height * o)), Image.LANCZOS)
        sol = max(0, min(im.width - pw, round(im.width * ODAK[key] - pw / 2)))
        ust = max(0, min(im.height - H, round((im.height - H) * DIKEY)))
        tuval.paste(im.crop((sol, ust, sol + pw, ust + H)), (x, 0))
        x += pw + ARA
    out = IMG / "kapak_toplu.jpg"
    tuval.save(out, quality=92, subsampling=1)
    print(f"yazıldı: {out.relative_to(ROOT)}  {tuval.size}  "
          f"panel {pw}px  ({out.stat().st_size / 1e3:.0f} KB)")


if __name__ == "__main__":
    main()

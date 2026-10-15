#!/usr/bin/env python3
"""Toplu katalog kapağı: dört bayrağı tek şeritte birleştirir.

Ülke kataloglarında kapakta TEK bayrak var ve `tools/place_flag_photo.py` onu
sayfanın sol üst köşesine oturtuyor. Toplu katalog dört ülkeyi birden anlattığı
için kapakta dördü birden duruyor: sayfanın üst bandında, soldan hafifçe taşan,
hafif kaydırılmış bir dizi.

Kaynak, ülke kataloglarının HAZIR kesimleri (`assets/img/bayrak_*.png`). Yeniden
kesim yapılmıyor: o dosyalar zaten arka planı silinmiş, alfa artıkları temizlenmiş
hâlde. Burada yalnız kırpma, ölçekleme ve yerleştirme var.

Çıktı: assets/img/bayrak_toplu.png (2240x840 px = 560x210pt, 4 px/pt)

    python3 tools/make_flags_toplu.py
"""
import pathlib

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / "assets/img"

# Tuval, kapaktaki .cv-flags kutusuyla aynı oranda: 560x210pt, 4 px/pt.
CW, CH = 2240, 840

# Sıra, gövdedeki ülke sırasıyla aynı: Almanya, Avustralya, İngiltere, ABD.
# Almanya ve Avustralya dikey dalgalı (uzun), İngiltere ve ABD yatay (kısa);
# bu sıra şeride soldan sağa alçalan doğal bir hat veriyor.
SIRA = ["deu", "aus", "uk", "usa"]

GEN = 560          # her bayrağın hedef genişliği (px)
BINDIRME = 58      # komşu bayraklar arası bindirme (px) — şerit tek parça dursun
UST = {"deu": 8, "aus": 46, "uk": 96, "usa": 74}   # tepe hizası (px)


def main():
    tuval = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    x = 0
    for key in SIRA:
        src = Image.open(IMG / f"bayrak_{key}.png").convert("RGBA")
        kutu = src.getbbox()
        if kutu is None:
            raise SystemExit(f"bayrak_{key}.png boş")
        im = src.crop(kutu)
        h = round(im.height * GEN / im.width)
        im = im.resize((GEN, h), Image.LANCZOS)
        tuval.alpha_composite(im, (x, UST[key]))
        alt = UST[key] + h
        if alt > CH:
            raise SystemExit(f"{key} tuvali aşıyor: {alt} > {CH}")
        x += GEN - BINDIRME
    # Tuvalin boş kenarları atılır: kapaktaki kutu görüntünün TAM ölçüsü olmalı,
    # yoksa CSS'te verilen genişlik/yükseklik bayrakları değil boşluğu ölçekler.
    tuval = tuval.crop(tuval.getbbox())
    out = IMG / "bayrak_toplu.png"
    tuval.save(out)
    w, h = tuval.size
    print(f"yazıldı: {out.relative_to(ROOT)}  {w}x{h}px  "
          f"= {w / 4:g}x{h / 4:g}pt  (build.py .cv-flags ölçüsü bu olmalı)")


if __name__ == "__main__":
    main()

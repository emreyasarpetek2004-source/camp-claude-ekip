#!/usr/bin/env python3
"""AUSCAMP kataloğundan devralınan varlıkları DENTCAMP paletine çevirir.

- logo.png          <- ~/Downloads/DENTCAMP/dentcamp.png (kırpılıp normalize edilir)
- yol_kesikli.png   <- AUSCAMP'in yeşil kesikli yolu, turkuaza boyanır
- icon_instagram/whatsapp.png <- AUSCAMP'ten aynen (marka ikonları, renk değişmez)
"""
import colorsys
import pathlib

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
AUS = pathlib.Path.home() / "auscamp-specialist-katalog" / "assets" / "img"
SRC_LOGO = pathlib.Path.home() / "Downloads" / "DENTCAMP" / "dentcamp.png"

TEAL = (43, 191, 168)      # theme.PATH


def logo():
    im = Image.open(SRC_LOGO).convert("RGBA")
    bbox = im.split()[3].getbbox()          # gerçek mürekkep sınırı (alfa kanalından)
    im = im.crop(bbox)
    im.save(IMG / "logo.png")
    print(f"logo.png  {im.size}  oran {im.size[0] / im.size[1]:.3f}")


def path():
    """Yeşil kesikli yol -> turkuaz. Alfa korunur, yalnız RGB değiştirilir."""
    im = Image.open(AUS / "alpha_p8_481_890x1517.png").convert("RGBA")
    r, g, b, a = im.split()
    solid = Image.new("RGB", im.size, TEAL)
    out = Image.merge("RGBA", (*solid.split(), a))
    out.save(IMG / "yol_kesikli.png")
    print(f"yol_kesikli.png  {out.size}")


def icons():
    """Instagram/WhatsApp marka ikonları renk değişmeden geçer."""
    for src, dst in [("alpha_p8_431_60x60.png", "icon_instagram.png"),
                     ("alpha_p8_433_99x99.png", "icon_whatsapp.png")]:
        Image.open(AUS / src).convert("RGBA").save(IMG / dst)
        print(f"{dst}")


TEAL_HUE = 174 / 360        # #005b52 ve #00d9bd ile aynı hue


def roadmap_icons():
    """Road map ikonları AUSCAMP'te iki yeşil tonundaydı (koyu figürler ~150°,
    açık tikler ~90°). Hue'yu turkuaza sabitleyip doygunluk/parlaklığı koruyoruz —
    böylece açık/koyu ayrımı bozulmadan ikonlar DENTCAMP paletine geçiyor."""
    for f in ["icon_belge_kalkan.png", "icon_chat_check.png", "icon_ikili_kisi.png",
              "icon_takvim_kisi.png", "icon_lisans_karti.png"]:
        im = Image.open(AUS / f).convert("RGBA")
        px = list(im.getdata())
        out = []
        for r, g, b, a in px:
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if a > 8 and s > 0.15 and 60 / 360 <= h <= 200 / 360:
                nr, ng, nb = colorsys.hsv_to_rgb(TEAL_HUE, s, v)
                out.append((round(nr * 255), round(ng * 255), round(nb * 255), a))
            else:
                out.append((r, g, b, a))
        im.putdata(out)
        im.save(IMG / f)
        print(f"{f}  (yeşil -> turkuaz)")


if __name__ == "__main__":
    logo()
    path()
    icons()
    roadmap_icons()

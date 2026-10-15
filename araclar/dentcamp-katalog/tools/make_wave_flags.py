#!/usr/bin/env python3
"""Kapak bayraklarını SIFIRDAN üretir — dalgalanan, tam, filigransız.

Neden: eski bayraklar stok fotoğraftı ve dört ayrı kusuru vardı —
  · İngiltere: bayrağın tamamına döşenmiş "Unsplash+" filigranı (lisans sorunu),
  · Almanya:  fly ucu kırpma sırasında düz çizgiyle kesilmiş,
  · ABD:      gökyüzü silinirken direk ve halatlar beyaz çizgi olarak kalmış,
  · Avustralya: 29 KB'lık kaynaktan geldiği için yumuşak + gökyüzü halesi.

Çözüm: bayraklar Wikimedia'daki KAMUYA AÇIK resmî SVG'lerden yüksek çözünürlükte
düzleme basılır, sonra burada dalga ve ışık verilir. Sonuç lisanssız, istenen her
çözünürlükte keskin ve bayrak her zaman EKSİKSİZ.

    python3 tools/make_wave_flags.py            # dördünü de üret
    python3 tools/make_wave_flags.py deu        # tek ülke

Girdi : assets/flag_src/<key>.png   (düz bayrak, yüksek çözünürlük)
Çıktı : assets/img/bayrak_<key>.png (alfa kanallı, dalgalı)
"""
import math
import pathlib
import sys

from PIL import Image, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "flag_src"
OUT = ROOT / "assets" / "img"

# Çıktı tuvali. Kapakta 260x130pt civarında basılacağı için 2000px genişlik
# ~550 dpi verir; küçültme her zaman büyütmeden iyidir.
TARGET_W = 2000

# Dalga: hoist (direk) tarafında genlik sıfır, fly ucuna doğru büyür — bez
# gerçekte de böyle davranır.
AMP = 0.052          # tuval yüksekliğine oranla tepe genliği
WAVES = 1.45         # bayrak boyunca kaç dalga
PHASE = 0.55         # dalganın başlangıç fazı (kadrajı güzelleştirir)
TILT = -0.030        # fly ucuna doğru hafif düşüş (yerçekimi)
SHADE = 0.30         # gölge/ışık şiddeti
PAD = 0.16           # dalga taşması için üst-alt boşluk payı


def wave(im, amp=AMP, waves=WAVES, phase=PHASE, tilt=TILT, shade=SHADE):
    """Düz bayrağı dalgalandırır ve dalgaya göre ışıklandırır."""
    im = im.convert("RGB")
    w, h = im.size
    pad = int(h * PAD)
    H = h + 2 * pad
    out = Image.new("RGBA", (w, H), (0, 0, 0, 0))
    src = im.load()
    dst = out.load()

    A = amp * h
    for x in range(w):
        t = x / (w - 1)
        # hoist'ta 0, fly ucunda 1'e yaklaşan zarf
        env = t ** 1.25
        u = 2 * math.pi * (waves * t + phase)
        dy = A * env * math.sin(u) + tilt * h * t
        # Işık: dalganın eğimi. Yükselen yüz aydınlık, inen yüz gölgeli.
        slope = math.cos(u) * env
        f = 1.0 + shade * slope
        # kenarlarda bezin kalınlığı hissi
        f *= 1.0 - 0.10 * (1.0 - env)
        off = int(round(dy)) + pad
        for y in range(h):
            r, g, b = src[x, y]
            yy = y + off
            if 0 <= yy < H:
                dst[x, yy] = (min(255, int(r * f)), min(255, int(g * f)),
                              min(255, int(b * f)), 255)
    # Dalga kaydırması tam sayı olduğu için kenarlarda 1px merdiven kalıyor;
    # yalnız alfa kanalını yumuşatıp gideriyoruz (renkler keskin kalsın).
    a = out.getchannel("A").filter(ImageFilter.GaussianBlur(0.7))
    out.putalpha(a)
    return out


def build(key):
    src = SRC / f"{key}.png"
    if not src.exists():
        sys.exit(f"HATA: {src} yok. Önce tools/fetch_flag_svg.sh çalıştırın.")
    im = Image.open(src)
    # hedef genişliğe ölçekle
    h = round(im.height * TARGET_W / im.width)
    im = im.resize((TARGET_W, h), Image.LANCZOS)
    out = wave(im)
    dst = OUT / f"bayrak_{key}.png"
    out.save(dst)
    print(f"{key}: {im.size} -> {out.size}  {dst.relative_to(ROOT)}")


if __name__ == "__main__":
    keys = sys.argv[1:] or ["deu", "aus", "uk", "usa"]
    OUT.mkdir(parents=True, exist_ok=True)
    for k in keys:
        build(k)

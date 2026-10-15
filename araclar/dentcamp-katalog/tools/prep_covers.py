#!/usr/bin/env python3
"""Kapak fotoğraflarını kart oranına (452x252pt = 1.7937) kırpar.

AUS için ülkeye özel görsel var (Sydney manzaralı diş kliniği). UK / USA / DEU için
şimdilik ülke ipucu taşımayan genel klinik fotoğrafları GEÇİCİ olarak kullanılıyor;
Kullanıcının Gemini ile üreteceği görseller gelince SOURCES sözlüğü güncellenip
bu script tekrar çalıştırılır.
"""
import pathlib

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
WEB = pathlib.Path.home() / "auscamp-web-migration"

RATIO = 452 / 252          # kapak kartı oranı (build.py .cv-photo ile aynı)
OUT_W = 2000               # 452pt kartta ~318 dpi (eskiden 1808 = 288 dpi)

# Kullanıcının ürettiği görseller buraya konur: kapak_kaynak/<ulke>.jpg (veya .png).
# Varsa aşağıdaki geçici kaynağın yerine otomatik olarak o kullanılır.
DROP = ROOT / "assets" / "kapak_kaynak"

# ülke -> (yedek kaynak, yatay kırpma odağı 0..1, ülkeye özel mi)
SOURCES = {
    "aus": (WEB / "ai_foto" / "dis-orj.jpg",     0.50, True),
    "uk":  (WEB / "stok_foto" / "dis-hero.jpg",  0.45, False),
    "usa": (WEB / "stok_foto" / "dis-b2.jpg",    0.55, False),
    "deu": (WEB / "stok_foto" / "dis-hero.jpg",  0.95, False),  # sağ taraf: çalışma alanı
}


def dropped(key):
    """kapak_kaynak/ altında o ülke için bir görsel var mı?"""
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        p = DROP / f"{key}{ext}"
        if p.exists():
            return p
    return None


def crop(src, focus):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    if w / h > RATIO:                       # çok geniş -> yanlardan kırp
        nw = int(round(h * RATIO))
        x = int(round((w - nw) * focus))
        im = im.crop((x, 0, x + nw, h))
    else:                                   # çok yüksek -> üstten/alttan kırp
        nh = int(round(w / RATIO))
        y = int(round((h - nh) * 0.35))     # yüzler üst yarıda kalsın
        im = im.crop((0, y, w, y + nh))
    return im.resize((OUT_W, int(round(OUT_W / RATIO))), Image.LANCZOS)


if __name__ == "__main__":
    DROP.mkdir(parents=True, exist_ok=True)
    for key, (fallback, focus, own) in SOURCES.items():
        new = dropped(key)
        src = new or fallback
        if not src.exists():
            print(f"ATLANDI {key}: kaynak yok -> {src}")
            continue
        # yeni bırakılan görsel zaten doğru kadrajda üretildiği için ortadan kırpılır
        crop(src, 0.5 if new else focus).save(IMG / f"kapak_{key}.jpg",
                                              quality=92, subsampling=0)
        tag = ("" if (new or own) else "  [GEÇİCİ — ülkeye özel görsel bekliyor]")
        print(f"kapak_{key}.jpg  <- {src.name}{tag}")

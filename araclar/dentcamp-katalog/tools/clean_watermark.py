#!/usr/bin/env python3
"""Gemini'nin sağ alt köşeye bastığı parıltı filigranını temizler.

İki aşama:

1. TESPİT — görüntü 8x küçültülüp medyan bulanığı alınır (tam çözünürlükte ~120px'lik
   pencereye denk gelir, ama hesabı ucuz). Filigran çevresinden açık olduğu için bu
   farkta bütünüyle ortaya çıkar. Ardından bağlı bileşenler ayrıştırılıp yalnız
   filigran ölçüsünde ve kabaca kare olan blob tutulur — böylece cam kenarı, kapı
   pervazı gibi gerçek detaylar maskeye girmez.

2. DOLDURMA — maskelenen bölge difüzyonla doldurulur: görüntü tekrar tekrar
   bulanıklaştırılıp maske dışındaki gerçek pikseller her turda geri yazılır. Delik,
   kenarındaki renkten içeri doğru yayılarak kapanır. Medyanla doldurmanın aksine
   filigranın dolu göbeği de tamamen gider.

Kullanım:
  python3 tools/clean_watermark.py girdi.png cikti.jpg
  python3 tools/clean_watermark.py girdi.png cikti.jpg --debug   # maskeyi de yazar
"""
import sys
from collections import deque

from PIL import Image, ImageChops, ImageFilter

# Gemini rozeti sağ alt köşede sabit bir orana oturuyor; dar bir pencerede aranır,
# yoksa arka plandaki cam/pervaz gibi parlak alanlar maskeye giriyor.
BADGE = (0.913, 0.845)             # rozet merkezinin görüntüye oranı
WINDOW = 0.12                      # merkez etrafında aranan yarıçap (genişliğe oran)
SCALE = 8                          # tespit için küçültme
MED = 15                           # küçültülmüş görüntüde medyan penceresi
THRESH = 18                        # medyandan bu kadar açık pikseller aday
MIN_AREA, MAX_AREA = 400, 60000    # filigran blob'unun kabul edilen alan aralığı
ASPECT = (0.55, 1.8)               # kabaca kare olmalı
GROW = 8                          # maskeyi genişletme
FEATHER = 5.0                     # maske yumuşatma


def largest_blob(mask):
    """Maskedeki bağlı bileşenlerden filigran ölçüsüne uyan en büyüğünü döndürür."""
    w, h = mask.size
    px = mask.load()
    seen = bytearray(w * h)
    best = None
    for sy in range(h):
        for sx in range(w):
            if px[sx, sy] == 0 or seen[sy * w + sx]:
                continue
            q = deque([(sx, sy)])
            seen[sy * w + sx] = 1
            pts = []
            x0 = x1 = sx
            y0 = y1 = sy
            while q:
                x, y = q.popleft()
                pts.append((x, y))
                x0, x1 = min(x0, x), max(x1, x)
                y0, y1 = min(y0, y), max(y1, y)
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx] \
                            and px[nx, ny]:
                        seen[ny * w + nx] = 1
                        q.append((nx, ny))
            area = len(pts)
            bw, bh = x1 - x0 + 1, y1 - y0 + 1
            if not (MIN_AREA <= area <= MAX_AREA):
                continue
            if not (ASPECT[0] <= bw / bh <= ASPECT[1]):
                continue
            # pencere merkezine en yakın blob rozettir (en büyüğü değil)
            d = ((x0 + x1) / 2 - w / 2) ** 2 + ((y0 + y1) / 2 - h / 2) ** 2
            if best is None or d < best[0]:
                best = (d, pts, (x0, y0, x1, y1))
    return best


def _stats(img, box):
    """Bir kutunun ortalama ve standart sapması (parlaklık)."""
    g = img.convert("L").crop(box)
    n = g.width * g.height
    if n == 0:
        return 1e9, 1e9
    hist = g.histogram()
    mean = sum(i * c for i, c in enumerate(hist)) / n
    var = sum(c * (i - mean) ** 2 for i, c in enumerate(hist)) / n
    return mean, var ** 0.5


def clone_fill(reg, bb):
    """Deliği, çevresindeki EN DÜZGÜN komşu alandan klonlayarak doldurur.

    Difüzyonla doldurmak, delik parlak bir nesneye (ör. ten) komşuysa o tonu içeri
    çekip leke bırakıyor. Dört yönden en düşük varyanslı ve delik kenarına en yakın
    tonda olan kaynak seçilir; böylece gerçek kumaş dokusu gelir.
    """
    x0, y0, x1, y1 = bb
    bw, bh = x1 - x0, y1 - y0
    ref, _ = _stats(reg, (max(0, x0 - 8), max(0, y0 - 8),
                          min(reg.width, x1 + 8), min(reg.height, y1 + 8)))
    best = None
    offsets = []
    for k in (1.15, 1.5, 2.0):                 # deliğe yakından uzağa
        offsets += [(0, int(bh * k)), (0, -int(bh * k)),
                    (int(bw * k), 0), (-int(bw * k), 0)]
    for dx, dy in offsets:
        sx0, sy0, sx1, sy1 = x0 + dx, y0 + dy, x1 + dx, y1 + dy
        if sx0 < 0 or sy0 < 0 or sx1 > reg.width or sy1 > reg.height:
            continue
        mean, sd = _stats(reg, (sx0, sy0, sx1, sy1))
        score = sd + abs(mean - ref) * 1.5      # düz VE aynı tonda olsun
        if best is None or score < best[0]:
            best = (score, (sx0, sy0, sx1, sy1))
    if best is None:
        print("  UYARI: klon için temiz komşu alan bulunamadı")
        return reg
    patch = reg.crop(best[1])
    out = reg.copy()
    out.paste(patch, (x0, y0))
    return out


def despeckle(im, box):
    """Klon sonrası kalan tekil parlak lekeyi siler.

    Parıltının bir ucu parlak bir kenara (ör. ten) denk geldiğinde tespit orada
    kırpılıyor ve küçük bir iz kalıyor. Yerel medyan dokuyu koruyup pencereden
    küçük olan bu lekeyi kaldırır.
    """
    reg = im.crop(box)
    med = reg.filter(ImageFilter.MedianFilter(21))
    diff = ImageChops.subtract(reg.convert("L"), med.convert("L"))
    mask = diff.point(lambda v: 255 if v > 14 else 0)
    if not mask.getbbox():
        return im
    mask = mask.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(2.5))
    im.paste(Image.composite(med, reg, mask), box)
    return im


def clean(path_in, path_out, debug=False):
    im = Image.open(path_in).convert("RGB")
    w, h = im.size
    cx, cy = int(w * BADGE[0]), int(h * BADGE[1])
    r = int(w * WINDOW)
    box = (max(0, cx - r), max(0, cy - r), min(w, cx + r), min(h, cy + r))
    reg = im.crop(box)
    rw, rh = reg.size

    small = reg.resize((rw // SCALE, rh // SCALE), Image.BOX)
    med = small.filter(ImageFilter.MedianFilter(MED)).resize((rw, rh), Image.BICUBIC)
    diff = ImageChops.subtract(reg.convert("L"), med.convert("L"))
    cand = diff.point(lambda v: 255 if v > THRESH else 0)

    blob = largest_blob(cand.resize((rw // 2, rh // 2), Image.BOX)
                        .point(lambda v: 255 if v > 127 else 0))
    if blob is None:
        print(f"filigran bulunamadı — {path_in} olduğu gibi kaydediliyor")
    else:
        _, pts, bb = blob
        hard = Image.new("L", (rw // 2, rh // 2), 0)
        hp = hard.load()
        for x, y in pts:
            hp[x, y] = 255
        hard = hard.resize((rw, rh), Image.BICUBIC).point(lambda v: 255 if v > 60 else 0)
        hard = hard.filter(ImageFilter.MaxFilter(2 * GROW + 1))
        soft = hard.filter(ImageFilter.GaussianBlur(FEATHER))
        pad = GROW + int(FEATHER * 2)
        fbb = (max(0, bb[0] * 2 - pad), max(0, bb[1] * 2 - pad),
               min(rw, bb[2] * 2 + pad), min(rh, bb[3] * 2 + pad))
        filled = clone_fill(reg, fbb)
        reg = Image.composite(filled, reg, soft)
        im.paste(reg, box)
        # kalan iz için ikinci geçiş (rozetin biraz genişletilmiş çevresi)
        m = 18
        pbox = (box[0] + max(0, bb[0] * 2 - m), box[1] + max(0, bb[1] * 2 - m),
                box[0] + min(rw, bb[2] * 2 + m), box[1] + min(rh, bb[3] * 2 + m))
        im = despeckle(im, pbox)
        gx, gy = box[0] + bb[0] * 2, box[1] + bb[1] * 2
        print(f"filigran temizlendi: ~{(bb[2]-bb[0])*2}x{(bb[3]-bb[1])*2}px "
              f"@ ({gx},{gy})")
        if debug:
            soft.save(str(path_out) + ".mask.png")

    if str(path_out).lower().endswith((".jpg", ".jpeg")):
        im.save(path_out, quality=95, subsampling=0)
    else:
        im.save(path_out)
    print(f"yazıldı: {path_out}  {im.size}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    clean(args[0], args[1], debug="--debug" in sys.argv)
